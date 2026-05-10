import ctypes
import sys

from .app_translator import AppTranslator


class AdvancedStartup:
    PREFIXES = ("/", "-", "--")

    # === Argument Building ===
    @staticmethod
    def _build_flag_args(name):
        return [f"{prefix}{name}" for prefix in AdvancedStartup.PREFIXES]

    @staticmethod
    def _build_kv_prefixes(name, separators=("=",)):
        return [f"{prefix}{name}{sep}" for prefix in AdvancedStartup.PREFIXES for sep in separators]
    # === End of Argument Building ===

    # === Runtime Arguments ===
    @staticmethod
    def get_specified_locale_argument():
        locale_args = AdvancedStartup._build_kv_prefixes("locale", separators=("=", ":"))
        for arg in sys.argv:
            lowered_arg = arg.lower()
            for prefix in locale_args:
                if lowered_arg.startswith(prefix):
                    raw_locale = arg[len(prefix):].strip().strip("\"")
                    return raw_locale.lower()
        return None

    @staticmethod
    def is_bypass_checks():
        bypass_checks_args = AdvancedStartup._build_flag_args("bypasschecks")
        return any(arg.lower() in bypass_checks_args for arg in sys.argv)

    @staticmethod
    def is_debugmode():
        debugmode_args = AdvancedStartup._build_flag_args("debugmode")
        return any(arg.lower() in debugmode_args for arg in sys.argv)

    @staticmethod
    def is_devmode():
        devmode_args = AdvancedStartup._build_flag_args("devmode")
        return any(arg.lower() in devmode_args for arg in sys.argv)

    @staticmethod
    def is_open_help_window():
        open_help_window_args = (
            AdvancedStartup._build_flag_args("?")
            + AdvancedStartup._build_flag_args("h")
            + AdvancedStartup._build_flag_args("help")
        )
        return any(arg.lower() in open_help_window_args for arg in sys.argv)
    # === End of Runtime Arguments ===

    # === Runtime Actions ===
    @staticmethod
    def get_runtime_arguments():
        # Excluding the program itself.
        return sys.argv[1:].copy()

    @staticmethod
    def is_administrator():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except (AttributeError, OSError):
            return False

    @staticmethod
    def run_as_administrator(args):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 0)
        if result > 32:
            sys.exit(0)

    @staticmethod
    def specify_locale():
        candidate = AdvancedStartup.get_specified_locale_argument()
        if AppTranslator.is_supported_locale(candidate):
            return candidate
        return None
    # === End of Runtime Actions ===
