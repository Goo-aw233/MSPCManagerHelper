import os
import subprocess
import sys
from typing import Sequence

import customtkinter
import darkdetect

from core.program_logger import ProgramLogger


class ProgramSettings:
    logger = ProgramLogger.get_logger()

    _THEME_MODE: str = "auto"
    _EFFECTIVE_THEME_MODE: str = "auto"
    _SUPPORTED_LANGUAGES = ("en-us", "zh-cn", "zh-tw")
    _LANGUAGE: str | None = None
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

    # ======================= Theme Settings =======================
    @classmethod
    def get_theme_mode(cls) -> str:
        return cls._THEME_MODE

    @classmethod
    def get_effective_theme_mode(cls) -> str:
        return cls._EFFECTIVE_THEME_MODE

    @classmethod
    def set_theme_mode(cls, mode: str) -> None:
        normalized = str(mode).lower() if mode else "auto"
        if normalized in ("auto", "system"):
            normalized = "auto"
            ctk_mode = "System"
        elif normalized == "light":
            ctk_mode = "Light"
        elif normalized == "dark":
            ctk_mode = "Dark"
        else:
            cls.logger.warning(f"Invalid appearance mode '{mode}' provided. Falling back to 'auto'.")
            normalized = "auto"
            ctk_mode = "System"

        cls._THEME_MODE = normalized
        try:
            customtkinter.set_appearance_mode(ctk_mode)
            cls._EFFECTIVE_THEME_MODE = cls._resolve_effective_mode(ctk_mode)
            cls.logger.info(f"Applied Appearance Mode: {normalized} (Effective={cls._EFFECTIVE_THEME_MODE})")
        except Exception as e:
            cls.logger.error(f"Failed to Apply Appearance Mode '{mode}': {e}")

    @classmethod
    def _resolve_effective_mode(cls, ctk_mode: str) -> str:
        try:
            # CustomTkinter may report "System"; map it using darkdetect so dependent UI can pick correct palette.
            if str(ctk_mode).lower() == "system":
                return "dark" if darkdetect.isDark() else "light"
            lowered = str(ctk_mode).lower()
            return "dark" if lowered == "dark" else "light"
        except Exception as e:
            cls.logger.warning(f"Failed to Resolve Effective Appearance Mode from '{ctk_mode}': {e}")
            return "light"
    # ======================= End of Theme Settings =======================

    # ======================= Language Settings =======================
    @classmethod
    def get_supported_languages(cls) -> tuple[str, ...]:
        return cls._SUPPORTED_LANGUAGES

    @classmethod
    def get_language(cls) -> str | None:
        return cls._LANGUAGE

    @classmethod
    def set_language(cls, language: str | None) -> None:
        if not language:
            cls._LANGUAGE = None
            return

        normalized = str(language).lower()
        if normalized == cls._LANGUAGE:
            return

        if normalized in cls._SUPPORTED_LANGUAGES:
            cls._LANGUAGE = normalized
            cls.logger.info(f"Applied Language: {normalized}")
            return

        cls.logger.warning(f"Invalid language '{language}' provided. Keeping existing language setting.")
    # ======================= End of Language Settings =======================

    # ======================= Support Developer Mode Settings =======================
    @classmethod
    def is_support_developer_enabled(cls) -> bool:
        return cls._is_support_developer_enabled

    @classmethod
    def set_support_developer_enabled(cls, enabled: bool) -> None:
        cls._is_support_developer_enabled = bool(enabled)
        ProgramSettings.logger.info(f"Support Developer Set to: {enabled}")

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
        ProgramSettings.logger.info(f"Compatibility Mode Set to: {enabled}")

    @classmethod
    def toggle_compatibility_mode(cls) -> None:
        cls.set_compatibility_mode_enabled(not cls._is_compatibility_mode_enabled)

    @classmethod
    def select_command(cls, default_command: Sequence[str] | str, compatibility_command: Sequence[str] | str):
        return compatibility_command if cls.is_compatibility_mode_enabled() else default_command
    # ======================= End of Compatibility Mode Settings =======================

    # ======================= Follow System Font Settings =======================
    @classmethod
    def is_follow_system_font_enabled(cls) -> bool:
        return cls._is_follow_system_font_enabled

    @classmethod
    def set_follow_system_font_enabled(cls, enabled: bool) -> None:
        cls._is_follow_system_font_enabled = bool(enabled)
        ProgramSettings.logger.info(f"Follow System Font Set to: {enabled}")

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