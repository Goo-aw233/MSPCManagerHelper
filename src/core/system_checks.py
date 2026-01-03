import ctypes
import os
import platform
import re
import shutil
import subprocess
import sys
import winreg
from ctypes import wintypes
from pathlib import Path

import pefile

from core.app_logger import AppLogger


class PrerequisiteChecks:
    app_translator = None

    @staticmethod
    def check_admin_approval_mode():
        try:
            # Check the Windows current build number.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as version_key:
                current_build_number = int(winreg.QueryValueEx(version_key, "CurrentBuildNumber")[0])
                # Launched in 27718/27764, added in 26120.4520, removed after br_release.
                if current_build_number < 26100:
                    return False

            # Check the Administrator Protection status.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System") as policy_key:
                admin_approval_mode = int(winreg.QueryValueEx(policy_key, "TypeOfAdminApprovalMode")[0])
                # Administrator Protection is enabled.
                if admin_approval_mode == 2:
                    return True
                # Administrator Protection is disabled.
                else:
                    return False
        except (FileNotFoundError, OSError, ValueError):
            return False

    @staticmethod
    def check_if_long_paths_enabled():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SYSTEM\\CurrentControlSet\\Control\\FileSystem") as key:
                long_paths_enabled = int(winreg.QueryValueEx(key, "LongPathsEnabled")[0])
                # Enabled
                if long_paths_enabled == 1:
                    return True
                # Disabled or Unknown
                else:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return False

    @staticmethod
    def check_if_windows_nt():
        check_uname = [
            os.name == "nt",
            platform.system() == "Windows",
            platform.release() == "NT",
            sys.platform.startswith("win"),
            os.environ.get("OS") == "Windows_NT",
            hasattr(sys, "getwindowsversion")
        ]

        if any(check_uname):
            return True
        return False

    @staticmethod
    def check_windows_minimum_requirements():
        try:
            # Check if the Windows meets the Microsoft PC Manager minimum requirements.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                # Meet the requirements.
                if int(current_build_number) >= 19042:
                    return True
                # Not meet the requirements.
                else:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return None

    @staticmethod
    def check_windows_server_levels():
        try:
            # Check if the InstallationType is Server or Server Core.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as installation_type_key:
                installation_type = winreg.QueryValueEx(installation_type_key, "InstallationType")[0]
                # An error will be reported if it is Server Core.
                if "Server Core" in installation_type:
                    return True
                # Skip if it is not Server.
                if installation_type != "Server":
                    return False

            # Check if ClientExperienceEnabled exists. (Secondary confirmation if Installation Type is Desktop Experience.)
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Server") as client_experience_enabled_key:
                    winreg.QueryValueEx(client_experience_enabled_key, "ClientExperienceEnabled")
                    # Desktop Experience
                    return False
            # Server Core
            except FileNotFoundError:
                return True
        # Desktop Experience
        except (OSError, ValueError):
            return False

    @staticmethod
    def get_windows_installation_information():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
                edition_id = winreg.QueryValueEx(key, "EditionID")[0]
                build_lab_ex = winreg.QueryValueEx(key, "BuildLabEx")[0]

                """
                try:
                    lcu_ver = winreg.QueryValueEx(key, "LCUVer")[0]
                    if lcu_ver:
                        return f"Microsoft Windows {display_version} {lcu_ver} {edition_id}\n{build_lab_ex}"
                except OSError:
                    # LCUVer not exists, reading other version information from the registry.
                    pass
                """

                major_version = winreg.QueryValueEx(key, "CurrentMajorVersionNumber")[0]
                minor_version = winreg.QueryValueEx(key, "CurrentMinorVersionNumber")[0]
                build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                ubr = winreg.QueryValueEx(key, "UBR")[0]

                # Get Windows Feature Experience Pack version.
                windows_feature_experience_pack = None
                try:
                    manifest_path = Path(os.environ[
                                             "SystemRoot"]) / "SystemApps" / "MicrosoftWindows.Client.CBS_cw5n1h2txyewy" / "appxmanifest.xml"
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Use a regular expression to find the format ` Version="..." `, ensuring there are spaces before and after.
                    match = re.search(r' Version="([^"]*)" ', content)
                    if match:
                        windows_feature_experience_pack = match.group(1)
                except (FileNotFoundError, OSError):
                    pass

                if windows_feature_experience_pack:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}\n{PrerequisiteChecks.app_translator.translate('windows_feature_experience_pack')} {windows_feature_experience_pack}"
                else:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}"
        except (FileNotFoundError, OSError):
            return None

