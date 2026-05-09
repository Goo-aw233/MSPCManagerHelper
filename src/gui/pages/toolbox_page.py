import customtkinter

from core import (
    AppMetadata,
    AppSettings
)
from gui.components import BaseWidgets
from handlers.shared import URLHandler
from .base_page_frame import BaseInfoPageFrame


class ToolboxPage(BaseInfoPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="toolbox_page"
        )

        # === App Update Section ===
        self._create_section_label(self.app_translator.translate("app_update"))

        self.app_update_group = self._create_group_frame()

        # --- From GitHub ---
        self.update_from_github_card = self._create_actions_card(
            self.app_update_group,
            title=self.app_translator.translate("update_from_github_title"),
            description=self.app_translator.translate("update_from_github_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("get_update_button"),
            command=lambda: URLHandler.launch_url(
                url=AppMetadata.APP_GITHUB_REPOSITORY_URL + "/releases",
                target_name="GitHub Release Page",
                messagebox_error_message="failed_to_open_github_releases_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(self.app_update_group)

        # --- From OneDrive ---
        self.update_from_onedrive_card = self._create_actions_card(
            self.app_update_group,
            title=self.app_translator.translate("update_from_onedrive_title"),
            description=self.app_translator.translate("update_from_onedrive_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("get_update_button"),
            command=lambda: URLHandler.launch_url(
                url=(
                    AppMetadata.APP_UPDATE_1DRV_DIR_URL
                    if not AppSettings.is_original_links_enabled()
                    else AppMetadata.APP_UPDATE_1DRV_URL
                ),
                target_name="OneDrive Release Page",
                messagebox_error_message="failed_to_open_1drv_release_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator,
                onedrive_release_url=(
                    AppMetadata.APP_UPDATE_1DRV_DIR_URL
                    if not AppSettings.is_original_links_enabled()
                    else AppMetadata.APP_UPDATE_1DRV_URL
                )
            )
        )
        # === End of App Update Section ===

        # === Download Microsoft PC Manager App Package Section ===
        self._create_section_label(self.app_translator.translate("download_microsoft_pc_manager_app_package"))

        self.download_microsoft_pc_manager_app_package_group = self._create_group_frame()

        # --- From Azure Blob ---
        self.microsoft_pc_manager_azure_blob_card = self._create_actions_card(
            self.download_microsoft_pc_manager_app_package_group,
            title=self.app_translator.translate("download_from_azure_blob_title"),
            description=self.app_translator.translate("download_from_azure_blob_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: URLHandler.launch_url(
                url="https://kaoz.uk/PCManagerOFL",
                target_name="Microsoft PC Manager Application Package Azure Blob Releases Page",
                messagebox_error_message="failed_to_open_mspcm_app_package_azure_blob_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(self.download_microsoft_pc_manager_app_package_group)

        # --- From OneDrive ---
        self.microsoft_pc_manager_onedrive_card = self._create_actions_card(
            self.download_microsoft_pc_manager_app_package_group,
            title=self.app_translator.translate("download_from_onedrive_title"),
            description=self.app_translator.translate("download_from_onedrive_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: URLHandler.launch_url(
                url=(
                    AppMetadata.MSPCM_APP_PACKAGE_1DRV_DIR_URL
                    if not AppSettings.is_original_links_enabled()
                    else AppMetadata.MSPCM_APP_PACKAGE_1DRV_URL
                ),
                target_name="Microsoft PC Manager Application Package OneDrive Releases Page",
                messagebox_error_message="failed_to_open_mspcm_app_package_onedrive_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator,
                mspcm_app_package_onedrive_url=(
                    AppMetadata.MSPCM_APP_PACKAGE_1DRV_DIR_URL
                    if not AppSettings.is_original_links_enabled()
                    else AppMetadata.MSPCM_APP_PACKAGE_1DRV_URL
                )
            )
        )
        # === End of Microsoft PC Manager App Package Download Section ===

        # === Download Runtime Section ===
        self._create_section_label(self.app_translator.translate("download_runtime"))

        self.download_runtime_group = self._create_group_frame()

        # --- Microsoft Edge WebView2 Runtime ---
        self.edge_webview2_runtime_card = self._create_actions_card(
            self.download_runtime_group,
            title=self.app_translator.translate("download_edge_webview2_runtime_title"),
            description=self.app_translator.translate("download_edge_webview2_runtime_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: URLHandler.launch_url(
                url="https://developer.microsoft.com/microsoft-edge/webview2" + AppSettings.get_support_developer_tracking_id(),
                target_name="Microsoft Edge WebView2 Runtime Download Page",
                messagebox_error_message="failed_to_open_webview2_download_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # Separator
        self._create_separator(self.download_runtime_group)

        # --- Windows App Runtime ---
        self.windows_app_runtime_card = self._create_actions_card(
            self.download_runtime_group,
            title=self.app_translator.translate("download_windows_app_runtime_title"),
            description=self.app_translator.translate("download_windows_app_runtime_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("download_button"),
            command=lambda: URLHandler.launch_url(
                url="https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive" + AppSettings.get_support_developer_tracking_id(),
                target_name="Windows App Runtime Download Page",
                messagebox_error_message="failed_to_open_windows_app_runtime_download_page",
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of Download Runtime Section ===
