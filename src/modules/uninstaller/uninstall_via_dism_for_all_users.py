import fnmatch
import os
import shutil
import subprocess
import tempfile
import time
import tkinter.filedialog
from pathlib import Path

import win32api
import win32con

from core import (
    AppResources,
    AppSettings
)


class UninstallViaDISMForAllUsers:
    PACKAGE_NAME_STABLE = "Microsoft.MicrosoftPCManager"
    PACKAGE_NAME_LEGACY = "Microsoft.PCManager"

    def __init__(self, logger, app_translator, log_callback, image_type="online_image", selected_cleanup_options=None):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.image_type = image_type
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
        self._uninstall_via_dism()

        # Offline images remove provisioned packages only.
        if self.image_type == "offline_image":
            return

        if self.image_type == "online_image":
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
                elif option == "advanced_app_package_data":
                    self._advanced_app_package_data()
                elif option == "advanced_registries":
                    if use_ownership:
                        self._advanced_registries_with_ownership()
                    else:
                        self._advanced_registries()

    def _uninstall_via_dism(self):
        # Determine Image Type
        if self.image_type == "offline_image":
            image_path = tkinter.filedialog.askdirectory(
                title=self.app_translator.translate("modules.common.select_offline_image_dir")
            )
            if not image_path:
                self._log(self.app_translator.translate("pages.common.canceled_operation"))
                self.logger.info("The operation was canceled by the user.")
                return
            image_status = f"/Image:{image_path}"
        else:
            image_status = "/Online"

        # Query Provisioned Packages
        self._log(self.app_translator.translate("modules.uninstaller.querying_dism_provisioned_packages"))
        self.logger.info(f"Querying Provisioned Packages via DISM ({image_status})")

        try:
            result = subprocess.run(
                ["Dism.exe", image_status, "/Get-ProvisionedAppxPackages"],
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.uninstaller.query_dism_provisioned_packages_error").format(error=str(e))
            )
            self.logger.error(f"An Error Occurred While Querying Provisioned Packages via DISM ({image_status}): {e}")
            return

        if result.returncode != 0:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr
            )
            self._log(
                self.app_translator.translate("modules.uninstaller.query_dism_provisioned_packages_error").format(error=error_output)
            )
            self.logger.error(
                f"An Error Occurred While Querying Provisioned Packages via DISM ({image_status}):\n"
                + self._format_error_output(self.app_translator, result.stdout, result.stderr, use_localized=False)
            )
            return

        # Parse the output to find packages related to Microsoft PC Manager.
        package_names = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("PackageName :"):
                pkg_name = line[len("PackageName :"):].strip()
                if self.PACKAGE_NAME_STABLE in pkg_name or self.PACKAGE_NAME_LEGACY in pkg_name:
                    package_names.append(pkg_name)

        if not package_names:
            self._log(
                self.app_translator.translate("modules.uninstaller.no_matching_packages_found")
            )
            self.logger.info("No matching provisioned packages found for Microsoft PC Manager.")
            return

        # Remove Identified Packages
        self._log(self.app_translator.translate("modules.uninstaller.removing_dism_provisioned_packages"))
        removed_packages = []
        errors = []

        for pkg_name in package_names:
            self.logger.info(f"Removing Provisioned Package via DISM ({image_status}): {pkg_name}")

            try:
                remove_result = subprocess.run(
                    ["Dism.exe", image_status, "/Remove-ProvisionedAppxPackage", f"/PackageName:{pkg_name}"],
                    check=False,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except Exception as e:
                errors.append((pkg_name, str(e)))
                self.logger.error(f"An Error Occurred While Removing Provisioned Package via DISM ({image_status}): {pkg_name}\n{e}")
                continue

            if remove_result.returncode == 0:
                removed_packages.append(pkg_name)
                self.logger.info(f"Provisioned Package Removed Successfully: {pkg_name}")
            else:
                error_output = self._format_error_output(
                    self.app_translator, remove_result.stdout, remove_result.stderr
                )
                errors.append((pkg_name, error_output))
                self.logger.error(
                    f"An Error Occurred While Removing Provisioned Package via DISM ({image_status}): {pkg_name}\n"
                    + self._format_error_output(self.app_translator, remove_result.stdout, remove_result.stderr, use_localized=False)
                )

        if removed_packages:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_dism_provisioned_packages_successfully").format(
                    paths="  - " + "\n  - ".join(removed_packages)
                )
            )

        for pkg_name, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_dism_provisioned_packages_error").format(
                    package_name=pkg_name, error=error
                )
            )

    def _uninstall_via_windows_powershell(self):
        self._log(self.app_translator.translate("modules.uninstaller.uninstalling_via_windows_powershell"))
        self.logger.info("Uninstalling via Windows PowerShell")

        base_command = (
            r"Get-AppxPackage -AllUsers | "
            r"Where-Object {$_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$'} | "
            r"Remove-AppxPackage -AllUsers"
        )

        for use_all_users in [True, False]:
            command = base_command if use_all_users else (
                r"Get-AppxPackage | "
                r"Where-Object {$_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$'} | "
                r"Remove-AppxPackage"
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
                continue

            if result.returncode == 0:
                self._log(
                    self.app_translator.translate("modules.uninstaller.uninstall_via_windows_powershell_successfully")
                )
                self.logger.info("Uninstalled via Windows PowerShell successfully.")
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
        # Generally, there's no need to hard-code a fallback to C:\Users\%UserName%.
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

                # Retry existence check to avoid race condition after RMDIR.
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
                # Check if key exists first.
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
        # Generally, there's no need to hard-code a fallback to C:\Users\%UserName%.
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
                Path(system_root) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Microsoft" / "CLR_v4.0" / "UsageLogs",
                usage_logs_patterns
            ),
            (
                Path(system_root) / "Prefetch",
                prefetch_patterns
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

                        # Retry existence check to avoid race condition after DEL.
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

    @staticmethod
    def _get_advanced_app_package_data_specs():
        # Generally, there's no need to hard-code a fallback to C:\Users\%UserName%.
        local_app_data = os.getenv("LocalAppData") or os.path.join(os.path.expandvars(r"%UserProfile%"), "AppData", "Local")
        program_data = os.getenv("ProgramData", r"C:\ProgramData")
        program_files = os.getenv("ProgramFiles", r"C:\Program Files")

        return [
            # (parent_path, glob_pattern)
            # Directories
            (Path(local_app_data) / "Packages" / "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe" / "LocalCache", "Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe"),
            (Path(local_app_data) / "Packages" / "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe" / "LocalCache", "MSPCManager_*_8wekyb3d8bbwe"),
            (Path(local_app_data) / "Packages" / "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe" / "LocalCache", "Microsoft.PCManager_*_8wekyb3d8bbwe"),
            (Path(program_data) / "Microsoft" / "Windows" / "AppRepository" / "Packages", "Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe"),
            (Path(program_data) / "Microsoft" / "Windows" / "AppRepository" / "Packages", "Microsoft.PCManager_*_8wekyb3d8bbwe"),
            (Path(program_data) / "Microsoft" / "Windows" / "WindowsApps", "Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe"),
            (Path(program_data) / "Microsoft" / "Windows" / "WindowsApps", "Microsoft.PCManager_*_8wekyb3d8bbwe"),
            (Path(program_data) / "Packages", "Microsoft.MicrosoftPCManager_8wekyb3d8bbwe"),
            (Path(program_data) / "Packages", "Microsoft.PCManager_8wekyb3d8bbwe"),
            (Path(program_files) / "WindowsApps", "Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe"),
            (Path(program_files) / "WindowsApps", "Microsoft.PCManager_*_8wekyb3d8bbwe"),
            # Files
            (Path(program_data) / "Microsoft" / "Windows" / "AppRepository", "Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe.xml"),
            (Path(program_data) / "Microsoft" / "Windows" / "AppRepository", "Microsoft.PCManager_*_8wekyb3d8bbwe.xml"),
            # Files with Wildcard Subfolder
            (Path(local_app_data) / "Packages" / "Microsoft.Windows.Search_cw5n1h2txyewy" / "LocalState" / "AppIconCache", "*/Microsoft_MicrosoftPCManager_8wekyb3d8bbwe!App"),
            (Path(local_app_data) / "Packages" / "Microsoft.Windows.Search_cw5n1h2txyewy" / "LocalState" / "AppIconCache", "*/Microsoft_PCManager_8wekyb3d8bbwe!App"),
        ]

    def _advanced_app_package_data(self):
        removed_items = []
        errors = []

        for parent_path, pattern in self._get_advanced_app_package_data_specs():
            if not parent_path.exists():
                self.logger.info(f"Parent Directory Does Not Exist, Skipped: {parent_path}")
                continue

            for item_path in parent_path.glob(pattern):
                try:
                    if item_path.is_dir():
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
                            str(item_path)
                        ]
                    else:
                        remove_cmd = [
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
                            str(item_path)
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

                    # Retry existence check to avoid race condition after RMDIR/DEL.
                    still_exists = True
                    for _ in range(3):
                        if not item_path.exists():
                            still_exists = False
                            break
                        time.sleep(0.3)

                    if still_exists:
                        if result.stderr:
                            self._log(
                                self.app_translator.translate("common.stderr") + ":\n" + result.stderr
                            )
                            self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                        raise Exception("Item still exists after removal attempt.")

                    removed_items.append(str(item_path))
                    self.logger.info(f"Application Package Data Removed Successfully: {item_path}")
                except Exception as e:
                    errors.append((str(item_path), str(e)))
                    self.logger.error(f"An Error Occurred While Removing Application Package Data: {item_path}\n{e}")

        if removed_items:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_app_package_data_successfully").format(
                    paths="  - " + "\n  - ".join(removed_items)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_app_package_data_error").format(
                    path=path, error=error
                )
            )

    @staticmethod
    def _get_hive_name(hive):
        mapping = {
            win32con.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
            win32con.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE",
        }
        return mapping.get(hive, "")

    @staticmethod
    def _get_advanced_registry_specs():
        return [
            # (type, root, key_path, pattern)
            # type="value": Delete values whose name matches pattern.
            ("value", win32con.HKEY_CURRENT_USER,
             r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store",
             r"C:\Program Files\WindowsApps\Microsoft.MicrosoftPCManager_*__8wekyb3d8bbwe\PCManager\MSPCManager.exe"),
            # type="key": Delete subkeys whose name matches pattern.
            ("key", win32con.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\WOW6432Node\Microsoft\SecurityManager\CapAuthz\ApplicationsEx",
             "Microsoft.MicrosoftPCManager_*__8wekyb3d8bbwe"),
            ("key", win32con.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\Microsoft\SecurityManager\CapAuthz\ApplicationsEx",
             "Microsoft.PCManager_*__8wekyb3d8bbwe"),
            ("key", win32con.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\PackageRepository\Packages",
             "Microsoft.PCManager_*__8wekyb3d8bbwe"),
        ]

    def _advanced_registries(self):
        removed_items = []
        errors = []

        for spec_type, root, key_path, pattern in self._get_advanced_registry_specs():
            try:
                key = win32api.RegOpenKeyEx(root, key_path, 0, win32con.KEY_READ)
            except win32api.error:
                self.logger.info(f"Registry Key Does Not Exist, Skipped: {key_path}")
                continue

            try:
                if spec_type == "value":
                    index = 0
                    while True:
                        try:
                            value_name, _, _ = win32api.RegEnumValue(key, index)
                            if fnmatch.fnmatch(value_name, pattern):
                                win32api.RegDeleteValue(key, value_name)
                                removed_items.append(f"{key_path} ({value_name})")
                                self.logger.info(f"Registry Value Removed Successfully: {value_name}")
                            index += 1
                        except win32api.error:
                            break
                else:  # "key"
                    index = 0
                    while True:
                        try:
                            subkey_name = win32api.RegEnumKey(key, index)
                            if fnmatch.fnmatch(subkey_name, pattern):
                                full_subkey = f"{key_path}\{subkey_name}"
                                win32api.RegCloseKey(key)
                                win32api.RegDeleteTree(root, full_subkey)
                                removed_items.append(full_subkey)
                                self.logger.info(f"Registry Subkey Removed Successfully: {full_subkey}")
                                key = win32api.RegOpenKeyEx(root, key_path, 0, win32con.KEY_READ)
                                index = 0
                                continue
                            index += 1
                        except win32api.error:
                            break
            except Exception as e:
                errors.append((key_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Advanced Registry: {key_path}\n{e}")
            finally:
                try:
                    win32api.RegCloseKey(key)
                except win32api.error:
                    pass

        if removed_items:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_registries_successfully").format(
                    paths="  - " + "\n  - ".join(removed_items)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_registries_error").format(
                    path=path, error=error
                )
            )

    def _advanced_registries_with_ownership(self):
        removed_items = []
        errors = []

        for spec_type, root, key_path, pattern in self._get_advanced_registry_specs():
            hive_name = self._get_hive_name(root)
            full_path = f"{hive_name}\{key_path}"

            try:
                key = win32api.RegOpenKeyEx(root, key_path, 0, win32con.KEY_READ)
            except win32api.error:
                self.logger.info(f"Registry Key Does Not Exist, Skipped: {key_path}")
                continue

            try:
                if spec_type == "value":
                    index = 0
                    while True:
                        try:
                            value_name, _, _ = win32api.RegEnumValue(key, index)
                            if fnmatch.fnmatch(value_name, pattern):
                                del_cmd = [
                                    self.nsudo_path,
                                    "-U:T",
                                    "-P:E",
                                    "-ShowWindowMode:Hide",
                                    "-UseCurrentConsole",
                                    "reg.exe",
                                    "delete",
                                    full_path,
                                    "/v",
                                    value_name,
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
                                removed_items.append(f"{key_path} ({value_name})")
                                self.logger.info(f"Registry Value Removed Successfully: {value_name}")
                                index = 0
                                continue
                            index += 1
                        except win32api.error:
                            break
                else:  # "key"
                    index = 0
                    while True:
                        try:
                            subkey_name = win32api.RegEnumKey(key, index)
                            if fnmatch.fnmatch(subkey_name, pattern):
                                subkey_full_path = f"{full_path}\{subkey_name}"
                                del_cmd = [
                                    self.nsudo_path,
                                    "-U:T",
                                    "-P:E",
                                    "-ShowWindowMode:Hide",
                                    "-UseCurrentConsole",
                                    "reg.exe",
                                    "delete",
                                    subkey_full_path,
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
                                removed_items.append(f"{key_path}\{subkey_name}")
                                self.logger.info(f"Registry Subkey Removed Successfully: {subkey_name}")
                                win32api.RegCloseKey(key)
                                key = win32api.RegOpenKeyEx(root, key_path, 0, win32con.KEY_READ)
                                index = 0
                                continue
                            index += 1
                        except win32api.error:
                            break
            except Exception as e:
                errors.append((key_path, str(e)))
                self.logger.error(f"An Error Occurred While Removing Advanced Registry: {key_path}\n{e}")
            finally:
                try:
                    win32api.RegCloseKey(key)
                except win32api.error:
                    pass

        if removed_items:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_registries_successfully").format(
                    paths="  - " + "\n  - ".join(removed_items)
                )
            )

        for path, error in errors:
            self._log(
                self.app_translator.translate("modules.uninstaller.remove_advanced_registries_error").format(
                    path=path, error=error
                )
            )
