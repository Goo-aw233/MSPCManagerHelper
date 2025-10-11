import winreg


class CheckSystemRequirements:
    _WINDOWS_NT_CURRENT_VERSION_KEY_PATH = r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"

    @staticmethod
    def check_admin_approval_mode():
        try:
            # Checking the Windows Current Build Number
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as version_key:
                current_build_number = int(winreg.QueryValueEx(version_key, "CurrentBuildNumber")[0])
                if current_build_number < 26100:    # Launched in 27718/27764, Added in 26120.4520, Removed After br_release
                    return False

            # Checking the Administrator Protection Status
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System") as policy_key:
                admin_approval_mode = int(winreg.QueryValueEx(policy_key, "TypeOfAdminApprovalMode")[0])
                # Administrator Protection is Enabled
                if admin_approval_mode == 2:
                    return True
                # Administrator Protection is Disabled
                else:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return False

    @staticmethod
    def check_windows_server_levels():
        try:
            # Check If the InstallationType is Server or Server Core
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as installation_type_key:
                installation_type = winreg.QueryValueEx(installation_type_key, "InstallationType")[0]
                # Error If Server Core
                if "Server Core" in installation_type:
                    return True
                # Skip If Server
                if installation_type != "Server":
                    return False

            # Check If ClientExperienceEnabled is Present (Installation Type is Desktop Experience, Secondary Confirmation)
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
            # Check If the System Meets the Microsoft PC Manager Minimum Requirements
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as key:
                current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                # Meet the Requirements
                if int(current_build_number) >= 19042:
                    return True
                # Not Meet the Requirements
                else:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return None

    @staticmethod
    def get_windows_installation_information():
        try:
            # Open the Registry Key for the Windows Version
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CheckSystemRequirements._WINDOWS_NT_CURRENT_VERSION_KEY_PATH) as key:
                # Read the Version Numbers And Other Information
                edition_id = winreg.QueryValueEx(key, "EditionID")[0]
                build_lab_ex = winreg.QueryValueEx(key, "BuildLabEx")[0]

                try:
                    # Try to Read LCUVer
                    lcu_ver = winreg.QueryValueEx(key, "LCUVer")[0]
                    # If LCUVer Exists, Use It
                    if lcu_ver:
                        return f"Microsoft Windows {lcu_ver} {edition_id}\n{build_lab_ex}"
                except OSError:
                    # LCUVer Does Not Exist, Continue to Manually Splice
                    pass

                major_version = winreg.QueryValueEx(key, "CurrentMajorVersionNumber")[0]
                minor_version = winreg.QueryValueEx(key, "CurrentMinorVersionNumber")[0]
                build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                ubr = winreg.QueryValueEx(key, "UBR")[0]
                # Return the Formatted Version String
                return f"Microsoft Windows {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}"
        except (FileNotFoundError, OSError):
            # An Error Occurred While Reading the Registry
            return None
