import os
import winreg
from pathlib import Path


class GetMicrosoftPCManagerVersionNumber:
    @staticmethod
    def get_microsoft_pc_manager_version_number():
        microsoft_pc_manager_version = None

        # Package Name: Microsoft.MicrosoftPCManager
        if microsoft_pc_manager_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications") as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if "Microsoft.MicrosoftPCManager_" in subkey_name:
                            microsoft_pc_manager_version = subkey_name.split("_")[1]
                            break
            except FileNotFoundError:
                pass

            # Package Name (Legacy): Microsoft.PCManager
            if microsoft_pc_manager_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications") as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            subkey_name = winreg.EnumKey(key, i)
                            if "Microsoft.PCManager_" in subkey_name:
                                microsoft_pc_manager_version = subkey_name.split("_")[1]
                                break
                except FileNotFoundError:
                    pass

                # Package Name: Microsoft.MicrosoftPCManager
                if microsoft_pc_manager_version is None:
                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                            r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.PCManager_8wekyb3d8bbwe\\Schemas") as key:
                            package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                            microsoft_pc_manager_version = package_full_name.split("_")[1]
                    except FileNotFoundError:
                        pass

                    # Package Name (Legacy): Microsoft.PCManager
                    if microsoft_pc_manager_version is None:
                        try:
                            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\\Schemas") as key:
                                package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                                microsoft_pc_manager_version = package_full_name.split("_")[1]
                        except FileNotFoundError:
                            pass

                        # EXE Installer (Internal Version)
                        if microsoft_pc_manager_version is None:
                            try:
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                                    r"SOFTWARE\\WOW6432Node\\MSPCManager Store") as key:
                                    microsoft_pc_manager_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                            except FileNotFoundError:
                                pass

                                # Program Folder in %ProgramFiles%
                                if microsoft_pc_manager_version is None:
                                    try:
                                        program_files_path = os.environ.get("ProgramFiles")
                                        if program_files_path:
                                            windows_apps_path = Path(program_files_path) / "WindowsApps"
                                            patterns = [
                                                "Microsoft.MicrosoftPCManager_*_*__8wekyb3d8bbwe",
                                                "Microsoft.MicrosoftPCManager_*_neutral_~_8wekyb3d8bbwe"
                                            ]
                                            for pattern in patterns:
                                                for app_dir in windows_apps_path.glob(pattern):
                                                    try:
                                                        version = app_dir.name.split("_")[1]
                                                        microsoft_pc_manager_version = version
                                                        break
                                                    except IndexError:
                                                        continue
                                                if microsoft_pc_manager_version:
                                                    break
                                    except (FileNotFoundError, PermissionError):
                                        pass
        return microsoft_pc_manager_version

    @staticmethod
    def get_microsoft_pc_manager_beta_version_number():
        microsoft_pc_manager_beta_version = None

        # Microsoft PC Manager Beta Setup
        if microsoft_pc_manager_beta_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager") as key:
                    microsoft_pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
            except FileNotFoundError:
                pass

            # Microsoft PC Manager Beta Uninstaller
            if microsoft_pc_manager_beta_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MSPCManager") as key:
                        microsoft_pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                except FileNotFoundError:
                    pass

                # EXE File Properties
                if microsoft_pc_manager_beta_version is None:
                    try:
                        import win32api
                        program_files_path = os.environ.get("ProgramFiles")
                        if program_files_path:
                            exe_path = Path(program_files_path) / "Microsoft PC Manager" / "MSPCManager.exe"
                            if exe_path.exists():
                                info = win32api.GetFileVersionInfo(str(exe_path), "\\")
                                if info:
                                    ms, ls = info["FileVersionMS"], info["FileVersionLS"]
                                    microsoft_pc_manager_beta_version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                    except (FileNotFoundError, ImportError):
                        pass
        return microsoft_pc_manager_beta_version
