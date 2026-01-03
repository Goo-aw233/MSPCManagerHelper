import tkinter
import tkinter.font

from core.app_logger import AppLogger


class SetFontFamily:
    @staticmethod
    def apply_font_setting(follow_system_font: bool = False, language: str = None):
        logger = AppLogger.get_logger()
        if follow_system_font:
            system_font = tkinter.font.nametofont("TkDefaultFont").actual().get("family", "")
            logger.info(f"Using System Font: {system_font}")
            return system_font
        else:
            # Follow App Font Settings
            language_font_map = {
                "en-us": "Segoe UI Variable Text",  # Introduced in Build 21376
                "zh-cn": "Microsoft YaHei UI",
                "zh-tw": "Microsoft JhengHei UI"
            }
            if not language:
                language = "en-us"
            available_fonts = set(tkinter.font.families())
            preferred_font = language_font_map.get(language, "Segoe UI Variable Text")
            if preferred_font == "Segoe UI Variable Text" and "Segoe UI Variable Text" not in available_fonts:
                preferred_font = "Segoe UI"
            mapped_font = preferred_font
            logger.info(f"Using App Font: {mapped_font}")
            return mapped_font
