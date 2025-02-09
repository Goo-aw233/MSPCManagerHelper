import winreg

class CheckSystemRequirements:
    def __init__(self, translator):
        self.translator = translator

    def check_system_requirements(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                if int(current_build_number) < 19042:
                    return self.translator.translate("failure_to_meet_system_requirements")
                else:
                    return self.translator.translate("meet_system_requirements")
        except FileNotFoundError:
            return self.translator.translate("cannot_read_version")

    @staticmethod
    def check_system_build_number_and_admin_approval_mode():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                current_build_number = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
                if current_build_number < 27774:
                    return False

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System") as key:
                admin_approval_mode = int(winreg.QueryValueEx(key, "TypeOfAdminApprovalMode")[0])
                if admin_approval_mode == 2:
                    return True
        except FileNotFoundError:
            return False

        return False
