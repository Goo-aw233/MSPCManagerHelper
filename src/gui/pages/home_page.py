import queue
import sys
import threading

import customtkinter

from core import (
    AdvancedStartup,
    AppMetadata,
    AppSettings,
    GetMSPCMVersion,
    PrerequisiteChecks
)
from gui.components import HomePageWidgets
from handlers.private import EnableLongPaths, RestartAsAdministrator
from handlers.shared import StartMSPCM, StartMSPCMBeta, URILauncher
from .base_page_frame import BaseInfoPageFrame


class HomePage(BaseInfoPageFrame, HomePageWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="home_page"
        )

        # Create a Thread-Safe Queue
        self.result_queue = queue.Queue()
        self.logger.debug("Initialized result_queue for thread-safe UI updates.")

        # === Welcome Section ===
        self._create_section_label(self.app_translator.translate("welcome_title"))

        self.welcome_group = self._create_group_frame()

        self._create_info_textbox_card(
            self.welcome_group,
            f"{self.app_translator.translate('welcome_to')} {AppMetadata.APP_NAME}",
            self.app_translator.translate("welcome_message"),
            activate_scrollbars=True,
            enable_text_selection=False,
            min_height=50
        )
        # === End of Welcome Section ===

        # === Microsoft PC Manager Version Info Section ===
        self.refresh_version_button = self._create_section_label_with_button(
            self.app_translator.translate("mspcm_version_info"),
            f"↻    {self.app_translator.translate('refresh_button')}",
            self._refresh_mspcm_version_info
        )

        self.mspcm_version_group = self._create_group_frame()

        self._load_mspcm_version_info()
        # === End of Microsoft PC Manager Version Info Section ===

        # === Windows Specifications Section ===
        self._create_section_label(self.app_translator.translate("windows_specifications"))

        self.windows_specifications_group = self._create_group_frame()

        # --- Load Windows Installation Information ---
        self._load_windows_installation_info()

        # --- System Checks ---
        self._load_system_checks()
        # === End of Windows Specifications Section ===

        # === Advanced Section ===
        self._create_section_label(self.app_translator.translate("home_page_advanced_section_title"))

        self.exit_group = self._create_group_frame()

        # --- Run as Administrator ---
        self._create_settings_card(
            self.exit_group,
            self.app_translator.translate("run_as_administrator"),
            self.app_translator.translate("run_as_administrator_description"),
            customtkinter.CTkButton,
            text=self.app_translator.translate("run_as_administrator_button"),
            command=lambda: RestartAsAdministrator.restart_as_administrator(
                AdvancedStartup, logger=self.logger,
                app_translator=self.app_translator,
                log_file_path=self.log_file_path
            ),
            state="disabled" if AdvancedStartup.is_administrator() else "normal"
        )

        # --- Long Paths ---
        if not PrerequisiteChecks.check_if_long_paths_enabled():
            # Separator
            self.long_paths_separator = self._create_separator(self.exit_group)

            self.long_paths_button = self._create_settings_card(
                self.exit_group,
                self.app_translator.translate("long_paths"),
                self.app_translator.translate("long_paths_description"),
                customtkinter.CTkButton,
                text=self.app_translator.translate("enable_long_paths_button"),
                command=self._on_long_paths_click,
                state="normal" if AdvancedStartup.is_administrator() else "disabled"
            )

        # --- Separator ---
        self._create_separator(self.exit_group)

        # --- Cleanup After Exit ---
        self.cleanup_after_exit_checkbox = self._create_settings_card(
            self.exit_group,
            self.app_translator.translate("cleanup_after_exit"),
            self.app_translator.translate("cleanup_after_exit_description"),
            customtkinter.CTkCheckBox,
            text=self.app_translator.translate(
                "button_on") if AppSettings.is_cleanup_after_exit_enabled() else self.app_translator.translate(
                "button_off"),
            command=self._on_cleanup_after_exit_toggled
        )
        if AppSettings.is_cleanup_after_exit_enabled():
            self.cleanup_after_exit_checkbox.select()
        else:
            self.cleanup_after_exit_checkbox.deselect()

        # --- Separator ---
        self._create_separator(self.exit_group)

        # --- Exit ---
        self._create_settings_card(
            self.exit_group,
            self.app_translator.translate("exit_section_title"),
            self.app_translator.translate("exit_app_description"),
            customtkinter.CTkButton,
            text=self.app_translator.translate("exit_app_button"),
            command=self._exit_app
        )
        # === End of Advanced Section ===

        # === After Initialization Tasks ===
        # Start the Main Thread's Periodic Check Loop
        # (Place at the end of __init__ to avoid loading before the GUI is ready.)
        self.logger.debug("Starting the main thread's periodic check loop.")
        self._check_queue_loop()
        # === End of After Initialization Tasks ===


    def _refresh_mspcm_version_info(self):
        # Clear existing widgets in the group frame.
        for widget in self.mspcm_version_group.winfo_children():
            widget.destroy()

        # Reload Version Info
        self._load_mspcm_version_info()

    def _load_mspcm_version_info(self):
        # Disable Refresh Button While Loading
        if hasattr(self, 'refresh_version_button'):
            self.refresh_version_button.configure(state="disabled")

        # Show Loading Message
        self._create_info_textbox_card(
            self.mspcm_version_group,
            self.app_translator.translate("mspcm_version_is"),
            self.app_translator.translate("loading")
        )

        # Start a Thread to Fetch the Version Info
        self.logger.debug("Starting background thread to fetch Microsoft PC Manager versions.")
        threading.Thread(target=self._fetch_mspcm_versions, daemon=True).start()

    def _fetch_mspcm_versions(self):
        # Microsoft PC Manager Version Info
        mspcm_version = GetMSPCMVersion.get_microsoft_pc_manager_version()

        # Microsoft PC Manager Beta Version Info
        mspcm_beta_version = GetMSPCMVersion.get_microsoft_pc_manager_beta_version()

        try:
            self.logger.debug(
                f"Background Thread Fetched Versions - Stable: {mspcm_version}, Beta: {mspcm_beta_version}")
            self.result_queue.put((mspcm_version, mspcm_beta_version))
            self.logger.debug("Successfully placed version information into result_queue.")
        except Exception as e:
            self.logger.debug(f"Failed to Put Data Into result_queue: {e}")
            pass

    def _check_queue_loop(self):
        try:
            # Try to get data from the queue (non-blocking).
            while True:
                # After obtaining the data, update the UI on the main thread.
                mspcm_version, mspcm_beta_version = self.result_queue.get_nowait()
                self.logger.debug("Retrieved version data from queue. Dispatching UI update.")
                self._update_mspcm_version_ui(mspcm_version, mspcm_beta_version)
        except queue.Empty:
            pass
        finally:
            # Every 100 ms, call itself to keep the loop running.
            self.after(100, self._check_queue_loop)

    def _update_mspcm_version_ui(self, mspcm_version, mspcm_beta_version):
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return

        # Enable Refresh Button After Loading
        if hasattr(self, 'refresh_version_button'):
            self.refresh_version_button.configure(state="normal")

        # Clear Loading Message
        for widget in self.mspcm_version_group.winfo_children():
            widget.destroy()

        # Microsoft PC Manager Version Info
        if mspcm_version:
            self.mspcm_version_card = self._create_info_textbox_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_version_is"),
                f"{self.app_translator.translate('mspcm_version_is')}: {mspcm_version}",
                customtkinter.CTkButton,
                text=self.app_translator.translate("start_mspcm_button"),
                command=lambda: StartMSPCM.start_mspcm(
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )
            self.logger.info(f"Loaded Microsoft PC Manager Version: {mspcm_version}")
        else:
            self.mspcm_version_card = self._create_info_textbox_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_version_is"),
                self.app_translator.translate("failed_to_get_mspcm_version_info")
            )
            self.logger.warning("Failed to load Microsoft PC Manager version.")

        # Microsoft PC Manager Beta Version Info
        if mspcm_beta_version:
            self._create_separator(self.mspcm_version_group)

            self.mspcm_beta_version_card = self._create_info_textbox_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_beta_version_is"),
                f"{self.app_translator.translate('mspcm_beta_version_is')}: {mspcm_beta_version}",
                customtkinter.CTkButton,
                text=self.app_translator.translate("start_mspcm_beta_button"),
                command=lambda: StartMSPCMBeta.start_mspcm_beta(
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )
            self.logger.info(f"Loaded Microsoft PC Manager Public Beta Version: {mspcm_beta_version}")

    def _load_windows_installation_info(self):
        windows_info = PrerequisiteChecks.get_windows_installation_information()

        if windows_info:
            self._create_info_textbox_card(
                self.windows_specifications_group,
                self.app_translator.translate("windows_installation_info"),
                windows_info,
                customtkinter.CTkButton,
                enable_text_selection=True,
                text=self.app_translator.translate("about_button"),
                command=lambda: URILauncher.launch_uri(
                    uri="ms-settings:about",
                    target_name="About Windows",
                    messagebox_error_message="failed_to_open_about_windows",
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )
        else:
            self._create_info_textbox_card(
                self.windows_specifications_group,
                self.app_translator.translate("windows_installation_info"),
                self.app_translator.translate("failed_to_load_windows_installation_info"),
                customtkinter.CTkButton,
                enable_text_selection=True,
                text=self.app_translator.translate("about_button"),
                command=lambda: URILauncher.launch_uri(
                    uri="ms-settings:about",
                    target_name="About Windows",
                    messagebox_error_message="failed_to_open_about_windows",
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )

    def _load_system_checks(self):
        attention_messages = []

        if not PrerequisiteChecks.check_windows_minimum_requirements():
            attention_messages.append(self.app_translator.translate("current_system_not_meets_system_requirements"))
        else:
            attention_messages.append(self.app_translator.translate("current_system_meets_system_requirements"))

        if PrerequisiteChecks.check_admin_approval_mode():
            attention_messages.append(self.app_translator.translate("administrator_protection_is_enabled"))

        if PrerequisiteChecks.check_windows_server_levels():
            attention_messages.append(self.app_translator.translate("windows_server_installation_type_is_core"))

        if attention_messages:
            self._create_separator(self.windows_specifications_group)
            self._create_info_textbox_card(
                self.windows_specifications_group,
                self.app_translator.translate("attention"),
                "\n\n".join(attention_messages),
                activate_scrollbars=True,
                enable_text_selection=False,
            )

    def _on_long_paths_click(self):
        EnableLongPaths.enable_long_paths(
            logger=self.logger,
            log_file_path=self.log_file_path,
            app_translator=self.app_translator
        )

        if PrerequisiteChecks.check_if_long_paths_enabled():
            if hasattr(self, 'long_paths_separator') and self.long_paths_separator.winfo_exists():
                self.long_paths_separator.destroy()
            if hasattr(self, 'long_paths_button') and self.long_paths_button.winfo_exists():
                # The button is inside the card container (CTkFrame). Destroy the container.
                self.long_paths_button.master.destroy()

    def _on_cleanup_after_exit_toggled(self):
        AppSettings.toggle_cleanup_after_exit()
        is_enabled = AppSettings.is_cleanup_after_exit_enabled()
        self.cleanup_after_exit_checkbox.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off"))

    def _exit_app(self):
        self.logger.info("The app is exiting via the exit button...")
        sys.exit(0)
