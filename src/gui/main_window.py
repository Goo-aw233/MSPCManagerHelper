import locale
import os
import sys
from pathlib import Path
from tkinter import messagebox

import customtkinter
from windows_toasts import Toast, WindowsToaster

from core.advanced_startup import AdvancedStartup
from core.check_system_requirements import CheckSystemRequirements
from core.get_program_resources import GetProgramResources
from core.program_logger import ProgramLogger
from core.program_metadata import ProgramMetadata
from core.program_settings import ProgramSettings
from core.set_font_family import SetFontFamily
from core.translator import Translator
from gui.widgets.navigation_frame import NavigationFrame


class MSPCManagerHelperMainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.logger = ProgramLogger.get_logger()
        program_launch_message = f"{ProgramMetadata.PROGRAM_NAME} {ProgramMetadata.PROGRAM_VERSION}"
        if AdvancedStartup.is_devmode():
            program_launch_message += " (in DevMode)"
        if AdvancedStartup.is_debugmode():
            program_launch_message += " (in DebugMode)"
        program_launch_message += " Launched"
        self.logger.info(program_launch_message)
        self.logger.info(f"Launched From: {Path(sys.argv[0]).resolve()}")
        self.logger.info(f"Runtime Arguments: {AdvancedStartup.get_runtime_arguments()}")
        self.logger.info(f"Current Working Directory: {os.getcwd()}")
        self.logger.info(f"Log File Path: {ProgramLogger.get_log_file_path()}")
        if hasattr(sys, "_MEIPASS"):
            self.logger.info(f"PyInstaller Extraction Path: {sys._MEIPASS}")
        else:
            self.logger.info("PyInstaller Extraction Path: Not Running from PyInstaller Bundle")
        self.logger.info(f"CPython JIT Available: {sys._jit.is_available()}, Enabled: {sys._jit.is_enabled()}")
        self.logger.info("========================= Initializing Base GUI =========================")
        self._configure_window()
        self._set_language()
        if AdvancedStartup.is_bypasscheck():
            self.logger.info("System Requirements Check Bypassed")
        else:
            self._check_system_requirements()
        self._initialize_layout()
        self.logger.info("========================= Base GUI Initialized =========================")

    def _configure_window(self):
        # Set the Window Title
        program_title_str = f"{ProgramMetadata.PROGRAM_NAME} {ProgramMetadata.PROGRAM_VERSION}"
        if AdvancedStartup.is_administrator():
            program_title_str += " (Administrator)"
        if AdvancedStartup.is_devmode():
            program_title_str += " - DevMode"
        if AdvancedStartup.is_debugmode():
            program_title_str += " - DebugMode"
        self.title(program_title_str)
    
        # Set Font Family
        language = getattr(self, "language", "").lower()
        # Determine whether to follow system font through ProgramSettings.
        follow_system_font = ProgramSettings.is_follow_system_font_enabled()
        self.font_family = SetFontFamily.apply_font_setting(follow_system_font=follow_system_font, language=language)
        self.logger.info(f"Font Setting: follow_system_font={follow_system_font}")
    
        # Set Window Size
        self._adjust_window_size(default_width=1100, default_height=720)

        # Set Window Icon
        program_icon_path = GetProgramResources.get_program_icon()
        if program_icon_path:
            self.iconbitmap(program_icon_path)
            self.logger.info(f"Window Icon: {program_icon_path}")

    def _initialize_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_frame = NavigationFrame(
            self,
            translator=self.translator,
            font_family=self.font_family,
            on_nav=self._switch_page,
        )
        self.navigation_frame.grid(row=0, column=0, sticky="ns")

        self.content_container = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self._build_pages()
        self._switch_page("home")

    def _set_language(self):
        language_map = {
            # English
            ("en_", "en-"): "en-us",
            # Simplified Chinese
            ("zh_CN", "zh_Hans", "zh_Hans_", "zh_Hans_CN", "zh_Hans_HK", "zh_Hans_MO", "zh_Hans_SG", "zh_SG", "zh-CN",
             "zh-Hans", "zh-Hans-", "zh-Hans-CN", "zh-Hans-HK", "zh-Hans-MO", "zh-Hans-SG", "zh-SG",): "zh-cn",
            # Traditional Chinese
            ("zh_Hant", "zh_Hant_", "zh_Hant_HK", "zh_Hant_MO", "zh_Hant_TW", "zh_HK", "zh_MO", "zh_TW", "zh-Hant",
             "zh-Hant-",
             "zh-Hant-HK", "zh-Hant-MO", "zh-Hant-TW", "zh-HK", "zh-MO", "zh_TW"): "zh-tw"
        }
        locale_str = locale.getdefaultlocale()[0]
        language = "en-us"  # Default Language
        for prefixes, trans_locale in language_map.items():
            if any(locale_str.startswith(prefix) for prefix in prefixes):
                language = trans_locale
                break
        self.language = language
        self.translator = Translator(self.language)
        # Synchronize the Language to CheckSystemRequirements Class
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

        if not AdvancedStartup.is_administrator():
            found_issue = True
            self.logger.warning("Program is not running as administrator.")
            toaster = WindowsToaster(ProgramMetadata.PROGRAM_NAME)
            run_as_administrator_toast = Toast()
            run_as_administrator_toast.text_fields = [
                self.translator.translate("administrator_required"),
                self.translator.translate("program_is_not_running_as_administrator")
            ]
            run_as_administrator_toast.tag = "administrator_required_toast"
            toaster.show_toast(run_as_administrator_toast)

        if not CheckSystemRequirements.check_if_long_paths_enabled():
            found_issue = True
            self.logger.warning("Long paths are not enabled.")

        if not found_issue:
            self.logger.info("No system requirement issues were found.")

    def _build_pages(self):
        page_specs = [
            ("home", "home_page", "home_page_subtitle", "home_page_hint"),
            ("maintenance", "maintenance_page", "maintenance_page_subtitle", "maintenance_page_hint"),
            ("installer", "installer_page", "installer_page_subtitle", "installer_page_hint"),
            ("uninstaller", "uninstaller_page", "uninstaller_page_subtitle", "uninstaller_page_hint"),
            ("utilities", "utilities_page", "utilities_page_subtitle", "utilities_page_hint"),
            ("toolbox", "toolbox_page", "toolbox_page_subtitle", "toolbox_page_hint"),
            ("about", "about_page", "about_page_subtitle", "about_page_hint"),
            ("settings", "settings_page", "settings_page_subtitle", "settings_page_hint"),
        ]

        for name, title_key, subtitle_key, hint_key in page_specs:
            frame = self._build_placeholder_page(
                title=self.translator.translate(title_key),
                subtitle=self.translator.translate(subtitle_key),
                hint=self.translator.translate(hint_key),
            )
            self.pages[name] = frame

    def _build_placeholder_page(self, title: str, subtitle: str, hint: str):
        frame = customtkinter.CTkFrame(self.content_container, fg_color="transparent", corner_radius=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header = customtkinter.CTkFrame(frame, fg_color="transparent", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        title_label = customtkinter.CTkLabel(
            header,
            text=title,
            font=(self.font_family, 28, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")

        subtitle_label = customtkinter.CTkLabel(
            header,
            text=subtitle,
            font=(self.font_family, 14),
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        hint_chip = customtkinter.CTkLabel(
            header,
            text=hint,
            font=(self.font_family, 12),
            fg_color="#e5f1fb",
            text_color="#0f6cbd",
            corner_radius=8,
            padx=12,
            pady=6,
        )
        hint_chip.grid(row=0, column=1, rowspan=2, sticky="e")

        placeholder = customtkinter.CTkFrame(frame, fg_color="transparent")
        placeholder.grid(row=1, column=0, padx=24, pady=12, sticky="nsew")
        placeholder.grid_rowconfigure(0, weight=1)
        placeholder.grid_columnconfigure(0, weight=1)
        return frame

    def _switch_page(self, page_key: str):
        for frame in self.pages.values():
            frame.grid_forget()

        target = self.pages.get(page_key)
        if target:
            target.grid(row=0, column=0, sticky="nsew")

        if hasattr(self, "navigation_frame"):
            self.navigation_frame.set_active(page_key)

    def _adjust_window_size(self, default_width, default_height, offset_ratio=0.05):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        min_offset = int(min(screen_width, screen_height) * offset_ratio)
        width = min(default_width, screen_width - min_offset)
        height = min(default_height, screen_height - min_offset)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
