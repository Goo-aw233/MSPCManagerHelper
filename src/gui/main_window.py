import ctypes
import locale
import os
import sys
import tkinter
import tkinter.font
from pathlib import Path
from tkinter import messagebox, ttk

from windows_toasts import Toast, WindowsToaster

from core.advanced_startup import AdvancedStartup
from core.check_system_requirements import CheckSystemRequirements
from core.get_program_resources import GetProgramResources
from core.program_logger import ProgramLogger
from core.program_metadata import ProgramMetadata
from core.program_settings import ProgramSettings
from core.system_utilities_availability_check import SystemUtilitiesAvailabilityCheck
from core.translator import Translator
from gui.widgets.navigation import Navigation


class MSPCManagerHelperMainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        # self.withdraw() # Hide window to prevent flashing.
        self.logger = ProgramLogger.get_logger()
        program_launch_message = f"{ProgramMetadata.PROGRAM_NAME} {ProgramMetadata.PROGRAM_VERSION}"
        if AdvancedStartup.is_devmode():
            program_launch_message += " (in DevMode)"
        if AdvancedStartup.is_debugmode():
            program_launch_message += " (in DebugMode)"
        program_launch_message += " launched."
        self.logger.info(program_launch_message)
        self.logger.info(f"Launched From: {Path(sys.argv[0]).resolve()}")
        self.logger.info(f"Runtime Arguments: {AdvancedStartup.get_runtime_arguments()}")
        self.logger.info(f"Current Working Directory: {os.getcwd()}")
        if hasattr(sys, "_MEIPASS"):
            self.logger.info(f"PyInstaller Extraction Path: {sys._MEIPASS}")
        else:
            self.logger.info("PyInstaller Extraction Path: Not running from PyInstaller bundle.")
        self.logger.info("========================= Initializing Base GUI =========================")
        ProgramSettings.apply_theme()
        self._set_dpi_awareness()
        self._set_language()
        self._configure_window()
        self._check_system_requirements()
        self._configure_ui()
        self.logger.info("========================= Base GUI Initialized =========================")
        # self.deiconify()    # Show window after all configurations are done.

    def _configure_window(self):
        # Create a Background Frame that will hold all other widgets.
        self.background_frame = ttk.Frame(self)
        self.background_frame.pack(fill="both", expand=True)

        # Set the window title.
        program_title_str = f"{ProgramMetadata.PROGRAM_NAME} {ProgramMetadata.PROGRAM_VERSION}"
        if AdvancedStartup.is_administrator():
            program_title_str += " (Administrator)"
        if AdvancedStartup.is_devmode():
            program_title_str += " - DevMode"
        if AdvancedStartup.is_debugmode():
            program_title_str += " - DebugMode"
        self.title(program_title_str)
        # Set font family.
        language_font_map = {
            "en-us": "Segoe UI",
            "zh-cn": "Microsoft YaHei UI",
            "zh-tw": "Microsoft JhengHei UI"
        }
        system_font = tkinter.font.nametofont("TkDefaultFont").actual().get("family", "")
        mapped_font = language_font_map.get(getattr(self, "language", "").lower(), system_font)
        # Use system font when it matches the mapping; otherwise use the mapped font.
        if system_font and system_font.lower() == mapped_font.lower():
            self.font_family = system_font
        else:
            self.font_family = mapped_font if mapped_font else system_font
        self.logger.info(f"System Font: {system_font}; Language Mapped Font: {mapped_font}; Using Font: {self.font_family}")
        # Set window size.
        self._adjust_window_size(default_width=984, default_height=661)
        # Set window icon.
        program_icon_path = GetProgramResources.get_program_icon()
        if program_icon_path:
            self.iconbitmap(program_icon_path)
            self.logger.info(f"Window Icon: {program_icon_path}")

    def _set_dpi_awareness(self):
        # Tell Windows to use this program's DPI awareness and adjust Tk scaling.
        self._dpi_scale_ratio = 1.0
        try:
            if sys.platform == "win32":
                if hasattr(ctypes.windll, "shcore"):
                    try:
                        ctypes.windll.shcore.SetProcessDpiAwareness(1)
                    except Exception:
                        pass
                    try:
                        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
                        # Save DPI ratio for use when setting window size.
                        self._dpi_scale_ratio = float(scale_factor) / 100.0
                        self.tk.call('tk', 'scaling', float(scale_factor) / 75)
                        self.logger.info(f"DPI Scaling Set: scale_factor={scale_factor}")
                    except Exception:
                        self._dpi_scale_ratio = 1.0
                        self.logger.warning("Failed to obtain or apply device scale factor.")
                else:
                    self.logger.debug("shcore.dll not available; skipping DPI awareness setting.")
        except Exception as e:
            self._dpi_scale_ratio = 1.0
            self.logger.warning(f"Failed to Set DPI Awareness: {e}")

    def _set_language(self):
        language_map = {
            # English
            ('en_', 'en-'): 'en-us',
            # Simplified Chinese
            ('zh_CN', 'zh_Hans', 'zh_Hans_', 'zh_Hans_CN', 'zh_Hans_HK', 'zh_Hans_MO', 'zh_Hans_SG', 'zh_SG', 'zh-CN',
             'zh-Hans', 'zh-Hans-', 'zh-Hans-CN', 'zh-Hans-HK', 'zh-Hans-MO', 'zh-Hans-SG', 'zh-SG',): 'zh-cn',
            # Traditional Chinese
            ('zh_Hant', 'zh_Hant_', 'zh_Hant_HK', 'zh_Hant_MO', 'zh_Hant_TW', 'zh_HK', 'zh_MO', 'zh_TW', 'zh-Hant',
             'zh-Hant-',
             'zh-Hant-HK', 'zh-Hant-MO', 'zh-Hant-TW', 'zh-HK', 'zh-MO', 'zh_TW'): 'zh-tw'
        }
        locale_str = locale.getdefaultlocale()[0]
        language = 'en-us'  # Default language.
        for prefixes, trans_locale in language_map.items():
            if any(locale_str.startswith(prefix) for prefix in prefixes):
                language = trans_locale
                break
        self.language = language
        self.translator = Translator(self.language)
        # Synchronize the language to CheckSystemRequirements class.
        CheckSystemRequirements.translator = self.translator
        self.logger.info(f"Program Language: {self.language}")

    def _check_system_requirements(self):
        found_issue = False
    
        if not CheckSystemRequirements.check_if_windows_nt():
            found_issue = True
            self.logger.error("Operating system is not Windows NT-based.")
            messagebox.showerror(
                self.translator.translate("error"),
                self.translator.translate("operating_system_is_not_windows_nt_based")
            )
            sys.exit(1)

        if CheckSystemRequirements.check_admin_approval_mode():
            found_issue = True
            self.logger.warning("Admin Approval Mode is enabled.")
            messagebox.showwarning(
                self.translator.translate("warning"),
                self.translator.translate("administrator_protection_is_enabled")
            )

        if CheckSystemRequirements.check_windows_server_levels():
            found_issue = True
            self.logger.warning("Windows Server installation type is Core.")
            messagebox.showwarning(
                self.translator.translate("warning"),
                self.translator.translate("windows_server_installation_type_is_core")
            )

        SystemUtilitiesAvailabilityCheck.check_system_path_availability()

        utility_availability = SystemUtilitiesAvailabilityCheck.check_system_utilities_availability()
        for utility, is_available in utility_availability.items():
            if not is_available:
                found_issue = True
                self.logger.warning(f"{utility} is not available.")

        SystemUtilitiesAvailabilityCheck.check_system_utilities_version()

        if not AdvancedStartup.is_administrator():
            found_issue = True
            self.logger.warning("Program is not running as administrator.")
            toaster = WindowsToaster(self.translator.translate("mspcmanagerhelper"))
            toast_notification = Toast()
            toast_notification.text_fields = [
                self.translator.translate("administrator_required"),
                self.translator.translate("program_is_not_running_as_administrator")
            ]
            toaster.show_toast(toast_notification)

        if SystemUtilitiesAvailabilityCheck.check_narrator_status():
            found_issue = True
            self.logger.warning("Narrator is running.")
            messagebox.showwarning(
                self.translator.translate("warning"),
                self.translator.translate("narrator_is_running")
            )

        if not found_issue:
            self.logger.info("No system requirement issues were found.")

    def _configure_ui(self):
        self.background_frame.grid_columnconfigure(1, weight=1)
        self.background_frame.grid_rowconfigure(0, weight=1)
        self.navigation = Navigation(self.background_frame, self.translator, self.font_family)
        self.navigation.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    def _adjust_window_size(self, default_width, default_height, offset_ratio=0.05):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        min_offset = int(min(screen_width, screen_height) * offset_ratio)
        scale_ratio = getattr(self, "_dpi_scale_ratio", 1.0)
        width = min(int(default_width * scale_ratio), screen_width - min_offset)
        height = min(int(default_height * scale_ratio), screen_height - min_offset)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.update_idletasks()  # Update window information.
        self.logger.info(f"Window Size: {self.winfo_width()} x {self.winfo_height()} (scale={scale_ratio})")

    def refresh_ui(self):
        self.logger.info("Refreshing Main Window UI...")
        if hasattr(self, "background_frame") and self.background_frame.winfo_exists():
            self.background_frame.destroy()
        ProgramSettings.apply_theme()
        self._configure_window()
        self._set_language()
        self._configure_ui()
        self.update_idletasks()
        self.logger.info("Main Window UI refreshed.")
