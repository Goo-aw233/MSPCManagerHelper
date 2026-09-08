import ctypes
import os
import sys
from pathlib import Path

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

    @staticmethod
    def is_runas():
        runas_args = AdvancedStartup._build_flag_args("runas")
        return any(arg.lower() in runas_args for arg in sys.argv)

    @staticmethod
    def remove_runas_argument(args):
        """Drop the runas flag from a list of arguments.
        Used when relaunching elevated so the new instance
        does not relaunch itself again.
        """
        runas_args = AdvancedStartup._build_flag_args("runas")
        return [arg for arg in args if arg.lower() not in runas_args]
    # === End of Runtime Arguments ===

    # === Runtime Actions ===
    @staticmethod
    def get_runtime_arguments():
        # Excluding the program itself. Drop a leading token that equals the
        # executable path, which may otherwise leak into argv[1:] after a
        # relaunch and accumulate across restarts.
        args = sys.argv[1:].copy()
        if args:
            try:
                if Path(args[0]).resolve() == Path(sys.executable).resolve():
                    args.pop(0)
            except OSError:
                pass
        return args

    @staticmethod
    def is_administrator():
        """Use CheckTokenMembership to check whether the program has an access token.
        1. In Bypass Checks, is_administrator() will always be True, but it does not have administrator privileges.
           At this time, /runas /bypasschecks will ignore the elevation request.

        Ref:
            https://learn.microsoft.com/windows/win32/api/securitybaseapi/nf-securitybaseapi-checktokenmembership
        """
        if AdvancedStartup.is_bypass_checks():
            return True
        try:
            sid = ctypes.c_void_p()
            ret = ctypes.windll.advapi32.ConvertStringSidToSidW(
                ctypes.c_wchar_p("S-1-5-32-544"),
                ctypes.byref(sid),
            )
            if not ret:
                return False

            try:
                is_member = ctypes.wintypes.BOOL()
                ret = ctypes.windll.advapi32.CheckTokenMembership(
                    None,  # NULL represents the access token of the current thread/process. 
                    sid,
                    ctypes.byref(is_member),
                )
                return bool(is_member.value) if ret else False
            finally:
                ctypes.windll.kernel32.LocalFree(sid)
        except (AttributeError, OSError):
            return False

    @staticmethod
    def execute_restart(args, verb=None):
        # A new instance spawned via sys.executable reuses this process's onefile
        # temp folder (_MEIxxxx), which is deleted on exit. Force an independent
        # instance so it extracts its own folder.
        # Ref: https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html
        if hasattr(sys, "_MEIPASS"):
            os.environ["PYINSTALLER_RESET_ENVIRONMENT"] = "1"

        # Low-level restart: ask the shell to start a new instance and return
        # the raw ShellExecuteW result code. Whether the current process should
        # exit is decided by the higher-level caller, since a successful restart
        # spawns a new instance that takes over.
        return ctypes.windll.shell32.ShellExecuteW(None, verb, sys.executable, args, None, 0)

    @staticmethod
    def specify_locale():
        candidate = AdvancedStartup.get_specified_locale_argument()
        if AppTranslator.is_supported_locale(candidate):
            return candidate
        return None
    # === End of Runtime Actions ===
