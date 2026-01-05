import os
import sys
import time
from pathlib import Path
from tkinter import messagebox

import customtkinter
from windows_toasts import Toast, WindowsToaster

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.app_resources import AppResources
from core.app_settings import AppSettings
from core.app_translator import AppTranslator
from core.set_font_family import SetFontFamily
from core.system_checks import OptionalChecks, PrerequisiteChecks


class MainWindow(customtkinter.CTk):
    def __init__(self):
        start_global_init_time = time.perf_counter()
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
        if AdvancedStartup.is_bypass_checks():
            self.logger.info("Startup system checks has been bypassed.")
        else:
            self._internal_prerequisite_system_checks()
            self._internal_optional_system_checks()
        self._configure_ui()
        self.logger.info("========================= Base GUI Initialized =========================")

        end_global_init_time = time.perf_counter()
        elapsed_global_init_time = end_global_init_time - start_global_init_time
        self.logger.debug(f"MainWindow Initialization Completed in: {elapsed_global_init_time:.5f} s")

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
        self.language = AppTranslator.detect_system_language()
        self.app_translator = AppTranslator(self.language)
        # Synchronize the language to PrerequisiteChecks class.
        PrerequisiteChecks.app_translator = self.app_translator
        self.logger.info(f"App Language: {self.language}")

    def _internal_prerequisite_system_checks(self):
        found_prerequisite_issue = False

        if not PrerequisiteChecks.check_if_windows_nt():
            found_prerequisite_issue = True
            self.logger.error("Operating system is not Windows NT-based.")
            messagebox.showerror(
                self.app_translator.translate("error"),
                self.app_translator.translate("operating_system_is_not_windows_nt_based")
            )
            sys.exit(1)

        if PrerequisiteChecks.check_admin_approval_mode():
            found_prerequisite_issue = True
            self.logger.warning("Admin Approval Mode is enabled.")
            messagebox.showwarning(
                self.app_translator.translate("warning"),
                self.app_translator.translate("administrator_protection_is_enabled")
            )

        if PrerequisiteChecks.check_windows_server_levels():
            found_prerequisite_issue = True
            self.logger.warning("Windows Server installation type is Core.")
            messagebox.showwarning(
                self.app_translator.translate("warning"),
                self.app_translator.translate("windows_server_installation_type_is_core")
            )

        if not AdvancedStartup.is_administrator():
            found_prerequisite_issue = True
            self.logger.warning("App is not running as administrator.")
            toaster = WindowsToaster(AppMetadata.APP_NAME)
            run_as_administrator_toast = Toast()
            run_as_administrator_toast.text_fields = [
                self.app_translator.translate("administrator_required"),
                self.app_translator.translate("app_is_not_running_as_administrator")
            ]
            run_as_administrator_toast.tag = "administrator_required_toast"
            toaster.show_toast(run_as_administrator_toast)

        if not PrerequisiteChecks.check_if_long_paths_enabled():
            found_prerequisite_issue = True
            self.logger.warning("Long paths are not enabled.")

        if not found_prerequisite_issue:
            self.logger.info("No prerequisite system requirement issues were found.")

    def _internal_optional_system_checks(self):
        found_optional_issue = False

        if OptionalChecks.check_narrator_status():
            found_optional_issue = True
            self.logger.warning("Narrator is currently running.")
            messagebox.showinfo(
                self.app_translator.translate("information"),
                self.app_translator.translate("narrator_is_running")
            )

        if not OptionalChecks.check_windows_utilities_availability():
            found_optional_issue = True
            self.logger.warning("Some Windows utilities are unavailable.")
            messagebox.showwarning(
                self.app_translator.translate("warning"),
                self.app_translator.translate("some_windows_utilities_are_unavailable").format(
                    log_file_path=AppLogger.get_log_file_path()
                )
            )

        OptionalChecks.check_windows_utilities_version()

        if not found_optional_issue:
            self.logger.info("No optional system requirement issues were found.")

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
        self.logger.info(f"Window Geometry Set: {width} x {height} (x + {x}, y + {y}), Scaling Factor: {self._get_window_scaling()}")

    def _create_nav_button(self, icon, text_key, command, row):
        button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=4,
            height=40,
            border_spacing=10,
            text=f"{icon}    {self.app_translator.translate(text_key)}",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            font=customtkinter.CTkFont(family=self.font_family),
            command=command
        )
        button.grid(row=row, column=0, sticky="ew", pady=(0, 4))    # Actually displays 6 - 8 physical pixels.
        return button

    def _configure_ui(self):
        # Configure Grid Layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create Navigation Frame.
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text=f"{AppMetadata.APP_NAME}",
            font=customtkinter.CTkFont(family=self.font_family, size=18, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = self._create_nav_button("🏠", "home_page", self.home_button_event, 1)
        self.maintenance_button = self._create_nav_button("🧹", "maintenance_page", self.maintenance_button_event, 2)
        self.installer_button = self._create_nav_button("📥", "installer_page", self.installer_button_event, 3)
        self.uninstaller_button = self._create_nav_button("🗑", "uninstaller_page", self.uninstaller_button_event, 4)
        self.utilities_button = self._create_nav_button("🛠", "utilities_page", self.utilities_button_event, 5)
        self.toolbox_button = self._create_nav_button("🧰", "toolbox_page", self.toolbox_button_event, 6)
        # Leave a row to place the following buttons at the bottom.
        self.about_button = self._create_nav_button("  i", "about_page", self.about_button_event, 8)
        self.settings_button = self._create_nav_button("⚙️", "settings_page", self.settings_button_event, 9)

        # Create Main Frame.
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Select Default Frame.
        self.select_frame_by_page_name("home")

    def select_frame_by_page_name(self, page_name):
        # Set button color for selected button.
        self.home_button.configure(fg_color=("gray75", "gray25") if page_name == "home" else "transparent")
        self.installer_button.configure(fg_color=("gray75", "gray25") if page_name == "installer" else "transparent")
        self.uninstaller_button.configure(fg_color=("gray75", "gray25") if page_name == "uninstaller" else "transparent")
        self.utilities_button.configure(fg_color=("gray75", "gray25") if page_name == "utilities" else "transparent")
        self.toolbox_button.configure(fg_color=("gray75", "gray25") if page_name == "toolbox" else "transparent")
        self.maintenance_button.configure(fg_color=("gray75", "gray25") if page_name == "maintenance" else "transparent")
        self.about_button.configure(fg_color=("gray75", "gray25") if page_name == "about" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if page_name == "settings" else "transparent")

        # Show Selected Frame
        # TODO: Implement page switching when pages are implemented as CTkFrames.
        if page_name == "home":
            pass
        elif page_name == "installer":
            pass
        elif page_name == "uninstaller":
            pass
        elif page_name == "utilities":
            pass
        elif page_name == "toolbox":
            pass
        elif page_name == "maintenance":
            pass
        elif page_name == "about":
            pass
        elif page_name == "settings":
            pass

    def home_button_event(self):
        self.select_frame_by_page_name("home")

    def installer_button_event(self):
        self.select_frame_by_page_name("installer")

    def uninstaller_button_event(self):
        self.select_frame_by_page_name("uninstaller")

    def utilities_button_event(self):
        self.select_frame_by_page_name("utilities")

    def toolbox_button_event(self):
        self.select_frame_by_page_name("toolbox")

    def maintenance_button_event(self):
        self.select_frame_by_page_name("maintenance")

    def about_button_event(self):
        self.select_frame_by_page_name("about")

    def settings_button_event(self):
        self.select_frame_by_page_name("settings")
