import os
import subprocess
import sys

import darkdetect
import pywinstyles
import sv_ttk

from core.program_logger import ProgramLogger
from core.set_font_family import SetFontFamily


class ProgramSettings:
    logger = ProgramLogger.get_logger()

    _THEME_MODE: str = "auto"
    _MS_STUDENT_AMBASSADOR_CID_DEFAULT: str = "/?wt.mc_id=studentamb_474966"
    _is_support_developer_enabled: bool = True
    _is_compatibility_mode_enabled: bool = False
    _is_follow_system_font_enabled: bool = False
    _cleanup_after_exit_enabled: bool = False

    # ======================= JIT Settings =======================
    @classmethod
    def is_jit_enabled(cls) -> bool:
        try:
            jit = getattr(sys, "_jit", None)
            is_enabled = getattr(jit, "is_enabled", None)
            return bool(jit and callable(is_enabled) and is_enabled())
        except Exception as e:
            ProgramSettings.logger.warning(f"Failed to Check JIT Status: {e}")
            return False

    @classmethod
    def enable_jit_and_exit(cls, is_admin: bool) -> None:
        cmd = ["setx.exe", "/M", "PYTHON_JIT", "1"] if is_admin else ["setx.exe", "PYTHON_JIT", "1"]
        target_scope = "System" if is_admin else "User"

        try:
            result = subprocess.run(
                cmd,
                check=True,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                shell=False
            )
            ProgramSettings.logger.info(f"Enabled JIT via {target_scope} environment variable. Return code: {result.returncode}. Stdout: {result.stdout}.")
        except Exception as e:
            ProgramSettings.logger.error(f"Failed to Enable JIT ({target_scope} Scope): {e}")
        sys.exit(0)

    @staticmethod
    def enable_jit_in_subprocess() -> None:
        try:
            os.environ["PYTHON_JIT"] = "1"
            ProgramSettings.logger.info(f"Enabled JIT Compilation in current subprocess environment.")
        except Exception as e:
            ProgramSettings.logger.warning(f"Failed to Enable JIT Compilation in Subprocess: {e}")
    # ======================= End of JIT Settings =======================

    # ======================= Theme Mode Settings =======================
    @classmethod
    def get_theme_mode(cls) -> str:
        return cls._THEME_MODE

    @classmethod
    def set_theme_mode(cls, mode: str) -> None:
        if mode not in ("auto", "light", "dark"):
            raise ValueError("Invalid theme mode. Use 'auto', 'light' or 'dark'.")
        cls._THEME_MODE = mode

    @classmethod
    def apply_theme(cls, window=None) -> None:
        try:
            if cls._THEME_MODE == "auto":
                theme = darkdetect.theme()
                if theme == "Light":
                    sv_ttk.set_theme("light")
                    ProgramSettings.logger.info("System theme is Light, setting theme to light.")
                    if window:
                        pywinstyles.apply_style(window, "light")
                else:
                    sv_ttk.set_theme("dark")
                    ProgramSettings.logger.info("System theme is Dark, setting theme to dark.")
                    if window:
                        pywinstyles.apply_style(window, "dark")
            elif cls._THEME_MODE == "light":
                sv_ttk.set_theme("light")
                ProgramSettings.logger.info("Forced theme to light.")
                if window:
                    pywinstyles.apply_style(window, "light")
            else:
                sv_ttk.set_theme("dark")
                ProgramSettings.logger.info("Forced theme to dark.")
                if window:
                    pywinstyles.apply_style(window, "dark")
        except Exception as e:
            ProgramSettings.logger.warning(f"Failed to Apply Theme: {e}")
    # ======================= End of Theme Mode Settings =======================

    # ======================= Support Developer Mode Settings =======================
    @classmethod
    def is_support_developer_enabled(cls) -> bool:
        return cls._is_support_developer_enabled

    @classmethod
    def set_support_developer_enabled(cls, enabled: bool) -> None:
        cls._is_support_developer_enabled = bool(enabled)

    @classmethod
    def toggle_support_developer(cls) -> None:
        cls.set_support_developer_enabled(not cls._is_support_developer_enabled)

    @classmethod
    def get_ms_student_ambassador_cid(cls) -> str:
        return cls._MS_STUDENT_AMBASSADOR_CID_DEFAULT if cls._is_support_developer_enabled else ""
    # ======================= End of Support Developer Mode Settings =======================

    # ======================= Compatibility Mode Settings =======================
    @classmethod
    def is_compatibility_mode_enabled(cls) -> bool:
        return cls._is_compatibility_mode_enabled

    @classmethod
    def set_compatibility_mode_enabled(cls, enabled: bool) -> None:
        cls._is_compatibility_mode_enabled = bool(enabled)

    @classmethod
    def toggle_compatibility_mode(cls) -> None:
        cls.set_compatibility_mode_enabled(not cls._is_compatibility_mode_enabled)
    # ======================= End of Compatibility Mode Settings =======================

    # ======================= Follow System Font Settings =======================
    @classmethod
    def is_follow_system_font_enabled(cls) -> bool:
        return cls._is_follow_system_font_enabled

    @classmethod
    def set_follow_system_font_enabled(cls, enabled: bool) -> None:
        cls._is_follow_system_font_enabled = bool(enabled)
        ProgramSettings.logger.info(f"Follow System Font Set to: {enabled}")
        SetFontFamily.apply_font_setting(follow_system_font=enabled)

    @classmethod
    def toggle_follow_system_font(cls) -> None:
        cls.set_follow_system_font_enabled(not cls._is_follow_system_font_enabled)
    # ======================= End of Follow System Font Settings =======================

    # ======================= Cleanup After Exit Settings =======================
    @classmethod
    def is_cleanup_after_exit_enabled(cls) -> bool:
        return cls._cleanup_after_exit_enabled

    @classmethod
    def set_cleanup_after_exit_enabled(cls, enabled: bool) -> None:
        cls._cleanup_after_exit_enabled = bool(enabled)

    @classmethod
    def toggle_cleanup_after_exit(cls) -> None:
        cls.set_cleanup_after_exit_enabled(not cls._cleanup_after_exit_enabled)
    # ======================= End of Cleanup After Exit Settings =======================