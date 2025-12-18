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
        devmode_args = ["/devmode", "-devmode", "--devmode"]
        return any(arg.lower() in devmode_args for arg in sys.argv)

    @staticmethod
    def is_debugmode():
        debugmode_args = ["/debugmode", "-debugmode", "--debugmode"]
        return any(arg.lower() in debugmode_args for arg in sys.argv)

    @staticmethod
    def get_runtime_arguments():
        # Return argument list (excluding the program itself).
        return sys.argv[1:].copy()

    @staticmethod
    def format_runtime_arguments(args=None):
        # Format args into a shell argument string, adapting arguments with spaces (by adding quotes).
        args = args if args is not None else AdvancedStartup.get_runtime_arguments()
        return " ".join(f'"{a}"' if " " in a else a for a in args)

    @staticmethod
    def run_as_administrator(args):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 0)
        if result > 32:
            sys.exit(0)
