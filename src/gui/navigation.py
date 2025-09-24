import customtkinter


class NavigationFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, on_page_change, font_family=None, translator=None, *args, **kwargs):
        super().__init__(master, corner_radius=0, *args, **kwargs)
        self.on_page_change = on_page_change
        self.font_family = font_family
        self.translator = translator

        self.navigation_frame_label = customtkinter.CTkLabel(
            self,
            text="MSPCManagerHelper",
            compound="left",
            font=(self.font_family, 15, "bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.buttons = []
        # 存储翻译键 (translation key) 和页面名称
        self.button_info = [
            ("home_page", "home_page"),
            ("maintenance_page", "maintenance_page"),
            ("installation_features_page", "installation_features_page"),
            ("uninstallation_features_page", "uninstallation_features_page"),
            ("utils_page", "utils_page"),
            ("toolbox_page", "toolbox_page"),
            ("about_page", "about_page"),
        ]
        for idx, (translation_key, page_name) in enumerate(self.button_info, start=1):
            # 直接翻译键，不再使用 .lower()
            btn_text = self.translator.translate(translation_key) if self.translator else translation_key
            btn = customtkinter.CTkButton(
                self, corner_radius=4, height=40, border_spacing=10, text=btn_text,
                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                anchor="center", font=(self.font_family, 14),
                command=lambda n=page_name: self.select_page(n)
            )
            btn.grid(row=idx, column=0, sticky="ew", padx=16.5, pady=2)
            self.buttons.append((page_name, btn))

        self.grid_rowconfigure(len(self.button_info) + 1, weight=1)
        self.selected_page = None
        # 不自动 select_page("home")，交由主窗口控制

    def select_page(self, name):
        for n, btn in self.buttons:
            btn.configure(fg_color=("gray75", "gray25") if n == name else "transparent")
        self.selected_page = name
        if self.on_page_change:
            self.on_page_change(name)
