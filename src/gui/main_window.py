import locale
import os
import sys
from pathlib import Path

import customtkinter

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_resources import AppResources
from core.app_settings import AppSettings
from core.app_translator import AppTranslator
from core.set_font_family import SetFontFamily
from core.system_checks import PrerequisiteChecks


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.logger = AppLogger.get_logger()
        app_launch_message = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION}"
        if AdvancedStartup.is_devmode():
            app_launch_message += " (in DevMode)"
        elif AdvancedStartup.is_debugmode():
            app_launch_message += " (in DebugMode)"
        app_launch_message += " Launched"
        self.logger.info(app_launch_message)
        self.logger.info(f"Launched From: {Path(sys.argv[0]).resolve()}")
        self.logger.info(f"Runtime Arguments: {AdvancedStartup.get_runtime_arguments()}")
        self.logger.info(f"Current Working Directory: {os.getcwd()}")
        self.logger.info(f"Log File Path: {AppLogger.get_log_file_path()}")
        if hasattr(sys, "_MEIPASS"):
            self.logger.info(f"PyInstaller Extraction Path: {sys._MEIPASS}")
        else:
            self.logger.info("PyInstaller Extraction Path: Not Running from PyInstaller Bundle")
        self.logger.info(f"CPython JIT Available: {sys._jit.is_available()}, Enabled: {sys._jit.is_enabled()}")

        self.logger.info("========================= Initializing Base GUI =========================")
        self._set_language()
        self._configure_window()
        self.logger.info("========================= Base GUI Initialized =========================")

    def _configure_window(self):
        app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION}"
        if AdvancedStartup.is_administrator():
            app_title += " [Administrator]"
        if AdvancedStartup.is_devmode():
            app_title += " [DevMode]"
        elif AdvancedStartup.is_debugmode():
            app_title += " [DebugMode]"
        self.title(app_title)

        icon_path = AppResources.app_icon()
        if icon_path:
            self.iconbitmap(icon_path)
            self.logger.info(f"Window Icon: {icon_path}")

        self._set_window_geometry()

        # Set font family.
        language = getattr(self, "language", "").lower()
        # Determine whether to follow system font through AppSettings.
        follow_system_font = AppSettings.is_follow_system_font_enabled()
        self.font_family = SetFontFamily.apply_font_setting(follow_system_font=follow_system_font, language=language)
        self.logger.info(f"Follow Font Setting: {follow_system_font}")

    def _set_language(self):
        language_map = {
            # English
            ("en_", "en-",): "en-us",
            # Simplified Chinese
            ("zh_CN", "zh_Hans", "zh_Hans_", "zh_Hans_CN", "zh_Hans_HK", "zh_Hans_MO", "zh_Hans_SG", "zh_SG", "zh-CN",
             "zh-Hans", "zh-Hans-", "zh-Hans-CN", "zh-Hans-HK", "zh-Hans-MO", "zh-Hans-SG", "zh-SG",): "zh-cn",
            # Traditional Chinese
            ("zh_Hant", "zh_Hant_", "zh_Hant_HK", "zh_Hant_MO", "zh_Hant_TW", "zh_HK", "zh_MO", "zh_TW", "zh-Hant",
             "zh-Hant-", "zh-Hant-HK", "zh-Hant-MO", "zh-Hant-TW", "zh-HK", "zh-MO", "zh_TW",): "zh-tw"
        }
        locale_str = locale.getdefaultlocale()[0]
        language = "en-us"  # Default Language
        for prefixes, trans_locale in language_map.items():
            if any(locale_str.startswith(prefix) for prefix in prefixes):
                language = trans_locale
                break
        self.language = language
        self.app_translator = AppTranslator(self.language)
        # Synchronize the language to PrerequisiteChecks class.
        PrerequisiteChecks.app_translator = self.app_translator
        self.logger.info(f"App Language: {self.language}")

    def _set_window_geometry(self):
        # Use a target size that feels native, but ensure it fits within 85% of the screen for smaller displays.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        target_width = 1100
        target_height = 750

        width = min(target_width, int(screen_width * 0.85))
        height = min(target_height, int(screen_height * 0.85))

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(800, 600)
        self.logger.info(f"Window Geometry Set: {width} x {height} (x + {x}, y + {y})")
