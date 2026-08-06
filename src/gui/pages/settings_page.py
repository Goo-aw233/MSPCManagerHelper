import customtkinter
from windows_toasts import Toast, WindowsToaster

from core import (
    AdvancedStartup,
    AppMetadata,
    AppSettings,
    AppTranslator,
    PrerequisiteChecks
)
from gui.components import (
    SettingsPageWidgets,
    task_coordinator
)
from handlers.shared import URILauncher
from .base_page_frame import BaseInfoPageFrame


class SettingsPage(BaseInfoPageFrame, SettingsPageWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.settings",
        )
        self._main_window = parent.master

        # Flags for deferring UI refresh while an operation is running.
        self._refresh_ui_pending = False
        self._refresh_deferred_toast_shown = False

        # === Personalization Section ===
        self._create_section_label(self.app_translator.translate("pages.settings.personalization"))

        self.personalization_group = self._create_group_frame()

        # --- Appearance ---
        self.theme_map = {
            self.app_translator.translate("pages.settings.follow_system"): "System",
            self.app_translator.translate("pages.settings.light_mode"): "Light",
            self.app_translator.translate("pages.settings.dark_mode"): "Dark"
        }
        self.theme_map_rev = {v: k for k, v in self.theme_map.items()}

        self.appearance_mode_optionemenu = self._create_settings_card(
            self.personalization_group,
            self.app_translator.translate("pages.settings.appearance"),
            self.app_translator.translate("pages.settings.appearance_description"),
            customtkinter.CTkOptionMenu,
            values=list(self.theme_map.keys()),
            command=self._change_appearance_mode
        )
        self.appearance_mode_optionemenu.set(self.theme_map_rev.get(AppSettings.get_appearance_mode(),
                                                                    self.app_translator.translate(
                                                                        "pages.settings.follow_system")))

        # --- Separator ---
        self._create_separator(self.personalization_group)

        # --- Follow System Font ---
        self.follow_system_font_switch = self._create_settings_card(
            self.personalization_group,
            self.app_translator.translate("pages.settings.follow_system_font_settings"),
            self.app_translator.translate("pages.settings.follow_system_font_settings_description"),
            customtkinter.CTkSwitch,
            text=self.font_family,
            command=self._change_follow_system_font
        )

        self._apply_switch_state(self.follow_system_font_switch, AppSettings.is_follow_system_font_enabled())
        # === End of Personalization Section ===

        # === Language Section ===
        self._create_section_label(self.app_translator.translate("pages.settings.language"))

        self.language_group = self._create_group_frame()

        #--- App Display Language ---
        self.language_map = {
            self.app_translator.translate("metadata.i18n.locales.en-US"): "en-us",
            self.app_translator.translate("metadata.i18n.locales.zh-CN"): "zh-cn",
            self.app_translator.translate("metadata.i18n.locales.zh-TW"): "zh-tw"
        }
        self.language_map_rev = {v: k for k, v in self.language_map.items()}

        self.language_optionmenu = self._create_settings_card(
            self.language_group,
            self.app_translator.translate("pages.settings.app_display_language"),
            self.app_translator.translate("pages.settings.app_display_language_description"),
            customtkinter.CTkOptionMenu,
            values=list(self.language_map.keys()),
            command=self._change_language
        )

        current_locale = getattr(self._main_window, "language", "en-us")
        self.language_optionmenu.set(
            self.language_map_rev.get(current_locale, self.app_translator.translate("metadata.i18n.locales.en-US")))
        # === End of Language Section ===

        # === Reload Section ===
        self._create_section_label(self.app_translator.translate("pages.settings.reload"))

        self.reload_group = self._create_group_frame()

        # --- Reload UI ---
        self.reload_ui_button = self._create_settings_card(
            self.reload_group,
            self.app_translator.translate("pages.settings.reload_ui"),
            self.app_translator.translate("pages.settings.reload_ui_description"),
            customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.refresh"),
            command=self._request_refresh_ui
        )
        # === End of Reload Section ===

        # === Preferences ===
        self._create_section_label(self.app_translator.translate("pages.settings.preferences"))

        self.preferences_group = self._create_group_frame()

        # --- Support Developer ---
        self.support_developer_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("pages.settings.support_developer"),
            self.app_translator.translate("pages.settings.support_developer_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "pages.common.on") if AppSettings.is_support_developer_enabled() else self.app_translator.translate(
                "pages.common.off"),
            command=self._change_support_developer
        )

        self._apply_switch_state(self.support_developer_switch, AppSettings.is_support_developer_enabled())

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Original Links ---
        self.original_links_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("pages.settings.original_links"),
            self.app_translator.translate("pages.settings.original_links_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "pages.common.on") if AppSettings.is_original_links_enabled() else self.app_translator.translate(
                "pages.common.off"),
            command=self._change_original_links
        )
        self._apply_switch_state(self.original_links_switch, AppSettings.is_original_links_enabled())

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Compatibility Mode ---
        self.compatibility_mode_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("pages.settings.compatibility_mode"),
            self.app_translator.translate("pages.settings.compatibility_mode_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "pages.common.on") if AppSettings.is_compatibility_mode_enabled() else self.app_translator.translate(
                "pages.common.off"),
            command=self._change_compatibility_mode
        )
        self._apply_switch_state(self.compatibility_mode_switch, AppSettings.is_compatibility_mode_enabled())

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Use Internal Viewer ---
        self.use_internal_viewer_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("pages.settings.use_internal_viewer"),
            self.app_translator.translate("pages.settings.use_internal_viewer_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "pages.common.on") if AppSettings.is_use_internal_viewer_enabled() else self.app_translator.translate(
                "pages.common.off"),
            command=self._change_use_internal_viewer
        )
        self._apply_switch_state(self.use_internal_viewer_switch, AppSettings.is_use_internal_viewer_enabled())
        # === End of Preferences ===

        # === Privacy & Security ===
        self._create_section_label(self.app_translator.translate("pages.settings.privacy_settings"))

        self.privacy_settings_group = self._create_group_frame()

        # --- Privacy Settings ---
        self.privacy_settings_button = self._create_settings_card(
            self.privacy_settings_group,
            self.app_translator.translate("pages.settings.privacy_settings"),
            self.app_translator.translate("pages.settings.privacy_settings_description"),
            customtkinter.CTkButton,
            text=self.app_translator.translate("pages.settings.privacy_and_security"),
            command=lambda: URILauncher.launch_uri(
                uri="ms-settings:privacy",
                target_name="Privacy & Security Settings",
                messagebox_error_message="pages.settings.open_privacy_settings_error",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of Privacy & Security ===

        # === Advanced ===
        if AdvancedStartup.is_administrator() and (AdvancedStartup.is_debugmode() or AdvancedStartup.is_devmode()):
            self._create_section_label(self.app_translator.translate("pages.settings.advanced"))

            self.advanced_group = self._create_group_frame()

            # --- Take Ownership ---
            self.take_ownership_card = self._create_settings_card(
                self.advanced_group,
                self.app_translator.translate("pages.settings.take_ownership"),
                self.app_translator.translate("pages.settings.take_ownership_description"),
                customtkinter.CTkSwitch,
                text=self.app_translator.translate(
                    "pages.common.on") if AppSettings.is_take_ownership_enabled() else self.app_translator.translate(
                    "pages.common.off"),
                command=self._change_take_ownership
            )
            self._apply_switch_state(self.take_ownership_card, AppSettings.is_take_ownership_enabled())
        # === End of Advanced ===


    def _change_appearance_mode(self, new_appearance_mode: str):
        mode = self.theme_map.get(new_appearance_mode)
        if mode:
            customtkinter.set_appearance_mode(mode)
            AppSettings.set_appearance_mode(mode)

            # Trigger Refresh Task in MainWindow
            self._request_refresh_ui()

    def _change_follow_system_font(self):
        is_enabled = self.follow_system_font_switch.get()
        AppSettings.set_follow_system_font_enabled(is_enabled)

        # Trigger Refresh Task in MainWindow
        self._request_refresh_ui()

    def _change_language(self, new_language: str):
        locale = self.language_map.get(new_language)
        if locale and self._main_window:
            self.logger.info(f"Language Switched to: {locale}")
            main_window = self._main_window
            main_window.language = locale
            main_window.app_translator = AppTranslator(locale)
            PrerequisiteChecks.app_translator = main_window.app_translator

            # Trigger Refresh Task in MainWindow
            self._request_refresh_ui()

    def _change_support_developer(self):
        self._toggle_switch_setting(self.support_developer_switch, AppSettings.set_support_developer_enabled)

    def _change_compatibility_mode(self):
        self._toggle_switch_setting(self.compatibility_mode_switch, AppSettings.set_compatibility_mode_enabled)

    def _change_original_links(self):
        self._toggle_switch_setting(self.original_links_switch, AppSettings.set_original_links_enabled)

    def _change_use_internal_viewer(self):
        self._toggle_switch_setting(self.use_internal_viewer_switch, AppSettings.set_use_internal_viewer_enabled)

    def _change_take_ownership(self):
        self._toggle_switch_setting(self.take_ownership_card, AppSettings.set_take_ownership_enabled)

        # Trigger Refresh Task in MainWindow
        self._request_refresh_ui()

    @staticmethod
    def _apply_switch_state(switch, enabled):
        if enabled:
            switch.select()
        else:
            switch.deselect()

    def _toggle_switch_setting(self, switch, setting_setter):
        is_enabled = switch.get()
        setting_setter(is_enabled)
        switch.configure(
            text=self.app_translator.translate("pages.common.on") if is_enabled else self.app_translator.translate(
                "pages.common.off")
        )

    def _request_refresh_ui(self):
        main_window = self._main_window
        if main_window and hasattr(main_window, "refresh_ui"):
            if task_coordinator.is_busy():
                # Do not rebuild the UI while an operation is running; defer
                # refresh until the operation completes and notify the user.
                if not self._refresh_deferred_toast_shown:
                    self._refresh_deferred_toast_shown = True
                    self._notify_refresh_deferred()
                self._schedule_refresh_ui_after_operation()
                return
            # Reset the toast flag once the UI is actually refreshed again.
            self._refresh_deferred_toast_shown = False
            main_window.after(0, main_window.refresh_ui)

    def _notify_refresh_deferred(self):
        try:
            toaster = WindowsToaster(AppMetadata.APP_NAME)
            refresh_deferred_toast = Toast()
            refresh_deferred_toast.text_fields = [
                self.app_translator.translate("pages.settings.refresh_deferred_title"),
                self.app_translator.translate("pages.settings.refresh_deferred_message")
            ]
            refresh_deferred_toast.tag = "refresh_deferred_toast"
            toaster.show_toast(refresh_deferred_toast)
        except Exception as e:
            self.logger.warning(f"Failed to Show Refresh-deferred Toast Notification: {e}")

    def _schedule_refresh_ui_after_operation(self):
        if self._refresh_ui_pending:
            return
        self._refresh_ui_pending = True

        def _poll():
            self._refresh_ui_pending = False
            if task_coordinator.is_busy():
                self._schedule_refresh_ui_after_operation()
                return
            self._request_refresh_ui()

        self.after(200, _poll)
