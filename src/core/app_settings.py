from core.app_logger import AppLogger
from core.set_font_family import SetFontFamily


class AppSettings:
    logger = AppLogger.get_logger()

    _is_follow_system_font_enabled: bool = False

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
