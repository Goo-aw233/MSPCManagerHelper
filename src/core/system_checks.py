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
    _suppressed = False

    @staticmethod
    def set_suppressed(value):
        PrerequisiteChecks._suppressed = value

    @staticmethod
    def check_admin_approval_mode():
        if PrerequisiteChecks._suppressed:
            return False
        try:
            # Check Windows Current Build Number
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as version_key:
                current_build_number = int(winreg.QueryValueEx(version_key, "CurrentBuildNumber")[0])
                # Launched in 27718/27764, added in 26120.4520, removed after br_release.
                if current_build_number < 26100:
                    return False

            # Check Administrator Protection Status
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System") as policy_key:
                admin_approval_mode = int(winreg.QueryValueEx(policy_key, "TypeOfAdminApprovalMode")[0])
                # Enabled
                if admin_approval_mode == 2:
                    return True
                # Disabled
                else:
                    return False
        except (FileNotFoundError, OSError, ValueError):
            return False

    @staticmethod
    def check_if_long_paths_enabled():
        if PrerequisiteChecks._suppressed:
            return True
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
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
        if PrerequisiteChecks._suppressed:
            return True
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
    def check_os_architecture():
        machine = platform.machine()
        if machine == "ARM64":
            return "ARM64"
        elif machine == "AMD64":
            return "x64"
        return machine

    @staticmethod
    def check_windows_minimum_requirements():
        try:
            # Check if Windows meets Microsoft PC Manager Minimum Requirements
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                # Meet Requirements
                if int(current_build_number) >= 19042:
                    return True
                # Does Not Meet Requirements
                else:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return None

    @staticmethod
    def check_windows_server_levels(check_type="is_windows_server_core"):
        """
        SUPPORTS PARAMETERS:

        1. `is_windows_server_core`: Checks if the Windows Server installation type is Core. (Default)
        2. `is_windows_server`: Checks if the Windows installation is any type of Windows Server (including both Server Core and Desktop Experience).

        --------------------------------------------------

        USAGE EXAMPLE (Using `is_windows_server_core` Has the Same Effect as Not Providing the Parameter):

        if PrerequisiteChecks.check_windows_server_levels(check_type="is_windows_server"):
            return True # Windows Server
        """
        if PrerequisiteChecks._suppressed:
            return False
        try:
            # Check if InstallationType is Server or Server Core
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as installation_type_key:
                installation_type = winreg.QueryValueEx(installation_type_key, "InstallationType")[0]

                if check_type == "is_windows_server":
                    return "Server" in installation_type

                # Server Core
                if "Server Core" in installation_type:
                    return True
                # Not Server
                if installation_type != "Server":
                    return False

            # Check if ClientExperienceEnabled Exists
            # (Secondary Confirmation if Installation Type is Desktop Experience)
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Server") as client_experience_enabled_key:
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
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
                edition_id = winreg.QueryValueEx(key, "EditionID")[0]
                build_lab_ex = winreg.QueryValueEx(key, "BuildLabEx")[0]

                """
                try:
                    lcu_ver = winreg.QueryValueEx(key, "LCUVer")[0]
                    if lcu_ver:
                        return f"Microsoft Windows {display_version} {lcu_ver} {edition_id}\n{build_lab_ex}"
                except OSError:
                    pass
                """

                major_version = winreg.QueryValueEx(key, "CurrentMajorVersionNumber")[0]
                minor_version = winreg.QueryValueEx(key, "CurrentMinorVersionNumber")[0]
                build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                ubr = winreg.QueryValueEx(key, "UBR")[0]

                # Get Windows Feature Experience Pack Version
                windows_feature_experience_pack = None
                try:
                    manifest_path = Path(os.getenv(
                                             "SystemRoot", r"C:\Windows")) / "SystemApps" / "MicrosoftWindows.Client.CBS_cw5n1h2txyewy" / "appxmanifest.xml"
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Use a regular expression to find the format ` Version="..." `,
                    # ensuring there are spaces before and after.
                    match = re.search(r' Version="([^"]*)" ', content)
                    if match:
                        windows_feature_experience_pack = match.group(1)
                except (FileNotFoundError, OSError):
                    pass

                if windows_feature_experience_pack:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}\n{PrerequisiteChecks.app_translator.translate('core.windows_feature_experience_pack')} {windows_feature_experience_pack}"
                else:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}"
        except (FileNotFoundError, OSError):
            return None

