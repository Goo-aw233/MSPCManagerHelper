from core.app_logger import AppLogger


class AppSettings:
    logger = AppLogger.get_logger()

    _is_cleanup_after_exit_enabled: bool = False
    _appearance_mode: str = "System"
    _is_follow_system_font_enabled: bool = False
    _is_support_developer_enabled: bool = True
    _is_compatibility_mode_enabled: bool = False
    _is_take_ownership_enabled: bool = False

    # ======================= Cleanup After Exit Settings =======================
    @classmethod
    def is_cleanup_after_exit_enabled(cls) -> bool:
        return cls._is_cleanup_after_exit_enabled

    @classmethod
    def set_cleanup_after_exit_enabled(cls, enabled: bool) -> None:
        cls._is_cleanup_after_exit_enabled = bool(enabled)
        AppSettings.logger.info(f"Cleanup After Exit Set to: {cls._is_cleanup_after_exit_enabled}")

    @classmethod
    def toggle_cleanup_after_exit(cls) -> None:
        cls.set_cleanup_after_exit_enabled(not cls._is_cleanup_after_exit_enabled)
    # ======================= End of Cleanup After Exit Settings =======================

    # ======================= Appearance Settings =======================
    @classmethod
    def get_appearance_mode(cls) -> str:
        return cls._appearance_mode

    @classmethod
    def set_appearance_mode(cls, mode: str) -> None:
        cls._appearance_mode = mode
        AppSettings.logger.info(f"Appearance Mode Set to: {mode}")
    # ======================= End of Appearance Settings =======================

    # ======================= Follow System Font Settings =======================
    @classmethod
    def is_follow_system_font_enabled(cls) -> bool:
        return cls._is_follow_system_font_enabled

    @classmethod
    def set_follow_system_font_enabled(cls, enabled: bool) -> None:
        cls._is_follow_system_font_enabled = bool(enabled)
        AppSettings.logger.info(f"Follow System Font Set to: {cls._is_follow_system_font_enabled}")

    @classmethod
    def toggle_follow_system_font(cls) -> None:
        cls.set_follow_system_font_enabled(not cls._is_follow_system_font_enabled)
    # ======================= End of Follow System Font Settings =======================

    # ======================= Support Developer Settings =======================
    @classmethod
    def is_support_developer_enabled(cls) -> bool:
        return cls._is_support_developer_enabled

    @classmethod
    def set_support_developer_enabled(cls, enabled: bool) -> None:
        cls._is_support_developer_enabled = bool(enabled)
        AppSettings.logger.info(f"Support Developer Set to: {cls._is_support_developer_enabled}")

    @classmethod
    def get_support_developer_tracking_id(cls) -> str:
        return "/?wt.mc_id=studentamb_474966" if cls._is_support_developer_enabled else ""
    # ======================= End of Support Developer Settings =======================

    # ======================= Compatibility Mode Settings =======================
    @classmethod
    def is_compatibility_mode_enabled(cls) -> bool:
        return cls._is_compatibility_mode_enabled
    
    @classmethod
    def set_compatibility_mode_enabled(cls, enabled: bool) -> None:
        cls._is_compatibility_mode_enabled = bool(enabled)
        AppSettings.logger.info(f"Compatibility Mode Set to: {cls._is_compatibility_mode_enabled}")
    
    @classmethod
    def toggle_compatibility_mode(cls) -> None:
        cls.set_compatibility_mode_enabled(not cls._is_compatibility_mode_enabled)
    # ======================= End of Compatibility Mode Settings =======================

    # ======================= Take Ownership Settings =======================
    @classmethod
    def is_take_ownership_enabled(cls) -> bool:
        return cls._is_take_ownership_enabled
    
    @classmethod
    def set_take_ownership_enabled(cls, enabled: bool) -> None:
        cls._is_take_ownership_enabled = bool(enabled)
        AppSettings.logger.info(f"Take Ownership Set to: {cls._is_take_ownership_enabled}")
    
    @classmethod
    def toggle_take_ownership(cls) -> None:
        cls.set_take_ownership_enabled(not cls._is_take_ownership_enabled)
    # ======================= End of Take Ownership Settings =======================