class OptionalChecks:
    logger = AppLogger.get_logger()

    @staticmethod
    def check_narrator_status():
        try:
            # Define the structure for PROCESSENTRY32.
            class PROCESSENTRY32(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", ctypes.c_char * 260)
                ]

            # Create a snapshot of the current processes.
            # TH32CS_SNAPPROCESS = 0x00000002
            hProcessSnap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
            if hProcessSnap == -1:
                return False

            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

            # Retrieve information about the first process.
            if not ctypes.windll.kernel32.Process32First(hProcessSnap, ctypes.byref(pe32)):
                ctypes.windll.kernel32.CloseHandle(hProcessSnap)
                return False

            # Iterate through the processes.
            while True:
                exe_file = pe32.szExeFile.decode('utf-8', errors='ignore')
                if "narrator" in exe_file.lower():
                    ctypes.windll.kernel32.CloseHandle(hProcessSnap)
                    return True
                if not ctypes.windll.kernel32.Process32Next(hProcessSnap, ctypes.byref(pe32)):
                    break

            ctypes.windll.kernel32.CloseHandle(hProcessSnap)
            return False
        except Exception:
            return False

    @staticmethod
    def check_windows_utilities_availability():
        utilities = ["cmd.exe", "Dism.exe", "powershell.exe", "reg.exe", "sc.exe", "sfc.exe", "where.exe"]
        found_utilities = {}
        all_checks_passed = True

        # Find Utilities (Including PATH Search)
        for utility in utilities:
            path = shutil.which(utility)
            if path:
                found_utilities[utility] = path
            else:
                OptionalChecks.logger.warning(f"Utility not found: {utility}")
                all_checks_passed = False

        if not found_utilities:
            OptionalChecks.logger.error("No utilities found.")
            return False

        # Check Availability
        # Others utilities are text-based, there are only a few byte-based utilities.
        byte_based_utilities = ["sfc.exe"]

        # Ignored not found utilities.
        for utility, path in found_utilities.items():
            try:
                is_byte_based = utility in byte_based_utilities
                
                if is_byte_based:
                    result = subprocess.run([path, "/?"], capture_output=True, text=False, shell=False,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
                    if result.stdout == b"" and result.stderr == b"":
                        OptionalChecks.logger.warning(f"Utility {utility} is not available (empty output).")
                        all_checks_passed = False
                else:
                    result = subprocess.run([path, "/?"], capture_output=True, text=True, shell=False,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
                    if not result.stdout and not result.stderr:
                        OptionalChecks.logger.warning(f"Utility {utility} is not available (empty output).")
                        all_checks_passed = False
            except Exception as e:
                OptionalChecks.logger.warning(f"Utility {utility} Check Failed: {e}")
                all_checks_passed = False

        if all_checks_passed:
            OptionalChecks.logger.info("All utilities availability check completed. No issues found.")
        return all_checks_passed

    @staticmethod
    def check_windows_utilities_version():
        utilities = ["cmd.exe", "Dism.exe", "powershell.exe", "reg.exe", "sc.exe", "sfc.exe", "where.exe"]
        utilities_versions = {}

        for utility in utilities:
            path = shutil.which(utility)
            if path:
                try:
                    pe = pefile.PE(path)
                    if hasattr(pe, "VS_FIXEDFILEINFO"):
                        ver_info = pe.VS_FIXEDFILEINFO[0]
                        ms = ver_info.FileVersionMS
                        ls = ver_info.FileVersionLS
                        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                        utilities_versions[utility] = version
                    pe.close()
                except (FileNotFoundError, ImportError, Exception) as e:
                    OptionalChecks.logger.warning(f"Failed to Get Version for {utility}: {e}")
            else:
                OptionalChecks.logger.warning(f"Utility Not Found for Version Check: {utility}")

        if utilities_versions:
            formatted = "\n".join(
                f"    {k.ljust(15)}: {v}" for k, v in utilities_versions.items()
            )
            OptionalChecks.logger.info(f"Windows Utilities Versions:\n{formatted}")

        return utilities_versions
