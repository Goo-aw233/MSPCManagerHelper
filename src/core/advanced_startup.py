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

    @staticmethod
    def is_bypass_checks():
        bypass_checks_args = ["/bypasschecks", "-bypasschecks", "--bypasschecks"]
        return any(arg.lower() in bypass_checks_args for arg in sys.argv)

    @staticmethod
    def is_open_help_window():
        open_help_window_args = ["/?", "-?", "--?", "/h", "-h", "--h", "/help", "-help", "--help"]
        return any(arg.lower() in open_help_window_args for arg in sys.argv)

    @staticmethod
    def get_runtime_arguments():
        # Excluding the program itself.
        return sys.argv[1:].copy()

    @staticmethod
    def run_as_administrator(args):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 0)
        if result > 32:
            sys.exit(0)
