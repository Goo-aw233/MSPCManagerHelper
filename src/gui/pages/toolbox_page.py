import customtkinter

from core.app_logger import AppLogger
from gui.pages.events import *


class ToolboxPage(customtkinter.CTkFrame):
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
            text=self.app_translator.translate("toolbox_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # === App Update Section ===
        self._create_section_label(self.app_translator.translate("app_update"))

        self.app_update_group = self._create_group_frame()

        # --- From GitHub ---
        self.update_from_github_card = self._create_settings_card(
            self.app_update_group,
            title=self.app_translator.translate("update_from_github_title"),
            description=self.app_translator.translate("update_from_github_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("get_update_button"),
            command=lambda: OnOpenURLButtonClick.open_github_releases_page(logger=self.logger,
                                                                           log_file_path=self.log_file_path,
                                                                           app_translator=self.app_translator)
        )

        # --- Separator ---
        self._create_separator(self.app_update_group)

        # --- From OneDrive ---
        self.update_from_onedrive_card = self._create_settings_card(
            self.app_update_group,
            title=self.app_translator.translate("update_from_onedrive_title"),
            description=self.app_translator.translate("update_from_onedrive_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("get_update_button"),
            command=lambda: OnOpenURLButtonClick.open_1drv_page(logger=self.logger, log_file_path=self.log_file_path,
                                                                app_translator=self.app_translator)
        )
        # === End of App Update Section ===

        # === Download Microsoft PC Manager App Package Section ===
        self._create_section_label(self.app_translator.translate("download_microsoft_pc_manager_app_package"))

        self.download_microsoft_pc_manager_app_package_group = self._create_group_frame()

        # --- From Azure Blob ---
        self.microsoft_pc_manager_azure_blob_card = self._create_settings_card(
            self.download_microsoft_pc_manager_app_package_group,
            title=self.app_translator.translate("download_from_azure_blob_title"),
            description=self.app_translator.translate("download_from_azure_blob_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: OnOpenURLButtonClick.open_mspcm_app_package_azure_blob_page(logger=self.logger,
                                                                                        log_file_path=self.log_file_path,
                                                                                        app_translator=self.app_translator)
        )

        # --- Separator ---
        self._create_separator(self.download_microsoft_pc_manager_app_package_group)

        # --- From OneDrive ---
        self.microsoft_pc_manager_onedrive_card = self._create_settings_card(
            self.download_microsoft_pc_manager_app_package_group,
            title=self.app_translator.translate("download_from_onedrive_title"),
            description=self.app_translator.translate("download_from_onedrive_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: OnOpenURLButtonClick.open_mspcm_app_package_1drv_page(logger=self.logger,
                                                                                  log_file_path=self.log_file_path,
                                                                                  app_translator=self.app_translator)
        )
        # === End of Microsoft PC Manager App Package Download Section ===

        # === Download Runtime Section ===
        self._create_section_label(self.app_translator.translate("download_runtime"))

        self.download_runtime_group = self._create_group_frame()

        # --- Microsoft Edge WebView 2 Runtime ---
        self.edge_webview2_runtime_card = self._create_settings_card(
            self.download_runtime_group,
            title=self.app_translator.translate("download_edge_webview2_runtime_title"),
            description=self.app_translator.translate("download_edge_webview2_runtime_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: OnOpenURLButtonClick.open_wv2_rt_download_page(logger=self.logger,
                                                                           log_file_path=self.log_file_path,
                                                                           app_translator=self.app_translator)
        )

        # Separator
        self._create_separator(self.download_runtime_group)

        # --- Windows App Runtime ---
        self.windows_app_runtime_card = self._create_settings_card(
            self.download_runtime_group,
            title=self.app_translator.translate("download_windows_app_runtime_title"),
            description=self.app_translator.translate("download_windows_app_runtime_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: OnOpenURLButtonClick.open_war_rt_download_page(logger=self.logger,
                                                                          log_file_path=self.log_file_path,
                                                                          app_translator=self.app_translator)
        )
        # === End of Download Runtime Section ===


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
