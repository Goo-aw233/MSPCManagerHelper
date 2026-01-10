import customtkinter

from core.app_logger import AppLogger
from core.app_metadata import AppMetadata
from core.get_mspcm_version import GetMSPCMVersion
from core.system_checks import PrerequisiteChecks
from gui.pages.events import OnAboutWindowsButtonClick, StartMSPCM, StartMSPCMBeta


class HomePage(customtkinter.CTkFrame):
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
            text=self.app_translator.translate("home_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Welcome Section ---
        self._create_section_label(self.app_translator.translate("welcome_title"))

        self.welcome_group = self._create_group_frame()

        # Welcome Section Header
        self.welcome_header_frame = customtkinter.CTkFrame(self.welcome_group, fg_color="transparent")
        self.welcome_header_frame.pack(fill="x", padx=16, pady=(16, 12))

        self.welcome_title_label = customtkinter.CTkLabel(
            self.welcome_header_frame,
            text=f"{self.app_translator.translate('welcome_to')} {AppMetadata.APP_NAME}",
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        self.welcome_title_label.pack(fill="x")

        # Welcome Description Textbox
        self.welcome_description_textbox = customtkinter.CTkTextbox(
            self.welcome_header_frame,
            font=customtkinter.CTkFont(family=self.font_family, size=12),
            text_color="gray50",    # CTkTextbox does not support dual-mode text_color ("gray50", "gray70").
            fg_color="transparent",
            height=70,
            wrap="word",
            activate_scrollbars=False,  # Disable Scrollbars
            border_width=0
        )
        self.welcome_description_textbox.pack(fill="x", pady=(4, 0))
        self.welcome_description_textbox.insert("1.0", self.app_translator.translate("welcome_message"))
        self.welcome_description_textbox.configure(state="disabled")
        # Disable Text Selection
        self.welcome_description_textbox.bind("<Button-1>", lambda e: "break")  # Disable Single Click
        self.welcome_description_textbox.bind("<B1-Motion>", lambda e: "break")  # Disable Click & Drag
        self.welcome_description_textbox.bind("<Double-Button-1>", lambda e: "break")  # Disable Double Click
        self.welcome_description_textbox.bind("<Triple-Button-1>", lambda e: "break")  # Disable Triple Click
        # --- End of Welcome Section ---

        # --- Microsoft PC Manager Version Info Section ---
        self._create_section_label_with_button(
            self.app_translator.translate("mspcm_version_info"),
            f"↻    {self.app_translator.translate('refresh_button')}",
            self._refresh_mspcm_version_info
        )

        self.mspcm_version_group = self._create_group_frame()
        self._load_mspcm_version_info()
        # --- End of Microsoft PC Manager Version Info Section ---

        # --- Windows Specifications Section ---
        self._create_section_label(self.app_translator.translate("windows_specifications"))
        self.windows_specifications_group = self._create_group_frame()
        self._load_windows_specifications()
        # --- End of Windows Specifications Section ---

    def _refresh_mspcm_version_info(self):
        # Clear existing widgets in the group frame.
        for widget in self.mspcm_version_group.winfo_children():
            widget.destroy()
        
        # Reload version info
        self._load_mspcm_version_info()

    def _load_mspcm_version_info(self):
        # Microsoft PC Manager Version Info
        mspcm_version = GetMSPCMVersion.get_microsoft_pc_manager_version()

        if mspcm_version:
            self.mspcm_version_card = self._create_settings_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_version_is"),
                f"{self.app_translator.translate('mspcm_version_is')}: {mspcm_version}",
                customtkinter.CTkButton,
                text=self.app_translator.translate("start_mspcm_button"),
                width=30,
                command=lambda: StartMSPCM.start_mspcm(logger=self.logger, log_file_path=self.log_file_path,
                                                       app_translator=self.app_translator)
            )
            self.logger.info(f"Loaded Microsoft PC Manager Version: {mspcm_version}")
        else:
            self.mspcm_version_card = self._create_settings_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_version_is"),
                self.app_translator.translate("failed_to_get_mspcm_version_info")
            )
            self.logger.warning("Failed to load Microsoft PC Manager Version.")

        # Microsoft PC Manager Beta Version Info
        mspcm_beta_version = GetMSPCMVersion.get_microsoft_pc_manager_beta_version()

        if mspcm_beta_version:
            self._create_separator(self.mspcm_version_group)

            self.mspcm_beta_version_card = self._create_settings_card(
                self.mspcm_version_group,
                self.app_translator.translate("mspcm_beta_version_is"),
                f"{self.app_translator.translate('mspcm_beta_version_is')}: {mspcm_beta_version}",
                customtkinter.CTkButton,
                text=self.app_translator.translate("start_mspcm_beta_button"),
                width=30,
                command=lambda: StartMSPCMBeta.start_mspcm_beta(logger=self.logger, log_file_path=self.log_file_path,
                                                       app_translator=self.app_translator)
            )
            self.logger.info(f"Loaded Microsoft PC Manager Public Beta Version: {mspcm_beta_version}")

    def _load_windows_specifications(self):
        windows_info = PrerequisiteChecks.get_windows_installation_information()

        if windows_info:
            self._create_settings_card(
                self.windows_specifications_group,
                self.app_translator.translate("windows_installation_info"),
                windows_info,
                customtkinter.CTkButton,
                enable_text_selection=True,
                text=self.app_translator.translate("about_button"),
                width=30,
                command=lambda: OnAboutWindowsButtonClick.open_about_windows(logger=self.logger,
                                                                             log_file_path=self.log_file_path,
                                                                             app_translator=self.app_translator)
            )
        else:
            self._create_settings_card(
                self.windows_specifications_group,
                self.app_translator.translate("windows_installation_info"),
                self.app_translator.translate("failed_to_load_windows_installation_info"),
                customtkinter.CTkButton,
                enable_text_selection=True,
                text=self.app_translator.translate("about_button"),
                width=30,
                command=lambda: OnAboutWindowsButtonClick.open_about_windows(logger=self.logger,
                                                                             log_file_path=self.log_file_path,
                                                                             app_translator=self.app_translator)
            )

    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))

    def _create_section_label_with_button(self, text, button_text, command):
        container = customtkinter.CTkFrame(self.scroll_frame, fg_color="transparent")
        container.pack(fill="x", padx=25, pady=(20, 10))
        
        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(side="left")
        
        button = customtkinter.CTkButton(
            container,
            text=button_text,
            font=customtkinter.CTkFont(family=self.font_family, size=12),
            width=30,
            command=command
        )
        button.pack(side="right")

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

    def _create_settings_card(self, parent, title, description, widget_constructor=None,
                              enable_text_selection=False, **widget_kwargs):
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
            # Auto-adjust height based on newlines (approx 22px per line + padding).
            line_count = description.count('\n') + 1
            textbox_height = max(45, line_count * 22 + 10)

            desc_textbox = customtkinter.CTkTextbox(
                text_frame,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color="gray50",    # CTkTextbox does not support dual-mode text_color ("gray50", "gray70").
                fg_color="transparent",
                wrap="word",
                height=textbox_height,
                activate_scrollbars=False,
                border_width=0
            )
            desc_textbox.pack(fill="x", pady=(0, 5))
            desc_textbox.insert("1.0", description)
            desc_textbox.configure(state="disabled")
            # Disable Text Selection
            if not enable_text_selection:
                desc_textbox.bind("<Button-1>", lambda e: "break")  # Disable Single Click
                desc_textbox.bind("<B1-Motion>", lambda e: "break")  # Disable Click & Drag
                desc_textbox.bind("<Double-Button-1>", lambda e: "break")  # Disable Double Click
                desc_textbox.bind("<Triple-Button-1>", lambda e: "break")  # Disable Triple Click

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
