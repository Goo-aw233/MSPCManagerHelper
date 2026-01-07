import customtkinter

from core.app_settings import AppSettings


class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("settings_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Personalization Section ---
        self._create_section_label(self.app_translator.translate("personalization"))

        # Appearance
        self.theme_map = {
            self.app_translator.translate("follow_system"): "System",
            self.app_translator.translate("light_mode"): "Light",
            self.app_translator.translate("dark_mode"): "Dark"
        }
        self.theme_map_rev = {v: k for k, v in self.theme_map.items()}

        self.personalization_group = self._create_group_frame()
        self.appearance_mode_optionemenu = self._create_setting_card(
            self.personalization_group,
            self.app_translator.translate("appearance"),
            self.app_translator.translate("appearance_description"),
            customtkinter.CTkOptionMenu,
            values=list(self.theme_map.keys()),
            command=self._change_appearance_mode
        )
        self.appearance_mode_optionemenu.set(self.theme_map_rev.get(AppSettings.get_appearance_mode(), self.app_translator.translate("follow_system")))
        
        # Separator
        self._create_separator(self.personalization_group)

        # Follow System Font
        self.follow_system_font_switch = self._create_setting_card(
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
        # --- End of Personalization Section ---

    def _change_appearance_mode(self, new_appearance_mode: str):
        mode = self.theme_map.get(new_appearance_mode)
        if mode:
            customtkinter.set_appearance_mode(mode)
            AppSettings.set_appearance_mode(mode)

    def _change_follow_system_font(self):
        is_enabled = self.follow_system_font_switch.get()
        AppSettings.set_follow_system_font_enabled(is_enabled)

        # Trigger Refresh in MainWindow
        if self.master and self.master.master and hasattr(self.master.master, "refresh_ui"):
            self.master.master.refresh_ui()

    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))

    def _create_group_frame(self):
        frame = customtkinter.CTkFrame(
            self.scroll_frame,
            fg_color=("gray95", "#202020"),
            corner_radius=4,
            border_width=1,
            border_color=("gray90", "#2b2b2b")
        )
        frame.pack(fill="x", padx=20, pady=0)
        return frame

    @staticmethod
    def _create_separator(parent):
        separator = customtkinter.CTkFrame(parent, height=1, fg_color=("gray90", "#2b2b2b"))
        separator.pack(fill="x", padx=10)

    def _create_setting_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)

        # Text Column
        text_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5)

        title_label = customtkinter.CTkLabel(
            text_frame,
            text=title,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        title_label.pack(fill="x")

        if description:
            desc_label = customtkinter.CTkLabel(
                text_frame,
                text=description,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("gray50", "gray70"),
                anchor="w"
            )
            desc_label.pack(fill="x")

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            # For OptionMenu, also set the dropdown font.
            if widget_constructor == customtkinter.CTkOptionMenu and "dropdown_font" not in widget_kwargs:
                widget_kwargs["dropdown_font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
