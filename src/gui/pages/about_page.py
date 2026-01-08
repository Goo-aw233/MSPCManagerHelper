from tkinter import messagebox

import customtkinter

from core.app_logger import AppLogger
from gui.pages.events import *


class AboutPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.logger = AppLogger.get_logger()
        self.log_file_path = AppLogger.get_log_file_path()
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
            height=130
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
            height=130
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

        # --- Privacy Settings Section ---
        self._create_section_label(self.app_translator.translate("privacy_settings"))

        self.privacy_settings_group = self._create_group_frame()

        # --- Privacy Settings ---
        self.privacy_settings_button = self._create_settings_card(
            self.privacy_settings_group,
            title=self.app_translator.translate("privacy_settings"),
            description=self.app_translator.translate("privacy_settings_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("privacy_settings_button"),
            command=lambda: OnPrivacySettingsButtonClick.open_privacy_settings(logger=self.logger,
                                                                               log_file_path=self.log_file_path,
                                                                               app_translator=self.app_translator)
        )
        # --- End of Privacy Settings Section ---

        # --- Get Help Section ---
        self._create_section_label(self.app_translator.translate("get_help"))

        self.get_help_group = self._create_group_frame()

        # --- Get Help ---
        self.official_website_button = self._create_settings_card(
            self.get_help_group,
            title=self.app_translator.translate("get_help"),
            description=self.app_translator.translate("get_help_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("get_help_button"),
            command=lambda: (
                messagebox.showinfo(
                    title=self.app_translator.translate("information"),
                    message=self.app_translator.translate("redirect_to_official_website_to_get_help")
                ),
                OnOfficialWebsiteButtonClick.open_official_website(
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )
        )

        # Separator
        self._create_separator(self.get_help_group)

        # --- Official Website ---
        self.official_website_button = self._create_settings_card(
            self.get_help_group,
            title=self.app_translator.translate("official_website"),
            description=self.app_translator.translate("official_website_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("official_website_button"),
            command=lambda: OnOfficialWebsiteButtonClick.open_official_website(logger=self.logger,
                                                                               log_file_path=self.log_file_path,
                                                                               app_translator=self.app_translator)
        )
        # --- End of Get Help Section ---

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

    def _create_settings_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
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

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
