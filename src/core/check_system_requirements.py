import os
import platform
import re
import sys
import winreg
from pathlib import Path


class CheckSystemRequirements:
    _WINDOWS_NT_CURRENT_VERSION_KEY_PATH = r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
    translator = None

    @staticmethod
    def check_admin_approval_mode():
        try:
            # Check the Windows current build number.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as version_key:
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
        except (FileNotFoundError, ValueError, OSError):
            return False

    @staticmethod
    def check_windows_server_levels():
        try:
            # Check if the InstallationType is Server or Server Core.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as installation_type_key:
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
        except (ValueError, OSError):
            return False

    @staticmethod
    def check_system_minimum_requirements():
        try:
            # Check if the Windows meets the Microsoft PC Manager minimum requirements.
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as key:
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
                    manifest_path = Path(os.environ["SystemRoot"]) / "SystemApps" / "MicrosoftWindows.Client.CBS_cw5n1h2txyewy" / "appxmanifest.xml"
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Use a regular expression to find the format ` Version="..." `, ensuring there are spaces before and after.
                    match = re.search(r' Version="([^"]*)" ', content)
                    if match:
                        windows_feature_experience_pack = match.group(1)
                except (FileNotFoundError, OSError):
                    pass

                if windows_feature_experience_pack:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}\n{CheckSystemRequirements.translator.translate('windows_feature_experience_pack')}: {windows_feature_experience_pack}"
                else:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}"
        except (FileNotFoundError, OSError):
            return None

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
        return None
