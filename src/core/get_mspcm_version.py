import os
import winreg
from pathlib import Path

import pefile


class GetMSPCMVersion:
    @staticmethod
    def get_microsoft_pc_manager_version():
        microsoft_pc_manager_version = None

        # Microsoft.MicrosoftPCManager
        if microsoft_pc_manager_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Applications") as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if "Microsoft.MicrosoftPCManager_" in subkey_name:
                            microsoft_pc_manager_version = subkey_name.split("_")[1]
                            break
            except FileNotFoundError:
                pass

            # Microsoft.PCManager (Legacy)
            if microsoft_pc_manager_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Applications") as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            subkey_name = winreg.EnumKey(key, i)
                            if "Microsoft.PCManager_" in subkey_name:
                                microsoft_pc_manager_version = subkey_name.split("_")[1]
                                break
                except FileNotFoundError:
                    pass

                # Microsoft.MicrosoftPCManager
                if microsoft_pc_manager_version is None:
                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                            r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData\Microsoft.PCManager_8wekyb3d8bbwe\Schemas") as key:
                            package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                            microsoft_pc_manager_version = package_full_name.split("_")[1]
                    except FileNotFoundError:
                        pass

                    # Microsoft.PCManager (Legacy)
                    if microsoft_pc_manager_version is None:
                        try:
                            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                r"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\Schemas") as key:
                                package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                                microsoft_pc_manager_version = package_full_name.split("_")[1]
                        except FileNotFoundError:
                            pass

                        # EXE Installer (Internal Version)
                        if microsoft_pc_manager_version is None:
                            try:
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                                    r"SOFTWARE\WOW6432Node\MSPCManager Store") as key:
                                    microsoft_pc_manager_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                            except FileNotFoundError:
                                pass

                                # %ProgramFiles%\WindowsApps, Drive:\Program Files\WindowsApps or Drive:\WindowsApps
                                if microsoft_pc_manager_version is None:
                                    try:
                                        import concurrent.futures
                                        from core.advanced_startup import AdvancedStartup
                                        from core.app_logger import AppLogger

                                        logger = AppLogger.get_logger()
                                        timeout_sec = 10 if (AdvancedStartup.is_devmode() or AdvancedStartup.is_debugmode()) else 5

                                        patterns = [
                                            "Microsoft.MicrosoftPCManager_*_*__8wekyb3d8bbwe",
                                            "Microsoft.MicrosoftPCManager_*_neutral_~_8wekyb3d8bbwe"
                                        ]

                                        def scan_job(path_to_check):
                                            try:
                                                if path_to_check.exists():
                                                    for pattern in patterns:
                                                        for app_dir in path_to_check.glob(pattern):
                                                            try:
                                                                return app_dir.name.split("_")[1]
                                                            except IndexError:
                                                                continue
                                            except Exception:
                                                pass
                                            return None

                                        search_paths = []
                                        # %ProgramFiles%\WindowsApps
                                        if os.environ.get("ProgramFiles"):
                                            search_paths.append(Path(os.environ["ProgramFiles"]) / "WindowsApps")

                                        # Drive:\Program Files\WindowsApps or Drive:\WindowsApps
                                        drives = [f"{chr(d)}:\\" for d in range(ord('A'), ord('Z') + 1)]
                                        for drive in drives:
                                            search_paths.append(Path(drive) / "Program Files" / "WindowsApps")
                                            search_paths.append(Path(drive) / "WindowsApps")

                                        # The maximum number of threads is 8, and in extreme cases, the maximum number of threads is 2.
                                        max_workers = min(8, os.cpu_count() or 2)
                                        logger.debug(f"ThreadPoolExecutor max_workers: {max_workers}")
                                        executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
                                        try:
                                            future_to_path = {executor.submit(scan_job, p): p for p in search_paths}
                                            
                                            for future in concurrent.futures.as_completed(future_to_path.keys(), timeout=timeout_sec):
                                                try:
                                                    ver = future.result()
                                                    if ver:
                                                        microsoft_pc_manager_version = ver
                                                        break
                                                except Exception:
                                                    pass
                                        except concurrent.futures.TimeoutError:
                                            incomplete_paths = [str(path) for future, path in future_to_path.items() if not future.done()]
                                            logger.warning(f"Scanning for Microsoft PC Manager version timed out (> {timeout_sec} s). Skipping Unreachable Paths: {', '.join(incomplete_paths)}")
                                        finally:
                                            executor.shutdown(wait=False)

                                    except Exception:
                                        pass

        return microsoft_pc_manager_version

    @staticmethod
    def get_microsoft_pc_manager_beta_version():
        microsoft_pc_manager_beta_version = None

        # Microsoft PC Manager Beta Setup
        if microsoft_pc_manager_beta_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\MSPCManager") as key:
                    microsoft_pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
            except FileNotFoundError:
                pass

            # Microsoft PC Manager Beta Uninstaller
            if microsoft_pc_manager_beta_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager") as key:
                        microsoft_pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                except FileNotFoundError:
                    pass

                # EXE File Properties
                if microsoft_pc_manager_beta_version is None:
                    try:
                        program_files_path = os.environ.get("ProgramFiles")
                        if program_files_path:
                            exe_path = Path(program_files_path) / "Microsoft PC Manager" / "MSPCManager.exe"
                            if exe_path.exists():
                                pe = pefile.PE(str(exe_path))
                                if hasattr(pe, "VS_FIXEDFILEINFO"):
                                    ver_info = pe.VS_FIXEDFILEINFO[0]
                                    ms = ver_info.FileVersionMS
                                    ls = ver_info.FileVersionLS
                                    microsoft_pc_manager_beta_version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                                pe.close()
                    except (FileNotFoundError, ImportError, Exception):
                        pass

        return microsoft_pc_manager_beta_version
