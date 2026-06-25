import fnmatch
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import win32api
import win32con

from core import (
    AppResources,
    AppSettings
)


class UninstallViaPowerShellForCurrentUser:
    PACKAGE_NAME_STABLE = "Microsoft.MicrosoftPCManager"
    PACKAGE_NAME_LEGACY = "Microsoft.PCManager"

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
        self._uninstall_via_windows_powershell()

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

    def _uninstall_via_windows_powershell(self):
        self._log(self.app_translator.translate("modules.uninstaller.uninstalling_via_windows_powershell"))
        self.logger.info("Uninstalling via Windows PowerShell")

        command = (
            r"Get-AppxPackage | "
            r"Where-Object { $_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$' } | "
            r"ForEach-Object { $_.PackageFullName; Remove-AppxPackage -Package $_.PackageFullName }"
        )

        try:
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", command],
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.uninstaller.uninstall_via_windows_powershell_error").format(error=str(e))
            )
            self.logger.error(f"An Error Occurred While Uninstalling via Windows PowerShell: {e}")
            return

        # Parse package names from stdout (one PackageFullName per line).
        package_names = [
            line.strip() for line in result.stdout.splitlines()
            if line.strip()
        ]

        if result.returncode == 0:
            self._log(
                self.app_translator.translate("modules.uninstaller.uninstall_via_windows_powershell_successfully")
            )
            self.logger.info("Uninstalled via Windows PowerShell successfully.")

            if package_names:
                self._log(
                    self.app_translator.translate("modules.uninstaller.removed_package_names").format(
                        paths="  - " + "\n  - ".join(package_names)
                    )
                )
                for pkg_name in package_names:
                    self.logger.info(f"Package Removed Successfully: {pkg_name}")
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr
            )
            self._log(
                self.app_translator.translate("modules.uninstaller.uninstall_via_windows_powershell_error").format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Uninstalling via Windows PowerShell:\n"
                + self._format_error_output(self.app_translator, result.stdout, result.stderr, use_localized=False)
            )

    def _get_config_cache_dir_paths(self):
        local_app_data = os.getenv("LocalAppData") or os.path.join(os.path.expandvars(r"%UserProfile%"), "AppData", "Local")
        program_data = os.getenv("ProgramData", r"C:\ProgramData")
        system_root = os.getenv("SystemRoot") or os.getenv("WinDir") or r"C:\Windows"
        temp_dir = tempfile.gettempdir()

        return [
            Path(local_app_data) / "Packages" / "Microsoft.MicrosoftPCManager_8wekyb3d8bbwe",
            Path(local_app_data) / "Packages" / "Microsoft.PCManager_8wekyb3d8bbwe",
            Path(local_app_data) / "PC Manager Store",
            Path(local_app_data) / "Windows Master Store",
            Path(program_data) / "Windows Master Setup",
            Path(program_data) / "Windows Master Store",
            Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Packages" / "Microsoft.MicrosoftPCManager_8wekyb3d8bbwe",
            Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Packages" / "Microsoft.PCManager_8wekyb3d8bbwe",
            Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Windows Master",
            Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Windows Master Store",
            Path(temp_dir) / "Windows Master Store",
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
            r"SOFTWARE\WOW6432Node\MSPCManager Store",
        ]

    def _basic_registries(self):
        removed_keys = []
        errors = []

        for key_path in self._get_basic_registry_paths():
            try:
                key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, key_path, 0, win32con.KEY_READ)
                win32api.RegCloseKey(key)
            except win32api.error:
                self.logger.info(f"Registry Key Does Not Exist, Skipped: {key_path}")
                continue

            try:
                win32api.RegDeleteTree(win32con.HKEY_LOCAL_MACHINE, key_path)
                removed_keys.append(key_path)
                self.logger.info(f"Registry Key Removed Successfully: {key_path}")
            except Exception as e:
                errors.append((key_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Registry Key: {key_path}\n{e}")

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

        for key_path in self._get_basic_registry_paths():
            full_key_path = f"HKEY_LOCAL_MACHINE\{key_path}"

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

                removed_keys.append(key_path)
                self.logger.info(f"Registry Key Removed Successfully: {key_path}")
            except Exception as e:
                errors.append((key_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Registry Key: {key_path}\n{e}")

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
        local_app_data = os.getenv("LocalAppData") or os.path.join(os.path.expandvars(r"%UserProfile%"), "AppData", "Local")
        system_root = os.getenv("SystemRoot") or os.getenv("WinDir") or r"C:\Windows"

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
            "*CREATEDUMP*.pf",
            "*MICROSOFT.WIC.PCWNDMANAGER*.pf",
            "*MSPCMANAGER*.pf",
            "*MSPCWNDMANAGER*.pf",
            "*PCMAUTORUN*.pf",
            "*PCMCHECKSUM*.pf",
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
