import os
import sys
from pathlib import Path

import customtkinter

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_resources import AppResources


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
