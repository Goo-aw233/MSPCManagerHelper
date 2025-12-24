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
from gui.pages import *
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
        ProgramSettings.set_theme_mode(ProgramSettings.get_theme_mode())
        self._set_language()
        self._configure_window()
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

        self._update_font_family()

        # Set Window Size
        self._adjust_window_size(default_width=1100, default_height=720)

        # Set Window Icon
        program_icon_path = GetProgramResources.get_program_icon()
        if program_icon_path:
            self.iconbitmap(program_icon_path)
            self.logger.info(f"Window Icon: {program_icon_path}")

    def _update_font_family(self):
        # Determine whether to follow system font through ProgramSettings.
        language = getattr(self, "language", "").lower()
        follow_system_font = ProgramSettings.is_follow_system_font_enabled()
        self.font_family = SetFontFamily.apply_font_setting(follow_system_font=follow_system_font, language=language)
        self.logger.info(f"Font Setting: follow_system_font={follow_system_font}")

    def _initialize_layout(self, initial_page: str = "home"):
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
        target_page = initial_page if initial_page in self.pages else "home"
        self._switch_page(target_page)

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
        locale_info = locale.getdefaultlocale()
        locale_str = locale_info[0] if locale_info and locale_info[0] else ""

        configured_language = ProgramSettings.get_language()
        language = configured_language if configured_language in ProgramSettings.get_supported_languages() else None

        if not language:
            for prefixes, trans_locale in language_map.items():
                if any(locale_str.startswith(prefix) for prefix in prefixes):
                    language = trans_locale
                    break

        if language not in ProgramSettings.get_supported_languages():
            language = "en-us"
        self.language = language
        ProgramSettings.set_language(language)
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
            if name == "settings":
                frame = SettingsPage(
                    self.content_container,
                    translator=self.translator,
                    font_family=self.font_family,
                    on_theme_change=self._on_theme_changed,
                    on_language_change=self._on_language_changed,
                )
            else:
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
        elif page_key != "home" and "home" in self.pages:
            self.pages["home"].grid(row=0, column=0, sticky="nsew")
            page_key = "home"

        if hasattr(self, "navigation_frame"):
            self.navigation_frame.set_active(page_key)

    def _on_theme_changed(self, mode: str):
        if hasattr(self, "navigation_frame"):
            self.navigation_frame.refresh_palette()

    def _on_language_changed(self, language: str):
        self._refresh_language(language)

    def _refresh_language(self, language: str):
        if not language:
            return

        normalized = language.lower()
        if normalized == getattr(self, "language", None):
            return

        if normalized not in ProgramSettings.get_supported_languages():
            self.logger.warning(f"Unsupported language change requested: {language}")
            return

        self.logger.info("--------------- Switching Language ---------------")
        self.language = normalized
        ProgramSettings.set_language(normalized)
        self.translator = Translator(self.language)
        CheckSystemRequirements.translator = self.translator
        self._update_font_family()

        active_page = "home"
        if hasattr(self, "navigation_frame") and getattr(self.navigation_frame, "active_key", None):
            active_page = self.navigation_frame.active_key

        if hasattr(self, "navigation_frame"):
            self.navigation_frame.destroy()
        if hasattr(self, "content_container"):
            self.content_container.destroy()

        self.pages = {}
        self._initialize_layout(initial_page=active_page)
        self.logger.info(f"Program Language Switched to: {self.language}")
        self.logger.info("--------------- Language Switched ---------------")

    def _adjust_window_size(self, default_width, default_height, offset_ratio=0.05):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        min_offset = int(min(screen_width, screen_height) * offset_ratio)
        width = min(default_width, screen_width - min_offset)
        height = min(default_height, screen_height - min_offset)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
