from core.app_logger import AppLogger
from core.set_font_family import SetFontFamily


class AppSettings:
    logger = AppLogger.get_logger()

    _is_follow_system_font_enabled: bool = False
    _appearance_mode: str = "System"

    # ======================= Appearance Settings =======================
    @classmethod
    def get_appearance_mode(cls) -> str:
        return cls._appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode: str) -> None:
        cls._appearance_mode = mode
        AppSettings.logger.info(f"Appearance Mode Set to: {mode}")

    # ======================= Follow System Font Settings =======================
    @classmethod
    def is_follow_system_font_enabled(cls) -> bool:
        return cls._is_follow_system_font_enabled

    @classmethod
    def set_follow_system_font_enabled(cls, enabled: bool) -> None:
        cls._is_follow_system_font_enabled = bool(enabled)
        AppSettings.logger.info(f"Follow System Font Set to: {enabled}")
        SetFontFamily.apply_font_setting(follow_system_font=enabled)

    @classmethod
    def toggle_follow_system_font(cls) -> None:
        cls.set_follow_system_font_enabled(not cls._is_follow_system_font_enabled)
    # ======================= End of Follow System Font Settings =======================
