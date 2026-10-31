import ctypes
import tkinter
import tkinter.font

from .app_logger import AppLogger


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

        from .app_resources import AppResources

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
    def apply_font_setting(
        follow_system_font: bool = False,
        language: str | None = None,
        monospaced: bool = False
    ):
        logger = AppLogger.get_logger()

        # Monospaced Font for Console or Code Display
        if monospaced:
            available_fonts = set(tkinter.font.families())
            candidates = ("Cascadia Mono", "Consolas")

            mapped_font = next(
                (font for font in candidates if font in available_fonts),
                tkinter.font.nametofont("TkFixedFont").actual()["family"]
            )

            logger.info(f"Using Monospaced Font: {mapped_font}")
            return mapped_font

        # Font for UI
        if follow_system_font:
            system_font = tkinter.font.nametofont("TkDefaultFont").actual().get("family", "")
            logger.info(f"Using System Font: {system_font}")
            return system_font

        # Follow App Font Settings
        # If there is not matching item, the first item in the list will be used as default,
        # displayed with Tk default font family.
        language_font_map = {
            # Segoe UI Variable Text is Introduced in Build 21376
            "en-us": ("Segoe UI Variable Text", "Segoe UI"),
            "zh-cn": ("Microsoft YaHei UI", "微软雅黑"),
            "zh-tw": ("Microsoft JhengHei UI", "微軟正黑體")
        }

        target_lang = (language or "en-us").lower()
        available_fonts = set(tkinter.font.families())
        candidates = language_font_map.get(target_lang, language_font_map["en-us"])
        mapped_font = next((font for font in candidates if font in available_fonts), candidates[0])

        logger.info(f"Using App Font: {mapped_font}")
        return mapped_font
