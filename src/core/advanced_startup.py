import ctypes
import sys


class AdvancedStartup:
    @staticmethod
    def is_administrator():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except (AttributeError, OSError):
            return False

    @staticmethod
    def is_devmode():
        devmode_args = ["/devmode", "-devmode", "--devmode"]
        return any(arg.lower() in devmode_args for arg in sys.argv)

    @staticmethod
    def is_debugmode():
        debugmode_args = ["/debugmode", "-debugmode", "--debugmode"]
        return any(arg.lower() in debugmode_args for arg in sys.argv)
