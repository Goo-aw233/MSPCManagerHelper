import ctypes
import sys


class AdvancedStartup:
    @staticmethod
    def is_administrator():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except (AttributeError, OSError):
            return 0

    @staticmethod
    def is_devmode():
        devmode_args = ['/devmode', '-devmode']
        return any(arg.lower() in devmode_args for arg in sys.argv)

    @staticmethod
    def run_as_administrator(params):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 0)
        if result > 32:
            sys.exit()