class OptionalChecks:
    _suppressed = False
    logger = AppLogger.get_logger()

    @staticmethod
    def set_suppressed(value):
        OptionalChecks._suppressed = value

    DEFAULT_UTILITIES = [
        "cmd.exe", "Dism.exe", "powershell.exe", "reg.exe",
        "sc.exe", "sfc.exe", "taskkill.exe"
    ]

    @staticmethod
    def check_narrator_status():
        """
        SPI_GETSCREENREADER:
        https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-systemparametersinfow
        """
        if OptionalChecks._suppressed:
            return False
        try:
            # Use System Accessibility State
            screen_reader_running = wintypes.BOOL()
            success = ctypes.windll.user32.SystemParametersInfoW(
                0x0046,
                0,
                ctypes.byref(screen_reader_running),
                0
            )

            if success and bool(screen_reader_running.value):
                return True

            # Fallback: detect Narrator by process name for apps that do not set SPI state.
            class PROCESSENTRY32W(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", ctypes.c_wchar * 260)
                ]

            # TH32CS_SNAPPROCESS = 0x00000002
            h_process_snap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
            if h_process_snap == -1:
                return False

            pe32 = PROCESSENTRY32W()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32W)

            if not ctypes.windll.kernel32.Process32FirstW(h_process_snap, ctypes.byref(pe32)):
                ctypes.windll.kernel32.CloseHandle(h_process_snap)
                return False

            screen_reader_targets = ("jfw", "narrator", "nvda", "zit")

            while True:
                exe_file = pe32.szExeFile.lower()
                if any(target in exe_file for target in screen_reader_targets):
                    ctypes.windll.kernel32.CloseHandle(h_process_snap)
                    return True
                if not ctypes.windll.kernel32.Process32NextW(h_process_snap, ctypes.byref(pe32)):
                    break

            ctypes.windll.kernel32.CloseHandle(h_process_snap)
            return False
        except Exception:
            return False

    @staticmethod
    def check_windows_utilities_availability(target_utility=None, suppress_complete_log=False):
        if OptionalChecks._suppressed:
            return True

        # List of Utilities to Check
        if target_utility:
            if isinstance(target_utility, str):
                # Supports Separating with Commas or Spaces
                utilities = [u.strip() for u in re.split(r"[,\s]+", target_utility) if u.strip()]
            elif isinstance(target_utility, (list, tuple)):
                utilities = list(target_utility)
            else:
                utilities = [str(target_utility)]
            """
            Use `target_utility=["Name1", "Name2", "..."]` to check specific utilities or exes (not limited to default list).
            USAGE EXAMPLE:

            if OptionalChecks.check_windows_utilities_availability(target_utility=["cmd.exe", "Dism.exe"]):
                return True # cmd.exe & Dism.exe is Available
            else:
                return False # cmd.exe & Dism.exe is Not Available
            """
        else:
            # Default List of Utilities
            utilities = OptionalChecks.DEFAULT_UTILITIES
        found_utilities = {}
        all_checks_passed = True

        # Find Utilities (Including PATH Search)
        for utility in utilities:
            path = shutil.which(utility)
            if path:
                found_utilities[utility] = path
            else:
                OptionalChecks.logger.warning(f"Utility Not Found: {utility}")
                all_checks_passed = False

        if not found_utilities:
            OptionalChecks.logger.error("No utilities found.")
            return False

        # Check Availability
        # Ignored Not Found Utilities
        for utility, path in found_utilities.items():
            try:
                is_text = utility not in {"sfc.exe"}

                result = subprocess.run([path, "/?"], text=is_text, shell=False, capture_output=True,
                                        creationflags=subprocess.CREATE_NO_WINDOW, timeout=5.0)

                if not result.stdout and not result.stderr:
                    OptionalChecks.logger.warning(f"Utility {utility} is not available (empty output).")
                    all_checks_passed = False
            except subprocess.TimeoutExpired:
                OptionalChecks.logger.warning(f"Utility {utility} check TIMED OUT (likely hung or corrupted).")
                all_checks_passed = False
            except Exception as e:
                OptionalChecks.logger.warning(f"Utility {utility} Check Failed: {e}")
                all_checks_passed = False

        if all_checks_passed and not suppress_complete_log:
            """
            Use `suppress_complete_log=True` to suppress the "All utilities availability check completed. No issues found." log message.
            USAGE EXAMPLE:
            if OptionalChecks.check_windows_utilities_availability(suppress_complete_log=True):
                return True # All utilities are available, but no log message will be shown.
            """
            OptionalChecks.logger.info("All utilities availability check completed. No issues found.")
        return all_checks_passed

    @staticmethod
    def check_windows_utilities_version():
        if OptionalChecks._suppressed:
            return {}
        utilities_versions = {}

        for utility in OptionalChecks.DEFAULT_UTILITIES:
            path = shutil.which(utility)
            if path:
                try:
                    pe = pefile.PE(path)
                    try:
                        if hasattr(pe, "VS_FIXEDFILEINFO"):
                            ver_info = pe.VS_FIXEDFILEINFO[0]
                            ms = ver_info.FileVersionMS
                            ls = ver_info.FileVersionLS
                            version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                            utilities_versions[utility] = version
                    finally:
                        pe.close()
                except Exception as e:
                    OptionalChecks.logger.warning(f"Failed to Get Version for {utility}: {e}")
            else:
                OptionalChecks.logger.warning(f"Utility Not Found for Version Check: {utility}")

        if utilities_versions:
            formatted = "\n".join(
                f"    {k.ljust(15)}: {v}" for k, v in utilities_versions.items()
            )
            OptionalChecks.logger.info(f"Windows Utilities Versions:\n{formatted}")

        return utilities_versions
