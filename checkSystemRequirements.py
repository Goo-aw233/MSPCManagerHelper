import winreg
from Translator import Translator

def check_system_requirements(locale):
    translator = Translator(locale)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
            current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
            if int(current_build_number) < 19042:
                return translator.translate("version_check")
            else:
                return translator.translate("system_requirements_met")
    except FileNotFoundError:
        return translator.translate("cannot_read_version")
