import customtkinter


class AboutPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout configuration (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("about_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Term of Use Section ---
        self._create_section_label(self.app_translator.translate("term_of_use"))

        # Term of Use Card
        self.term_of_use_card = customtkinter.CTkFrame(
            self.scroll_frame,
            corner_radius=4,
            border_width=1,
            border_color=("gray80", "gray30")
        )
        self.term_of_use_card.pack(fill="x", padx=20, pady=10)

        # Card Header
        self.term_of_use_title_label = customtkinter.CTkLabel(
            self.term_of_use_card,
            text=self.app_translator.translate("term_of_use_title"),
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold")
        )
        self.term_of_use_title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Card Content
        self.term_of_use_content_textbox = customtkinter.CTkTextbox(
            self.term_of_use_card,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            fg_color="transparent",
            wrap="word",
            height=220
        )
        self.term_of_use_content_textbox.pack(fill="x", padx=16, pady=(0, 16))

        term_of_use_content = (
            f"{self.app_translator.translate('term_of_use_content_preface')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_modification_date')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_1_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_1_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_2_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_2_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_3_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_3_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_4_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_4_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_5_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_5_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_6_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_6_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_7_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_7_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_8_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_8_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_9_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_9_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_10_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_10_body')}\n\n"
            f"{self.app_translator.translate('term_of_use_content_11_title')}\n"
            f"{self.app_translator.translate('term_of_use_content_11_body_1')}\n"
            f"{self.app_translator.translate('term_of_use_content_11_body_2')}\n"
            f"{self.app_translator.translate('term_of_use_content_11_body_3')}"
        )
        self.term_of_use_content_textbox.insert("0.0", term_of_use_content)
        self.term_of_use_content_textbox.configure(state="disabled")
        # --- End of Term of Use Section ---

        # --- Privacy Policy Section ---
        self._create_section_label(self.app_translator.translate("privacy_policy"))

        # Privacy Policy Card
        self.privacy_policy_card = customtkinter.CTkFrame(
            self.scroll_frame,
            corner_radius=4,
            border_width=1,
            border_color=("gray80", "gray30")
        )
        self.privacy_policy_card.pack(fill="x", padx=20, pady=10)

        # Card Header
        self.privacy_policy_title_label = customtkinter.CTkLabel(
            self.privacy_policy_card,
            text=self.app_translator.translate("privacy_policy_title"),
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold")
        )
        self.privacy_policy_title_label.pack(anchor="w", padx=16, pady=(16, 8))

        # Card Content
        self.privacy_policy_content_textbox = customtkinter.CTkTextbox(
            self.privacy_policy_card,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            fg_color="transparent",
            wrap="word",
            height=120
        )
        self.privacy_policy_content_textbox.pack(fill="x", padx=16, pady=(0, 16))

        privacy_policy_content = (
            f"{self.app_translator.translate('privacy_policy_content_modification_date')}\n\n"
            f"{self.app_translator.translate('privacy_policy_content_1')}\n\n"
            f"{self.app_translator.translate('privacy_policy_content_2')}"
        )
        self.privacy_policy_content_textbox.insert("0.0", privacy_policy_content)
        self.privacy_policy_content_textbox.configure(state="disabled")
        # --- End of Privacy Policy Section ---


    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))
