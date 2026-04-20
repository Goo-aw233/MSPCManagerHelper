import customtkinter

from core import (
    AdvancedStartup,
    AppSettings,
    AppTranslator,
    PrerequisiteChecks
)
from gui.components import SettingsPageWidgets
from .base_page_frame import BaseInfoPageFrame


class SettingsPage(BaseInfoPageFrame, SettingsPageWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="settings_page"
        )

        # === Personalization Section ===
        self._create_section_label(self.app_translator.translate("personalization"))

        # --- Appearance ---
        self.theme_map = {
            self.app_translator.translate("follow_system"): "System",
            self.app_translator.translate("light_mode"): "Light",
            self.app_translator.translate("dark_mode"): "Dark"
        }
        self.theme_map_rev = {v: k for k, v in self.theme_map.items()}

        self.personalization_group = self._create_group_frame()

        self.appearance_mode_optionemenu = self._create_settings_card(
            self.personalization_group,
            self.app_translator.translate("appearance"),
            self.app_translator.translate("appearance_description"),
            customtkinter.CTkOptionMenu,
            values=list(self.theme_map.keys()),
            command=self._change_appearance_mode
        )
        self.appearance_mode_optionemenu.set(
            self.theme_map_rev.get(AppSettings.get_appearance_mode(), self.app_translator.translate("follow_system")))
        
        # --- Separator ---
        self._create_separator(self.personalization_group)

        # --- Follow System Font ---
        self.follow_system_font_switch = self._create_settings_card(
            self.personalization_group,
            self.app_translator.translate("follow_system_font_settings"),
            self.app_translator.translate("follow_system_font_settings_description"),
            customtkinter.CTkSwitch,
            text=self.font_family,
            command=self._change_follow_system_font
        )

        if AppSettings.is_follow_system_font_enabled():
            self.follow_system_font_switch.select()
        else:
            self.follow_system_font_switch.deselect()
        # === End of Personalization Section ===

        # === Language Section ===
        self._create_section_label(self.app_translator.translate("language"))

        self.language_map = {
            self.app_translator.translate("lang_en-us"): "en-us",
            self.app_translator.translate("lang_zh-cn"): "zh-cn",
            self.app_translator.translate("lang_zh-tw"): "zh-tw"
        }
        self.language_map_rev = {v: k for k, v in self.language_map.items()}

        self.language_group = self._create_group_frame()

        self.language_optionmenu = self._create_settings_card(
            self.language_group,
            self.app_translator.translate("app_display_language"),
            self.app_translator.translate("app_display_language_description"),
            customtkinter.CTkOptionMenu,
            values=list(self.language_map.keys()),
            command=self._change_language
        )

        current_locale = getattr(self.master.master, "language", "en-us")
        self.language_optionmenu.set(self.language_map_rev.get(current_locale, "English"))
        # === End of Language Section ===

        # === Preferences ===
        self._create_section_label(self.app_translator.translate("preferences"))

        self.preferences_group = self._create_group_frame()

        # --- Support Developer ---
        self.support_developer_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("support_developer"),
            self.app_translator.translate("support_developer_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "button_on") if AppSettings.is_support_developer_enabled() else self.app_translator.translate(
                "button_off"),
            command=self._change_support_developer
        )

        if AppSettings.is_support_developer_enabled():
            self.support_developer_switch.select()
        else:
            self.support_developer_switch.deselect()

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Original Links ---
        self.original_links_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("original_links"),
            self.app_translator.translate("original_links_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "button_on") if AppSettings.is_original_links_enabled() else self.app_translator.translate(
                "button_off"),
            command=self._change_original_links
        )
        if AppSettings.is_original_links_enabled():
            self.original_links_switch.select()
        else:
            self.original_links_switch.deselect()

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Compatibility Mode ---
        self.compatibility_mode_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("compatibility_mode"),
            self.app_translator.translate("compatibility_mode_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "button_on") if AppSettings.is_compatibility_mode_enabled() else self.app_translator.translate(
                "button_off"),
            command=self._change_compatibility_mode
        )
        if AppSettings.is_compatibility_mode_enabled():
            self.compatibility_mode_switch.select()
        else:
            self.compatibility_mode_switch.deselect()

        # --- Separator ---
        self._create_separator(self.preferences_group)

        # --- Use Internal Viewer ---
        self.use_internal_viewer_switch = self._create_settings_card(
            self.preferences_group,
            self.app_translator.translate("use_internal_viewer"),
            self.app_translator.translate("use_internal_viewer_description"),
            customtkinter.CTkSwitch,
            text=self.app_translator.translate(
                "button_on") if AppSettings.is_use_internal_viewer_enabled() else self.app_translator.translate(
                "button_off"),
            command=self._change_use_internal_viewer
        )
        if AppSettings.is_use_internal_viewer_enabled():
            self.use_internal_viewer_switch.select()
        else:
            self.use_internal_viewer_switch.deselect()
        # === End of Preferences ===

        # === Advanced ===
        if AdvancedStartup.is_administrator() and (AdvancedStartup.is_debugmode() or AdvancedStartup.is_devmode()):
            self._create_section_label(self.app_translator.translate("settings_page_advanced_section_title"))

            self.advanced_group = self._create_group_frame()

            # --- Take Ownership ---
            self.take_ownership_card = self._create_settings_card(
                self.advanced_group,
                self.app_translator.translate("take_ownership"),
                self.app_translator.translate("take_ownership_description"),
                customtkinter.CTkSwitch,
                text=self.app_translator.translate(
                    "button_on") if AppSettings.is_take_ownership_enabled() else self.app_translator.translate(
                    "button_off"),
                command=self._change_take_ownership
            )
            if AppSettings.is_take_ownership_enabled():
                self.take_ownership_card.select()
            else:
                self.take_ownership_card.deselect()
        # === End of Advanced ===


    def _change_appearance_mode(self, new_appearance_mode: str):
        mode = self.theme_map.get(new_appearance_mode)
        if mode:
            customtkinter.set_appearance_mode(mode)
            AppSettings.set_appearance_mode(mode)

            # Trigger Refresh Task in MainWindow
            if self.master and self.master.master and hasattr(self.master.master, "refresh_ui"):
                self.master.master.refresh_ui()

    def _change_follow_system_font(self):
        is_enabled = self.follow_system_font_switch.get()
        AppSettings.set_follow_system_font_enabled(is_enabled)

        # Trigger Refresh Task in MainWindow
        if self.master and self.master.master and hasattr(self.master.master, "refresh_ui"):
            self.master.master.refresh_ui()

    def _change_language(self, new_language: str):
        locale = self.language_map.get(new_language)
        if locale and self.master and self.master.master:
            self.logger.info(f"Language Switched to: {locale}")
            main_window = self.master.master
            main_window.language = locale
            main_window.app_translator = AppTranslator(locale)
            PrerequisiteChecks.app_translator = main_window.app_translator

            # Trigger Refresh Task in MainWindow
            if hasattr(main_window, "refresh_ui"):
                main_window.refresh_ui()

    def _change_support_developer(self):
        is_enabled = self.support_developer_switch.get()
        AppSettings.set_support_developer_enabled(is_enabled)
        self.support_developer_switch.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off")
        )

    def _change_compatibility_mode(self):
        is_enabled = self.compatibility_mode_switch.get()
        AppSettings.set_compatibility_mode_enabled(is_enabled)
        self.compatibility_mode_switch.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off")
        )

    def _change_original_links(self):
        is_enabled = self.original_links_switch.get()
        AppSettings.set_original_links_enabled(is_enabled)
        self.original_links_switch.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off")
        )

    def _change_use_internal_viewer(self):
        is_enabled = self.use_internal_viewer_switch.get()
        AppSettings.set_use_internal_viewer_enabled(is_enabled)
        self.use_internal_viewer_switch.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off")
        )

    def _change_take_ownership(self):
        is_enabled = self.take_ownership_card.get()
        AppSettings.set_take_ownership_enabled(is_enabled)
        self.take_ownership_card.configure(
            text=self.app_translator.translate("button_on") if is_enabled else self.app_translator.translate(
                "button_off")
        )

        # Trigger Refresh Task in MainWindow
        if self.master and self.master.master and hasattr(self.master.master, "refresh_ui"):
            self.master.master.refresh_ui()
