import customtkinter

from core.program_settings import ProgramSettings


class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, master, translator, font_family: str, on_theme_change=None):
        super().__init__(master, fg_color="transparent", corner_radius=0)
        self.translator = translator
        self.font_family = font_family
        self.on_theme_change = on_theme_change

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_appearance_section()

    def _build_header(self):
        header = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 12))
        header.grid_columnconfigure(1, weight=1)

        title_label = customtkinter.CTkLabel(
            header,
            text=self.translator.translate("settings_page"),
            font=(self.font_family, 28, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w")

        subtitle_label = customtkinter.CTkLabel(
            header,
            text=self.translator.translate("settings_page_subtitle"),
            font=(self.font_family, 14),
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        hint_chip = customtkinter.CTkLabel(
            header,
            text=self.translator.translate("settings_page_hint"),
            font=(self.font_family, 12),
            fg_color="#e5f1fb",
            text_color="#0f6cbd",
            corner_radius=8,
            padx=12,
            pady=6,
        )
        hint_chip.grid(row=0, column=1, rowspan=2, sticky="e")

    def _build_appearance_section(self):
        content = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        content.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        content.grid_columnconfigure(0, weight=1)

        card = customtkinter.CTkFrame(content, fg_color=("white", "#1f1f1f"), corner_radius=12)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        section_title = customtkinter.CTkLabel(
            card,
            text=self.translator.translate("program_theme"),
            font=(self.font_family, 18, "bold"),
        )
        section_title.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 6))

        section_desc = customtkinter.CTkLabel(
            card,
            text=self.translator.translate("program_theme_desc"),
            font=(self.font_family, 12),
            text_color=("#404040", "#c7c7c7"),
            wraplength=620,
            justify="left",
        )
        section_desc.grid(row=1, column=0, sticky="w", padx=18)

        options_frame = customtkinter.CTkFrame(card, fg_color="transparent")
        options_frame.grid(row=2, column=0, sticky="w", padx=14, pady=(14, 16))

        option_specs = [
            ("match_system_theme", "auto"),
            ("light_theme", "light"),
            ("dark_theme", "dark"),
        ]

        option_labels = []
        self._theme_value_map = {}
        for key, value in option_specs:
            label = self.translator.translate(key)
            option_labels.append(label)
            self._theme_value_map[label] = value

        self.theme_selector = customtkinter.CTkSegmentedButton(
            options_frame,
            values=option_labels,
            command=self._handle_theme_change,
            font=(self.font_family, 12, "bold"),
        )
        self.theme_selector.grid(row=0, column=0, sticky="w")

        self._set_initial_theme(option_labels)

    def _set_initial_theme(self, option_labels):
        current_mode = ProgramSettings.get_theme_mode()
        label = next((lbl for lbl, mode in self._theme_value_map.items() if mode == current_mode), None)
        if not label and option_labels:
            label = option_labels[0]
        if label:
            self.theme_selector.set(label)

    def _handle_theme_change(self, selection: str):
        mode = self._theme_value_map.get(selection, "auto")
        ProgramSettings.set_theme_mode(mode)
        if self.on_theme_change:
            self.on_theme_change(mode)
