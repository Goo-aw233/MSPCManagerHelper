import ctypes
import tkinter
import tkinter.font

from core.app_logger import AppLogger


FLUENT_ICONS_FONT_FAMILY = "FluentSystemIcons-Regular"


class SetFontFamily:
    # Idempotent Protection: Prevent registering the same font multiple times
    # (GDI will count it, but the file will only be added once).
    _fluent_font_registered = False

    @staticmethod
    def register_fluent_icons_font():
        """Register the bundled FluentSystemIcons font for the current process.

        Tk can only use fonts that are known to GDI. The font is registered
        privately (FR_PRIVATE) through AddFontResourceExW, so no administrator
        rights or permanent system installation are required. The call is
        idempotent: only the first call registers the font.
        """
        if SetFontFamily._fluent_font_registered:
            return True

        from core.app_resources import AppResources

        logger = AppLogger.get_logger()
        font_path = AppResources.fluent_icons_font_path()
        if not font_path:
            logger.warning("FluentSystemIcons-Regular.ttf was not found in the application resources."
                           "If the font is not installed, the icons will not be displayed properly.")
            return False

        try:
            gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
            gdi32.AddFontResourceExW.argtypes = (ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p)
            gdi32.AddFontResourceExW.restype = ctypes.c_int
            # FR_PRIVATE (0x10): The font is only visible to the calling process.
            added = gdi32.AddFontResourceExW(font_path, 0x10, None)
            if added:
                SetFontFamily._fluent_font_registered = True
                logger.info(f"FluentSystemIcons-Regular.ttf Registered: {font_path}")
                return True
            logger.warning(
                f"AddFontResourceExW Failed to Register Font (Error {ctypes.get_last_error()}): {font_path}"
            )
        except OSError:
            logger.exception("Failed to register FluentSystemIcons-Regular.ttf via GDI.")
        return False

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
            preferred_font = language_font_map.get(language.lower(), "Segoe UI Variable Text")
            if preferred_font == "Segoe UI Variable Text" and "Segoe UI Variable Text" not in available_fonts:
                preferred_font = "Segoe UI"
            mapped_font = preferred_font
            logger.info(f"Using App Font: {mapped_font}")
            return mapped_font
