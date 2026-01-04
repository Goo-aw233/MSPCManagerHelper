import ctypes
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


class HelpWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.logger = AppLogger.get_logger()
        app_launch_message = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION } Help Window Launched"
        self.logger.info(app_launch_message)
        self.logger.info(f"Launched From: {Path(sys.argv[0]).resolve()}")
        self.logger.info(f"Runtime Arguments: {AdvancedStartup.get_runtime_arguments()}")
        self.logger.info(f"Current Working Directory: {os.getcwd()}")
        self.logger.info(f"Log File Path: {AppLogger.get_log_file_path()}")
        if hasattr(sys, "_MEIPASS"):
            self.logger.info(f"PyInstaller Extraction Path: {sys._MEIPASS}")
        else:
            self.logger.info("PyInstaller Extraction Path: Not Running from PyInstaller Bundle")

        self.logger.info("========================= Initializing Help Window =========================")
        self._set_language()
        self._configure_window()

        # Set font family.
        language = getattr(self, "language", "").lower()
        # Determine whether to follow system font through AppSettings.
        follow_system_font = AppSettings.is_follow_system_font_enabled()
        self.font_family = SetFontFamily.apply_font_setting(follow_system_font=follow_system_font, language=language)
        self.logger.info(f"Follow Font Setting: {follow_system_font}")

        self._create_widgets()

        self.after(200, self._remove_minimize_maximize_buttons)
        self.logger.info("========================= Help Window Initialized =========================")

    def _create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.help_content_textbox = customtkinter.CTkTextbox(
            self,
            font=(self.font_family, 13)
        )
        self.help_content_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        help_content = (
            f"{self.app_translator.translate('help_window_content_title')}\n\n\n"
            f"{self.app_translator.translate('help_window_content_args_1')}\n\n"
            f"{self.app_translator.translate('help_window_content_args_2')}\n"
            f"{self.app_translator.translate('help_window_content_args_3')}\n\n"
            f"{self.app_translator.translate('help_window_content_args_4')}\n"
            f"{self.app_translator.translate('help_window_content_args_5')}\n\n"
            f"{self.app_translator.translate('help_window_content_args_6')}\n"
            f"{self.app_translator.translate('help_window_content_args_7')}\n\n"
            f"{self.app_translator.translate('help_window_content_args_8')}\n"
            f"{self.app_translator.translate('help_window_content_args_9')}\n\n\n"
            f"{self.app_translator.translate('help_window_content_get_help_1')}\n"
            f"{self.app_translator.translate('help_window_content_get_help_2')}"
        )
        self.help_content_textbox.insert("0.0", help_content)
        self.help_content_textbox.configure(state="disabled")
    def _configure_window(self):
        app_title = f"{AppMetadata.APP_NAME} {AppMetadata.APP_VERSION} {self.app_translator.translate('help_window_title')}"
        if AdvancedStartup.is_administrator():
            app_title += " [Administrator]"
        self.title(app_title)

        icon_path = AppResources.app_icon()
        if icon_path:
            self.iconbitmap(icon_path)
            self.logger.info(f"Window Icon: {icon_path}")
        self._set_window_geometry()
        self.resizable(False, False)

    def _set_language(self):
        self.language = AppTranslator.detect_system_language()
        self.app_translator = AppTranslator(self.language)
        self.logger.info(f"App Language: {self.language}")

    def _set_window_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = 480
        height = 360

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.logger.info(f"Window Geometry Set: {width} x {height} (x + {x}, y + {y}), Scaling Factor: {self._get_window_scaling()}")

    def _remove_minimize_maximize_buttons(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            GWL_STYLE = -16
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            style = style & ~WS_MINIMIZEBOX & ~WS_MAXIMIZEBOX
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        except Exception:
            pass
