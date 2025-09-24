import shutil

class UtilsAvailabilityCheck:
    @staticmethod
    def check_windows_utilities_availability():
        exe_names = ["cmd.exe", "powershell.exe", "reg.exe"]
        results = {name: shutil.which(name) for name in exe_names}
        available = [name for name, path in results.items() if path]
        unavailable = [name for name, path in results.items() if not path]
        if len(available) == len(exe_names):
            return True, []
        elif available:
            return False, unavailable
        else:
            return None, exe_names
