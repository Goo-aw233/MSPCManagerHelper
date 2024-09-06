import winreg
from translator import Translator

def check_system_requirements(locale):
    translator = Translator(locale)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
            current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
            if int(current_build_number) < 19042:
                return translator.translate("failure_to_meet_system_requirements")
            else:
                return translator.translate("meet_system_requirements")
    except FileNotFoundError:
        return translator.translate("cannot_read_version")
