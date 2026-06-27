import fnmatch
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import psutil
import win32api
import win32con

from core import (
    AppResources,
    AppSettings
)


class UninstallBeta:
    def __init__(self, logger, app_translator, log_callback, selected_cleanup_options=None):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_cleanup_options = selected_cleanup_options if selected_cleanup_options else {}
        self.nsudo_path = AppResources.nsudo_path()

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    @staticmethod
    def _format_error_output(app_translator, stdout_text, stderr_text, use_localized=True):
        stdout_label = app_translator.translate(
            "common.stdout") if use_localized else "Stdout"
        stderr_label = app_translator.translate(
            "common.stderr") if use_localized else "Stderr"
        parts = []
        if stdout_text:
            parts.append(f"{stdout_label}:\n{stdout_text}")
        if stderr_text:
            if parts:
                parts.append("---")
            parts.append(f"{stderr_label}:\n{stderr_text}")
        return "\n".join(parts)

    def execute(self):
        is_uninstall = self._uninstall_beta()

        if is_uninstall:
            self.logger.debug(f"Selected Options for Additional Cleanup: {self.selected_cleanup_options}")
            use_ownership = AppSettings.is_take_ownership_enabled()
            if use_ownership:
                self.logger.debug(f"NSudo Path: {self.nsudo_path}")

            for option, enabled in self.selected_cleanup_options.items():
                if not enabled:
                    continue

                if option == "basic_config_cache_dirs":
                    if use_ownership:
                        self._basic_config_cache_dirs_with_ownership()
                    else:
                        self._basic_config_cache_dirs()
                elif option == "basic_registries":
                    if use_ownership:
                        self._basic_registries_with_ownership()
                    else:
                        self._basic_registries()
                elif option == "basic_cache_files":
                    if use_ownership:
                        self._basic_cache_files_with_ownership()
                    else:
                        self._basic_cache_files()

    def find_child_processes_by_ppid(self, ppid, name_pattern):
        # Match child processes based on parent PID and process name pattern.
        matched_pids = []
        for proc in psutil.process_iter(["pid", "ppid", "name"]):
            try:
                proc_name, proc_ppid = proc.info["name"], proc.info["ppid"]
                if fnmatch.fnmatch(proc_name, name_pattern) and proc_ppid == ppid:
                    matched_pids.append(proc.info["pid"])

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return matched_pids

    def monitor_uninstall(self, ppid, child_pattern="Uninst*.exe", exe_path=None, check_interval=2.0, timeout=2.0):
        self.logger.info(f"Monitoring Uninstall Process: Parent PID = {ppid}, Child Pattern = {child_pattern}, EXE Path = {exe_path}")
        # Store all target child PIDs to monitor
        target_pids = set()

        # Phase 1: Capture child processes through direct parent-child relationship.
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                parent = psutil.Process(ppid)
                children = parent.children(recursive=False)
                for child in children:
                    child_name = child.name()
                    if fnmatch.fnmatch(child_name, child_pattern):
                        target_pids.add(child.pid)
                        self.logger.info(f"Captured Child Process: PID = {child.pid}, Name = {child_name}")
            except psutil.NoSuchProcess:
                # Parent process has exited, moving to PPID reverse lookup phase.
                self.logger.info("Parent process has exited, stopping polling and moving to Parent PID reverse lookup.")
                break
            time.sleep(0.1)

        # Phase 2: If direct capture fails, attempt PPID reverse lookup across the OS.
        if not target_pids:
            self._log(self.app_translator.translate("modules.uninstaller.searching_for_child_process"))
            self.logger.info("No child processes captured through direct parent-child relationship, attempting Parent PID reverse lookup across the OS...")
            found = self.find_child_processes_by_ppid(ppid, child_pattern)
            if found:
                target_pids.update(found)
                for pid in found:
                    try:
                        p = psutil.Process(pid)
                        self.logger.info(f"Found Child Process via Parent PID Reverse Lookup: PID = {pid}, Name = {p.name()}")
                    except psutil.NoSuchProcess:
                        pass
            else:
                # No matching child processes found, log and terminate monitoring.
                self.logger.info(f"Failed to find any matching child processes, monitoring terminated.")
                return False

        # Output the list of target PIDs being monitored.
        for child_pid in sorted(target_pids):
            self._log(self.app_translator.translate("modules.uninstaller.starting_uninstaller_with_pids").format(ppid=ppid, pid=child_pid))

        process_word = "Process" if len(target_pids) == 1 else "Processes"
        self.logger.info(f"Starting to Monitor {len(target_pids)} Target {process_word}: {sorted(target_pids)}")
        # Phase 3: Continuously monitor all target child processes, waiting for them to exit.
        while True:
            for pid in list(target_pids):
                try:
                    p = psutil.Process(pid)
                    if not p.is_running():
                        self.logger.info(f"Target PID = {pid} has stopped running.")
                        target_pids.remove(pid)
                except psutil.NoSuchProcess:
                    self.logger.info(f"Target PID = {pid} no longer exists.")
                    target_pids.remove(pid)
            # If all target processes have exited, check if the uninstaller executable still exists.
            if not target_pids:
                self._log(self.app_translator.translate("modules.uninstaller.verifying_uninstall_result"))
                if not Path(exe_path).exists():
                    self.logger.info("All target processes have exited and the uninstaller executable no longer exists.")
                    return True
                else:
                    # If the uninstaller executable still exists, it may indicate that the uninstallation was canceled or failed.
                    self._log(self.app_translator.translate("modules.uninstaller.uninstallation_not_completed"))
                    self.logger.info("All target processes have exited but the uninstaller executable still exists, indicating a potential cancellation.")
                    return False
            time.sleep(check_interval)

    def _uninstall_beta(self):
        try:
            uninstaller_path = Path(os.getenv("ProgramFiles", r"C:\Program Files")) / "Microsoft PC Manager" / "Uninst.exe"
            self._log(self.app_translator.translate("modules.common.file_path").format(file_path=uninstaller_path))
            self.logger.info(f"Attempting to Execute Microsoft PC Manager Beta Uninstaller at: {uninstaller_path}")
            if not uninstaller_path.exists():
                self._log(self.app_translator.translate("modules.uninstaller.uninstaller_not_found"))
                self.logger.error("Microsoft PC Manager beta uninstaller not found.")
                return False

            result = subprocess.Popen([uninstaller_path], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      text=True)

            ppid = result.pid
            self._log(self.app_translator.translate("modules.uninstaller.waiting_for_uninstaller"))
            self.logger.info("Waiting for Microsoft PC Manager beta uninstaller to start...")
            is_uninstall = self.monitor_uninstall(ppid = ppid, child_pattern = "Uninst*.exe", exe_path = uninstaller_path)
            if is_uninstall:
                self._log(self.app_translator.translate("modules.uninstaller.uninstall_via_uninstaller_successfully"))
            return is_uninstall
        except Exception as e:
            self._log(self.app_translator.translate("modules.uninstaller.uninstall_via_uninstaller_error").format(error=str(e)))
            self.logger.error(f"An Error Occurred While Uninstalling via Microsoft PC Manager Beta Uninstaller:\n{e}")
            return False

    @staticmethod
    def _get_config_cache_dir_paths():
        # A robust fallback using os.path.expanduser("~").
        local_app_data = os.getenv("LocalAppData") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        program_data = os.getenv("ProgramData", r"C:\ProgramData")
        program_files = os.getenv("ProgramFiles", r"C:\Program Files")
        system_root = os.getenv("SystemRoot") or os.getenv("WinDir") or r"C:\Windows"
        temp_dir = tempfile.gettempdir()

        return [
            Path(local_app_data) / "PC Manager",
            Path(local_app_data) / "Windows Master",
            Path(program_data) / "PCMConfigPath",
            Path(program_data) / "Windows Master",
            Path(program_data) / "Windows Master Setup",
            Path(program_files) / "Microsoft PC Manager",
            Path(program_files) / "WindowsMaster",
            Path(program_files) / "Windows Master",
            Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Windows Master",
            Path(system_root) / "SystemTemp" / "Windows Master",
            Path(temp_dir) / "Windows Master",
            Path(temp_dir) / "WM Scan Test",
        ]

    def _basic_config_cache_dirs(self):
        removed_paths = []
        errors = []

        for dir_path in self._get_config_cache_dir_paths():
            if not dir_path.exists():
                self.logger.info(f"Config/Cache Directory Does Not Exist, Skipped: {dir_path}")
                continue

            try:
                shutil.rmtree(dir_path)
                removed_paths.append(str(dir_path))
                self.logger.info(f"Config/Cache Directory Removed Successfully: {dir_path}")
            except Exception as e:
                errors.append((str(dir_path), str(e)))
                self.logger.error(f"An Error Occurred While Removing Config/Cache Directory: {dir_path}\n{e}")

        if removed_paths:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_config_cache_dir_successfully").format(
                    paths="  - " + "\n  - ".join(removed_paths)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_config_cache_dir_error").format(
                    path=path, error=error
                )
            )

    def _basic_config_cache_dirs_with_ownership(self):
        removed_paths = []
        errors = []

        for dir_path in self._get_config_cache_dir_paths():
            if not dir_path.exists():
                self.logger.info(f"Config/Cache Directory Does Not Exist, Skipped: {dir_path}")
                continue

            try:
                remove_cmd = [
                    self.nsudo_path,
                    "-U:T",
                    "-P:E",
                    "-ShowWindowMode:Hide",
                    "-UseCurrentConsole",
                    "cmd.exe",
                    "/C",
                    "RMDIR",
                    "/S",
                    "/Q",
                    str(dir_path)
                ]
                result = subprocess.run(
                    remove_cmd,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                if result.returncode != 0:
                    raise Exception(f"NSudo Error Code: {result.returncode}")

                still_exists = True
                for _ in range(3):
                    if not dir_path.exists():
                        still_exists = False
                        break
                    time.sleep(0.3)

                if still_exists:
                    if result.stderr:
                        self._log(
                            self.app_translator.translate("common.stderr") + ":\n" + result.stderr
                        )
                        self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                    raise Exception("Directory still exists after removal attempt.")

                removed_paths.append(str(dir_path))
                self.logger.info(f"Config/Cache Directory Removed Successfully: {dir_path}")
            except Exception as e:
                errors.append((str(dir_path), str(e)))
                self.logger.error(f"An Error Occurred While Removing Config/Cache Directory: {dir_path}\n{e}")

        if removed_paths:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_config_cache_dir_successfully").format(
                    paths="  - " + "\n  - ".join(removed_paths)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_config_cache_dir_error").format(
                    path=path, error=error
                )
            )

    @staticmethod
    def _get_basic_registry_paths():
        return [
            (win32con.HKEY_CURRENT_USER, r"Software\WindowsMaster"),
            (win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run\WindowsMasterUI"),
            (win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsMasterUI"),
            (win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager"),
            (win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\微软电脑管家"),
            (win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\MSPCManager"),
        ]

    @staticmethod
    def _format_registry_path(hive, subkey):
        hive_name = {
            win32con.HKEY_CLASSES_ROOT: "HKEY_CLASSES_ROOT",
            win32con.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
            win32con.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE",
            win32con.HKEY_USERS: "HKEY_USERS",
            win32con.HKEY_CURRENT_CONFIG: "HKEY_CURRENT_CONFIG",
        }
        return f"{hive_name.get(hive, 'UNKNOWN')}\\{subkey}"

    def _basic_registries(self):
        removed_keys = []
        errors = []

        for hive, subkey in self._get_basic_registry_paths():
            full_path = self._format_registry_path(hive, subkey)

            try:
                key = win32api.RegOpenKeyEx(hive, subkey, 0, win32con.KEY_READ)
                win32api.RegCloseKey(key)
            except win32api.error:
                self.logger.info(f"Registry Key Does Not Exist, Skipped: {full_path}")
                continue

            try:
                win32api.RegDeleteTree(hive, subkey)
                removed_keys.append(full_path)
                self.logger.info(f"Registry Key Removed Successfully: {full_path}")
            except Exception as e:
                errors.append((full_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Registry Key: {full_path}\n{e}")

        if removed_keys:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_registries_successfully").format(
                    paths="  - " + "\n  - ".join(removed_keys)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_registries_error").format(
                    path=path, error=error
                )
            )

    def _basic_registries_with_ownership(self):
        removed_keys = []
        errors = []

        for hive, subkey in self._get_basic_registry_paths():
            full_key_path = self._format_registry_path(hive, subkey)

            try:
                del_cmd = [
                    self.nsudo_path,
                    "-U:T",
                    "-P:E",
                    "-ShowWindowMode:Hide",
                    "-UseCurrentConsole",
                    "reg.exe",
                    "delete",
                    full_key_path,
                    "/f"
                ]
                result = subprocess.run(
                    del_cmd,
                    check=False,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                if result.returncode != 0:
                    raise Exception(f"NSudo Error Code: {result.returncode}")

                if result.stderr:
                    raise Exception(f"reg.exe Error: {result.stderr.strip()}")

                removed_keys.append(full_key_path)
                self.logger.info(f"Registry Key Removed Successfully: {full_key_path}")
            except Exception as e:
                errors.append((full_key_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Registry Key: {full_key_path}\n{e}")

        if removed_keys:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_registries_successfully").format(
                    paths="  - " + "\n  - ".join(removed_keys)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_registries_error").format(
                    path=path, error=error
                )
            )

    @staticmethod
    def _get_basic_cache_file_specs():
        # A robust fallback using os.path.expanduser("~").
        local_app_data = os.getenv("LocalAppData") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        program_data = os.getenv("ProgramData", r"C:\ProgramData")
        system_root = os.getenv("SystemRoot") or os.getenv("WinDir") or r"C:\Windows"
        user_profile = os.getenv("UserProfile") or os.path.expanduser("~")

        usage_logs_patterns = [
            "*BGADefMgr*.log",
            "*Microsoft.WIC.PCWndManager.Plugin*.log",
            "*MSPCManager*.log",
            "*MSPCWndManager*.log",
            "*PCMAutoRun*.log",
            "*PCMCheckSum*.log",
        ]
        prefetch_patterns = [
            "*BGADEFMGR*.pf",
            "*MSPCMANAGER*.pf",
            "*MSPCWNDMANAGER*.pf",
            "*PCMAUTORUN*.pf",
            "*PCMCHECKSUM*.pf",
            "*UNINST*.pf",
            "*WINDOWSMASTER*.pf",
        ]
        shortcut_patterns = [
            "*PC Manager*.lnk",
            "*MSPCManager*.lnk",
            "*Microsoft PC Manager*.lnk",
            "*Microsoft 電腦管家*.lnk",
            "*Windows Master*.lnk",
            "*微软电脑管家*.lnk",
        ]

        return [
            (
                Path(local_app_data) / "Microsoft" / "CLR_v4.0" / "UsageLogs",
                usage_logs_patterns
            ),
            (
                Path(system_root) / "Prefetch",
                prefetch_patterns
            ),
            (
                Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Microsoft" / "CLR_v4.0" / "UsageLogs",
                usage_logs_patterns
            ),
            (
                Path(user_profile) / "Desktop",
                shortcut_patterns
            ),
            (
                Path(program_data) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
                shortcut_patterns
            ),
        ]

    def _basic_cache_files(self):
        removed_files = []
        errors = []

        for dir_path, patterns in self._get_basic_cache_file_specs():
            if not dir_path.exists():
                self.logger.info(f"Directory Does Not Exist, Skipped: {dir_path}")
                continue

            for pattern in patterns:
                for file_path in dir_path.glob(pattern):
                    try:
                        file_path.unlink()
                        removed_files.append(str(file_path))
                        self.logger.info(f"Cache File Removed Successfully: {file_path}")
                    except Exception as e:
                        errors.append((str(file_path), str(e)))
                        self.logger.error(f"An Error Occurred While Removing Cache File: {file_path}\n{e}")

        if removed_files:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_cache_files_successfully").format(
                    paths="  - " + "\n  - ".join(removed_files)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_cache_files_error").format(
                    path=path, error=error
                )
            )

    def _basic_cache_files_with_ownership(self):
        removed_files = []
        errors = []

        for dir_path, patterns in self._get_basic_cache_file_specs():
            if not dir_path.exists():
                self.logger.info(f"Directory Does Not Exist, Skipped: {dir_path}")
                continue

            for pattern in patterns:
                for file_path in dir_path.glob(pattern):
                    try:
                        del_cmd = [
                            self.nsudo_path,
                            "-U:T",
                            "-P:E",
                            "-ShowWindowMode:Hide",
                            "-UseCurrentConsole",
                            "cmd.exe",
                            "/C",
                            "DEL",
                            "/F",
                            "/Q",
                            str(file_path)
                        ]
                        result = subprocess.run(
                            del_cmd,
                            shell=False,
                            text=True,
                            capture_output=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )

                        if result.returncode != 0:
                            raise Exception(f"NSudo Error Code: {result.returncode}")

                        still_exists = True
                        for _ in range(3):
                            if not file_path.exists():
                                still_exists = False
                                break
                            time.sleep(0.3)

                        if still_exists:
                            if result.stderr:
                                self._log(
                                    self.app_translator.translate("common.stderr") + ":\n" + result.stderr
                                )
                                self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                            raise Exception("File still exists after removal attempt.")

                        removed_files.append(str(file_path))
                        self.logger.info(f"Cache File Removed Successfully: {file_path}")
                    except Exception as e:
                        errors.append((str(file_path), str(e)))
                        self.logger.error(f"An Error Occurred While Removing Cache File: {file_path}\n{e}")

        if removed_files:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_cache_files_successfully").format(
                    paths="  - " + "\n  - ".join(removed_files)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_basic_cache_files_error").format(
                    path=path, error=error
                )
            )
