from tkinter import messagebox

import customtkinter

from core import (
    AppMetadata,
    get_localization_translators
)
from gui.components import AboutPageWidgets
from handlers.private import ViewLogFile
from handlers.shared import URLHandler
from .base_page_frame import BaseInfoPageFrame


class AboutPage(BaseInfoPageFrame, AboutPageWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="about_page"
        )

        # === App Information Section ===
        self._create_section_label(self.app_translator.translate("app_information"))

        self.app_info_group = self._create_group_frame()

        # --- App Base Info ---
        self._create_info_card(
            self.app_info_group,
            title=AppMetadata.APP_NAME,
            description=AppMetadata.APP_VERSION
        )

        self._create_separator(self.app_info_group)

        # --- Contributors ---
        contributors_container = customtkinter.CTkFrame(self.app_info_group, fg_color="transparent")
        contributors_container.pack(fill="x", padx=10, pady=8)

        # Text Column
        contributors_text_frame = customtkinter.CTkFrame(contributors_container, fg_color="transparent")
        contributors_text_frame.pack(side="left", fill="both", expand=True, padx=5)

        customtkinter.CTkLabel(
            contributors_text_frame,
            text=self.app_translator.translate("contributors"),
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        ).pack(fill="x")

        contributors_list_frame = customtkinter.CTkFrame(contributors_text_frame, fg_color="transparent")
        contributors_list_frame.pack(fill="x", anchor="w")

        for name, contributor_url in AppMetadata.APP_CONTRIBUTORS.items():
            link = customtkinter.CTkLabel(
                contributors_list_frame,
                text=name,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color=("#1f6aa5", "#3a7ebf"),
                cursor="hand2"
            )
            link.pack(side="left", padx=(0, 10))
            link.bind("<Button-1>", lambda e, u=contributor_url: URLHandler.launch_url(
                url=u,
                target_name=f"{name}'s Profile",
                messagebox_error_message="failed_to_open_contributor_url",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
                )
            )

        # --- Separator ---
        self._create_separator(self.app_info_group)

        # --- Translators ---
        translators_list = get_localization_translators(self.app_translator)
        if translators_list:
            translators_container = customtkinter.CTkFrame(self.app_info_group, fg_color="transparent")
            translators_container.pack(fill="x", padx=10, pady=8)

            # Text Column
            translators_text_frame = customtkinter.CTkFrame(translators_container, fg_color="transparent")
            translators_text_frame.pack(side="left", fill="both", expand=True, padx=5)

            customtkinter.CTkLabel(
                translators_text_frame,
                text=self.app_translator.translate("translators"),
                font=customtkinter.CTkFont(family=self.font_family, size=14),
                anchor="w"
            ).pack(fill="x")

            translators_list_frame = customtkinter.CTkFrame(translators_text_frame, fg_color="transparent")
            translators_list_frame.pack(fill="x", anchor="w")

            for username, display_name in translators_list:
                github_profile_url = f"https://github.com/{username}"
                link = customtkinter.CTkLabel(
                    translators_list_frame,
                    text=display_name,
                    font=customtkinter.CTkFont(family=self.font_family, size=12),
                    text_color=("#1f6aa5", "#3a7ebf"),
                    cursor="hand2"
                )
                link.pack(side="left", padx=(0, 10))
                link.bind("<Button-1>", lambda e, u=github_profile_url: URLHandler.launch_url(
                    url=u,
                    target_name=f"{display_name}'s GitHub Profile",
                    messagebox_error_message="failed_to_open_contributor_url",
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                    )
                )
        else:
             self._create_info_card(
                self.app_info_group,
                title=self.app_translator.translate("translators"),
                description=None
            )

        # --- Separator ---
        self._create_separator(self.app_info_group)

        # --- License ---
        self._create_info_card(
            self.app_info_group,
            title=self.app_translator.translate("license"),
            description=AppMetadata.APP_LICENSE_URL,
            description_command=lambda: URLHandler.launch_url(
                url=AppMetadata.APP_LICENSE_URL,
                target_name=f"License",
                messagebox_error_message="failed_to_open_license",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(self.app_info_group)

        # --- Repository ---
        self._create_info_card(
             self.app_info_group,
             title=self.app_translator.translate("repository_url"),
             description=AppMetadata.APP_GITHUB_REPOSITORY_URL,
             description_command=lambda: URLHandler.launch_url(
                url=AppMetadata.APP_GITHUB_REPOSITORY_URL,
                target_name=f"GitHub Repository",
                messagebox_error_message="failed_to_open_github_repository",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(self.app_info_group)

        # --- View Log File ---
        self._create_info_card(
            self.app_info_group,
            title=self.app_translator.translate("view_log_file"),
            description=self.log_file_path,
            description_command=lambda: ViewLogFile.open_log_file(
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of App Information Section ===

        # === Term of Use Section ===
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
            font=customtkinter.CTkFont(family=self.font_family, size=12),
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
        # === End of Term of Use Section ===

        # === Privacy Policy Section ===
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
            font=customtkinter.CTkFont(family=self.font_family, size=12),
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
        # === End of Privacy Policy Section ===

        # === Get Help Section ===
        self._create_section_label(self.app_translator.translate("get_help"))

        self.get_help_group = self._create_group_frame()

        # --- Get Help ---
        self.official_website_button = self._create_info_card(
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
                URLHandler.launch_url(
                    url=AppMetadata.MICROSOFT_PC_MANAGER_URL,
                    target_name="Official Website",
                    messagebox_error_message="failed_to_open_official_website",
                    logger=self.logger,
                    log_file_path=self.log_file_path,
                    app_translator=self.app_translator
                )
            )
        )

        # --- Separator ---
        self._create_separator(self.get_help_group)

        # --- Official Website ---
        self.official_website_button = self._create_info_card(
            self.get_help_group,
            title=self.app_translator.translate("official_website"),
            description=self.app_translator.translate("official_website_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("official_website_button"),
            command=lambda: URLHandler.launch_url(
                url=AppMetadata.MICROSOFT_PC_MANAGER_URL,
                target_name="Official Website",
                messagebox_error_message="failed_to_open_official_website",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of Get Help Section ===
