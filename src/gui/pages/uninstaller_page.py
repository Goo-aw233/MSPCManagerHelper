import tkinter

import customtkinter
from CTkToolTip import CTkToolTip

from core import (
    AdvancedStartup,
    OptionalChecks
)
from gui.components import (
    BaseWidgets,
    ScrollableFrame
)
from modules.uninstaller import (
    UninstallBeta,
    UninstallEdgeComponents,
    UninstallViaDISMForAllUsers,
    UninstallViaPowerShellForAllUsers,
    UninstallViaPowerShellForCurrentUser
)
from .base_page_frame import BaseFuncPageFrame


class UninstallerPage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family, on_mspcm_version_changed=None):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.uninstaller",
            events_textbox_wrap="none",
            on_mspcm_version_changed=on_mspcm_version_changed
        )

        # Build UI Sections
        self._create_uninstall_stable_section()
        self._create_uninstall_beta_section()
        self._create_uninstall_edge_components_section()

        # Operation cards protected by the global operation lock.
        self._operation_cards = [
            (self.uninstall_via_dism_all_users_card, self._refresh_uninstall_via_dism_state),
            (self.uninstall_via_powershell_all_users_card, self._refresh_uninstall_via_powershell_all_state),
            (self.uninstall_via_powershell_current_user_card, self._refresh_uninstall_via_powershell_current_state),
            (self.uninstall_beta_card, self._refresh_uninstall_beta_state),
            (self.uninstall_edge_components_card, self._refresh_uninstall_edge_components_state),
        ]
        self._register_operation_cards()

    def _create_uninstall_stable_section(self):
        # === Uninstall Stable ===
        self._create_section_label(self.app_translator.translate("pages.uninstaller.uninstall_stable"))

        # --- Uninstall via DISM for All Users ---
        uninstall_via_dism_for_all_users_frame = self._create_group_frame()
        uninstall_via_dism_for_all_users_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.uninstall_via_dism_all_users_card = self._create_actions_card(
            parent=uninstall_via_dism_for_all_users_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_dism_all_users"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_dism_all_users_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_dism_all_users
        )

        self._create_separator(uninstall_via_dism_for_all_users_frame)

        # - Uninstall Options -
        self.dism_uninstall_options_frame = ScrollableFrame(
            uninstall_via_dism_for_all_users_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.dism_uninstall_options_frame.pack(fill="x", padx=10, pady=5)

        self.uninstall_image_var = tkinter.StringVar(value="online_image")

        # Online Image
        self.dism_radiobutton_online_image = customtkinter.CTkRadioButton(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.online_image"),
            variable=self.uninstall_image_var,
            value="online_image",
            command=self._refresh_uninstall_via_dism_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.dism_radiobutton_online_image.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Offline Image
        self.dism_radiobutton_offline_image = customtkinter.CTkRadioButton(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.offline_image"),
            variable=self.uninstall_image_var,
            value="offline_image",
            command=self._refresh_uninstall_via_dism_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_radiobutton_offline_image.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.dism_radiobutton_offline_image,
                   self.app_translator.translate("pages.common.offline_image_tooltip"),
                   font=(self.font_family, 12))

        # Basic Cleanup
        self.dism_checkbox_basic_cleanup = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._refresh_uninstall_via_dism_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.dism_checkbox_basic_cleanup.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Advanced Cleanup
        self.dism_checkbox_advanced_cleanup = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_cleanup"),
            command=self._refresh_uninstall_via_dism_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_advanced_cleanup.grid(row=0, column=3, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.dism_checkbox_basic_select_all = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_dism_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.dism_checkbox_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.dism_checkbox_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._refresh_dism_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.dism_checkbox_basic_registries = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._refresh_dism_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.dism_checkbox_basic_cache_files = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._refresh_dism_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Advanced Select All
        self.dism_checkbox_advanced_select_all = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_dism_advanced_select_all,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_advanced_select_all.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Advanced App Package Data
        self.dism_checkbox_advanced_app_package_data = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_app_package_data"),
            command=self._refresh_dism_advanced_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_advanced_app_package_data.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Advanced Registries
        self.dism_checkbox_advanced_registries = customtkinter.CTkCheckBox(
            self.dism_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_registries"),
            command=self._refresh_dism_advanced_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.dism_checkbox_advanced_registries.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.dism_basic_option_checkboxes = [
            self.dism_checkbox_basic_config_cache_dirs,
            self.dism_checkbox_basic_registries,
            self.dism_checkbox_basic_cache_files
        ]
        self.dism_advanced_option_checkboxes = [
            self.dism_checkbox_advanced_app_package_data,
            self.dism_checkbox_advanced_registries
        ]

        self._refresh_uninstall_via_dism_state()

        # --- Uninstall via Windows PowerShell for All Users ---
        uninstall_via_powershell_for_all_users_frame = self._create_group_frame()
        uninstall_via_powershell_for_all_users_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.uninstall_via_powershell_all_users_card = self._create_actions_card(
            parent=uninstall_via_powershell_for_all_users_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_windows_powershell_all_users"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_windows_powershell_all_users_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_powershell_all_users
        )

        self._create_separator(uninstall_via_powershell_for_all_users_frame)

        # - Uninstall Options -
        self.powershell_all_uninstall_options_frame = ScrollableFrame(
            uninstall_via_powershell_for_all_users_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.powershell_all_uninstall_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.powershell_all_checkbox_basic_cleanup = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._refresh_uninstall_via_powershell_all_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.powershell_all_checkbox_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Advanced Cleanup
        self.powershell_all_checkbox_advanced_cleanup = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_cleanup"),
            command=self._refresh_uninstall_via_powershell_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_advanced_cleanup.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.powershell_all_checkbox_basic_select_all = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_all_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.powershell_all_checkbox_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.powershell_all_checkbox_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._refresh_powershell_all_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.powershell_all_checkbox_basic_registries = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._refresh_powershell_all_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.powershell_all_checkbox_basic_cache_files = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._refresh_powershell_all_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Advanced Select All
        self.powershell_all_checkbox_advanced_select_all = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_all_advanced_select_all,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_advanced_select_all.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Advanced App Package Data
        self.powershell_all_checkbox_advanced_app_package_data = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_app_package_data"),
            command=self._refresh_powershell_all_advanced_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_advanced_app_package_data.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Advanced Registries
        self.powershell_all_checkbox_advanced_registries = customtkinter.CTkCheckBox(
            self.powershell_all_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_registries"),
            command=self._refresh_powershell_all_advanced_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_all_checkbox_advanced_registries.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.powershell_all_basic_option_checkboxes = [
            self.powershell_all_checkbox_basic_config_cache_dirs,
            self.powershell_all_checkbox_basic_registries,
            self.powershell_all_checkbox_basic_cache_files
        ]
        self.powershell_all_advanced_option_checkboxes = [
            self.powershell_all_checkbox_advanced_app_package_data,
            self.powershell_all_checkbox_advanced_registries
        ]

        self._refresh_uninstall_via_powershell_all_state()

        # --- Uninstall via Windows PowerShell for Current User ---
        uninstall_via_powershell_for_current_user_frame = self._create_group_frame()
        self.uninstall_via_powershell_current_user_card = self._create_actions_card(
            parent=uninstall_via_powershell_for_current_user_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_windows_powershell_current_user"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_windows_powershell_current_user_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_powershell_current_user
        )

        self._create_separator(uninstall_via_powershell_for_current_user_frame)

        # - Uninstall Options -
        self.powershell_current_uninstall_options_frame = ScrollableFrame(
            uninstall_via_powershell_for_current_user_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.powershell_current_uninstall_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.powershell_current_checkbox_basic_cleanup = customtkinter.CTkCheckBox(
            self.powershell_current_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._refresh_uninstall_via_powershell_current_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.powershell_current_checkbox_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.powershell_current_checkbox_basic_select_all = customtkinter.CTkCheckBox(
            self.powershell_current_uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_current_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.powershell_current_checkbox_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.powershell_current_checkbox_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.powershell_current_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._refresh_powershell_current_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_current_checkbox_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.powershell_current_checkbox_basic_registries = customtkinter.CTkCheckBox(
            self.powershell_current_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._refresh_powershell_current_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_current_checkbox_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.powershell_current_checkbox_basic_cache_files = customtkinter.CTkCheckBox(
            self.powershell_current_uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._refresh_powershell_current_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.powershell_current_checkbox_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        self.powershell_current_basic_option_checkboxes = [
            self.powershell_current_checkbox_basic_config_cache_dirs,
            self.powershell_current_checkbox_basic_registries,
            self.powershell_current_checkbox_basic_cache_files
        ]

        self._refresh_uninstall_via_powershell_current_state()
        # === End of Uninstall Stable ===

    def _create_uninstall_beta_section(self):
        # === Uninstall Beta ===
        self._create_section_label(self.app_translator.translate("pages.uninstaller.uninstall_beta"))

        # --- Uninstall Beta ---
        uninstall_beta_frame = self._create_group_frame()
        self.uninstall_beta_card = self._create_actions_card(
            parent=uninstall_beta_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_beta"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_beta_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_beta
        )

        self._create_separator(uninstall_beta_frame)

        # - Uninstall Options -
        self.uninstall_beta_options_frame = ScrollableFrame(
            uninstall_beta_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.uninstall_beta_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.uninstall_beta_checkbox_basic_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._refresh_uninstall_beta_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.uninstall_beta_checkbox_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.uninstall_beta_checkbox_basic_select_all = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_uninstall_beta_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.uninstall_beta_checkbox_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.uninstall_beta_checkbox_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._refresh_uninstall_beta_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_beta_checkbox_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.uninstall_beta_checkbox_basic_registries = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._refresh_uninstall_beta_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_beta_checkbox_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.uninstall_beta_checkbox_basic_cache_files = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._refresh_uninstall_beta_basic_select_all_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_beta_checkbox_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.uninstall_beta_basic_option_checkboxes = [
            self.uninstall_beta_checkbox_basic_config_cache_dirs,
            self.uninstall_beta_checkbox_basic_registries,
            self.uninstall_beta_checkbox_basic_cache_files
        ]

        self._refresh_uninstall_beta_state()
        # === End of Uninstall Beta ===

    def _create_uninstall_edge_components_section(self):
        # === Uninstall Edge Components ===
        self._create_section_label(self.app_translator.translate("pages.uninstaller.uninstall_edge_components"))

        uninstall_edge_components_frame = self._create_group_frame()
        self.uninstall_edge_components_card = self._create_actions_card(
            parent=uninstall_edge_components_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_edge_components"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_edge_components_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_edge_components
        )

        self._create_separator(uninstall_edge_components_frame)

        # - Uninstall Options -
        self.uninstall_edge_components_options_frame = ScrollableFrame(
            uninstall_edge_components_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.uninstall_edge_components_options_frame.pack(fill="x", padx=10, pady=5)

        # Force Uninstall
        self.uninstall_force_uninstall_checkbox = customtkinter.CTkCheckBox(
            self.uninstall_edge_components_options_frame,
            text=self.app_translator.translate("pages.uninstaller.uninstall_force_uninstall"),
            command=self._refresh_uninstall_edge_components_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.uninstall_force_uninstall_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Microsoft Edge
        self.uninstall_edge_checkbox = customtkinter.CTkCheckBox(
            self.uninstall_edge_components_options_frame,
            text=self.app_translator.translate("pages.uninstaller.uninstall_edge"),
            command=self._refresh_uninstall_edge_components_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_edge_checkbox.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Microsoft Edge WebView2 Runtime
        self.uninstall_webview2_checkbox = customtkinter.CTkCheckBox(
            self.uninstall_edge_components_options_frame,
            text=self.app_translator.translate("pages.uninstaller.uninstall_webview2"),
            command=self._refresh_uninstall_edge_components_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_webview2_checkbox.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Microsoft EdgeUpdate
        self.uninstall_edgeupdate_checkbox = customtkinter.CTkCheckBox(
            self.uninstall_edge_components_options_frame,
            text=self.app_translator.translate("pages.uninstaller.uninstall_edgeupdate"),
            command=self._refresh_uninstall_edge_components_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uninstall_edgeupdate_checkbox.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Apply initial state (availability is detected on every refresh).
        self._refresh_uninstall_edge_components_state()
        # === End of Uninstall Edge Components ===


    # ~~~ Features Functions ~~~
    # ~ Uninstall via DISM for All Users ~
    def _refresh_uninstall_via_dism_card_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["Dism.exe", "powershell.exe"],
                                                                   suppress_complete_log=True):
            state = "disabled"
            self.logger.warning(
                "Dism.exe or powershell.exe is not available. Disabling 'Uninstall via DISM (All Users)' option.")
        self._set_card_state(self.uninstall_via_dism_all_users_card, state)

    def _refresh_dism_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.dism_basic_option_checkboxes):
            self.dism_checkbox_basic_select_all.select()
        else:
            self.dism_checkbox_basic_select_all.deselect()

    def _refresh_dism_advanced_select_all_state(self):
        if all(cb.get() == 1 for cb in self.dism_advanced_option_checkboxes):
            self.dism_checkbox_advanced_select_all.select()
        else:
            self.dism_checkbox_advanced_select_all.deselect()

    def _set_dism_basic_row_enabled(self, enabled):
        if enabled:
            self.dism_checkbox_basic_select_all.configure(state="normal")
            for cb in self.dism_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.dism_checkbox_basic_select_all.deselect()
            self.dism_checkbox_basic_select_all.configure(state="disabled")
            for cb in self.dism_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _set_dism_advanced_row_enabled(self, enabled):
        if enabled:
            self.dism_checkbox_advanced_select_all.configure(state="normal")
            for cb in self.dism_advanced_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.dism_checkbox_advanced_select_all.deselect()
            self.dism_checkbox_advanced_select_all.configure(state="disabled")
            for cb in self.dism_advanced_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _refresh_uninstall_via_dism_options_state(self):
        is_offline = self.uninstall_image_var.get() == "offline_image"

        # Cleanup options are not applicable to offline images.
        if is_offline:
            self.dism_checkbox_basic_cleanup.deselect()
            self.dism_checkbox_advanced_cleanup.deselect()
        self.dism_checkbox_basic_cleanup.configure(
            state="disabled" if is_offline else "normal")
        self.dism_checkbox_advanced_cleanup.configure(
            state="disabled" if is_offline else "normal")

        self._set_dism_basic_row_enabled(
            not is_offline and self.dism_checkbox_basic_cleanup.get() == 1)
        self._set_dism_advanced_row_enabled(
            not is_offline and self.dism_checkbox_advanced_cleanup.get() == 1)

        self._refresh_dism_basic_select_all_state()
        self._refresh_dism_advanced_select_all_state()

    def _refresh_uninstall_via_dism_state(self):
        self._refresh_uninstall_via_dism_options_state()
        self._refresh_uninstall_via_dism_card_state()

    def _toggle_dism_basic_select_all(self):
        state = self.dism_checkbox_basic_select_all.get()
        for cb in self.dism_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_dism_basic_select_all_state()

    def _toggle_dism_advanced_select_all(self):
        state = self.dism_checkbox_advanced_select_all.get()
        for cb in self.dism_advanced_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_dism_advanced_select_all_state()

    def _run_uninstall_via_dism_all_users(self):
        self.uninstall_via_dism_all_users_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.dism_checkbox_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.dism_checkbox_basic_registries.get() == 1,
            "basic_cache_files": self.dism_checkbox_basic_cache_files.get() == 1,
            "advanced_app_package_data": self.dism_checkbox_advanced_app_package_data.get() == 1,
            "advanced_registries": self.dism_checkbox_advanced_registries.get() == 1
        }

        worker = UninstallViaDISMForAllUsers(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            image_type=self.uninstall_image_var.get(),
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            worker.execute,
            "pages.uninstaller.uninstall_via_dism_all_users",
            on_completion=lambda: self._refresh_uninstall_via_dism_state()
        )
    # ~ End of Uninstall via DISM for All Users ~

    # ~ Uninstall via Windows PowerShell for All Users ~
    def _refresh_uninstall_via_powershell_all_card_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"],
                                                                   suppress_complete_log=True):
            state = "disabled"
            self.logger.warning(
                "powershell.exe is not available. Disabling 'Uninstall via Windows PowerShell (All Users)' option.")
        self._set_card_state(self.uninstall_via_powershell_all_users_card, state)

    def _refresh_powershell_all_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_all_basic_option_checkboxes):
            self.powershell_all_checkbox_basic_select_all.select()
        else:
            self.powershell_all_checkbox_basic_select_all.deselect()

    def _refresh_powershell_all_advanced_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_all_advanced_option_checkboxes):
            self.powershell_all_checkbox_advanced_select_all.select()
        else:
            self.powershell_all_checkbox_advanced_select_all.deselect()

    def _set_powershell_all_basic_row_enabled(self, enabled):
        if enabled:
            self.powershell_all_checkbox_basic_select_all.configure(state="normal")
            for cb in self.powershell_all_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.powershell_all_checkbox_basic_select_all.deselect()
            self.powershell_all_checkbox_basic_select_all.configure(state="disabled")
            for cb in self.powershell_all_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _set_powershell_all_advanced_row_enabled(self, enabled):
        if enabled:
            self.powershell_all_checkbox_advanced_select_all.configure(state="normal")
            for cb in self.powershell_all_advanced_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.powershell_all_checkbox_advanced_select_all.deselect()
            self.powershell_all_checkbox_advanced_select_all.configure(state="disabled")
            for cb in self.powershell_all_advanced_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _refresh_uninstall_via_powershell_all_options_state(self):
        self.powershell_all_checkbox_basic_cleanup.configure(state="normal")
        self.powershell_all_checkbox_advanced_cleanup.configure(state="normal")

        self._set_powershell_all_basic_row_enabled(self.powershell_all_checkbox_basic_cleanup.get() == 1)
        self._set_powershell_all_advanced_row_enabled(self.powershell_all_checkbox_advanced_cleanup.get() == 1)

        self._refresh_powershell_all_basic_select_all_state()
        self._refresh_powershell_all_advanced_select_all_state()

    def _refresh_uninstall_via_powershell_all_state(self):
        self._refresh_uninstall_via_powershell_all_options_state()
        self._refresh_uninstall_via_powershell_all_card_state()

    def _toggle_powershell_all_basic_select_all(self):
        state = self.powershell_all_checkbox_basic_select_all.get()
        for cb in self.powershell_all_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_powershell_all_basic_select_all_state()

    def _toggle_powershell_all_advanced_select_all(self):
        state = self.powershell_all_checkbox_advanced_select_all.get()
        for cb in self.powershell_all_advanced_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_powershell_all_advanced_select_all_state()

    def _run_uninstall_via_powershell_all_users(self):
        self.uninstall_via_powershell_all_users_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.powershell_all_checkbox_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.powershell_all_checkbox_basic_registries.get() == 1,
            "basic_cache_files": self.powershell_all_checkbox_basic_cache_files.get() == 1,
            "advanced_app_package_data": self.powershell_all_checkbox_advanced_app_package_data.get() == 1,
            "advanced_registries": self.powershell_all_checkbox_advanced_registries.get() == 1
        }

        worker = UninstallViaPowerShellForAllUsers(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            worker.execute,
            "pages.uninstaller.uninstall_via_windows_powershell_all_users",
            on_completion=lambda: self._refresh_uninstall_via_powershell_all_state()
        )
    # ~ End of Uninstall via Windows PowerShell for All Users ~

    # ~ Uninstall via Windows PowerShell for Current User ~
    def _refresh_uninstall_via_powershell_current_card_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"],
                                                                   suppress_complete_log=True):
            state = "disabled"
            self.logger.warning(
                "powershell.exe is not available. Disabling 'Uninstall via Windows PowerShell (Current User)' option.")
        self._set_card_state(self.uninstall_via_powershell_current_user_card, state)

    def _refresh_powershell_current_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_current_basic_option_checkboxes):
            self.powershell_current_checkbox_basic_select_all.select()
        else:
            self.powershell_current_checkbox_basic_select_all.deselect()

    def _set_powershell_current_basic_row_enabled(self, enabled):
        if enabled:
            self.powershell_current_checkbox_basic_select_all.configure(state="normal")
            for cb in self.powershell_current_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.powershell_current_checkbox_basic_select_all.deselect()
            self.powershell_current_checkbox_basic_select_all.configure(state="disabled")
            for cb in self.powershell_current_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _refresh_uninstall_via_powershell_current_options_state(self):
        self.powershell_current_checkbox_basic_cleanup.configure(state="normal")
        self._set_powershell_current_basic_row_enabled(self.powershell_current_checkbox_basic_cleanup.get() == 1)
        self._refresh_powershell_current_basic_select_all_state()

    def _refresh_uninstall_via_powershell_current_state(self):
        self._refresh_uninstall_via_powershell_current_options_state()
        self._refresh_uninstall_via_powershell_current_card_state()

    def _toggle_powershell_current_basic_select_all(self):
        state = self.powershell_current_checkbox_basic_select_all.get()
        for cb in self.powershell_current_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_powershell_current_basic_select_all_state()

    def _run_uninstall_via_powershell_current_user(self):
        self.uninstall_via_powershell_current_user_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.powershell_current_checkbox_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.powershell_current_checkbox_basic_registries.get() == 1,
            "basic_cache_files": self.powershell_current_checkbox_basic_cache_files.get() == 1
        }

        worker = UninstallViaPowerShellForCurrentUser(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            worker.execute,
            "pages.uninstaller.uninstall_via_windows_powershell_current_user",
            on_completion=lambda: self._refresh_uninstall_via_powershell_current_state()
        )
    # ~ End of Uninstall via Windows PowerShell for Current User ~

    # ~ Uninstall Beta ~
    def _refresh_uninstall_beta_card_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        self._set_card_state(self.uninstall_beta_card, state)

    def _refresh_uninstall_beta_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.uninstall_beta_basic_option_checkboxes):
            self.uninstall_beta_checkbox_basic_select_all.select()
        else:
            self.uninstall_beta_checkbox_basic_select_all.deselect()

    def _set_uninstall_beta_basic_row_enabled(self, enabled):
        if enabled:
            self.uninstall_beta_checkbox_basic_select_all.configure(state="normal")
            for cb in self.uninstall_beta_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.uninstall_beta_checkbox_basic_select_all.deselect()
            self.uninstall_beta_checkbox_basic_select_all.configure(state="disabled")
            for cb in self.uninstall_beta_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _refresh_uninstall_beta_options_state(self):
        self.uninstall_beta_checkbox_basic_cleanup.configure(state="normal")
        self._set_uninstall_beta_basic_row_enabled(self.uninstall_beta_checkbox_basic_cleanup.get() == 1)
        self._refresh_uninstall_beta_basic_select_all_state()

    def _refresh_uninstall_beta_state(self):
        self._refresh_uninstall_beta_options_state()
        self._refresh_uninstall_beta_card_state()

    def _toggle_uninstall_beta_basic_select_all(self):
        state = self.uninstall_beta_checkbox_basic_select_all.get()
        for cb in self.uninstall_beta_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._refresh_uninstall_beta_basic_select_all_state()

    def _run_uninstall_beta(self):
        self.uninstall_beta_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.uninstall_beta_checkbox_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.uninstall_beta_checkbox_basic_registries.get() == 1,
            "basic_cache_files": self.uninstall_beta_checkbox_basic_cache_files.get() == 1
        }

        worker = UninstallBeta(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            worker.execute,
            "pages.uninstaller.uninstall_beta",
            on_completion=lambda: self._refresh_uninstall_beta_state()
        )
    # ~ End of Uninstall Beta ~

    # ~ Uninstall Edge Components ~
    @staticmethod
    def _set_uninstall_edge_option_state(checkbox, available):
        if available:
            checkbox.configure(state="normal")
        else:
            checkbox.deselect()
            checkbox.configure(state="disabled")

    def _refresh_uninstall_edge_components_options_state(self):
        self._set_uninstall_edge_option_state(
            self.uninstall_edge_checkbox, UninstallEdgeComponents.is_edge_available())
        self._set_uninstall_edge_option_state(
            self.uninstall_webview2_checkbox, UninstallEdgeComponents.is_webview2_available())
        self._set_uninstall_edge_option_state(
            self.uninstall_edgeupdate_checkbox, UninstallEdgeComponents.is_edgeupdate_available())

        can_force = (self.uninstall_edge_checkbox.get() == 1) or (self.uninstall_webview2_checkbox.get() == 1)
        self._set_uninstall_edge_option_state(self.uninstall_force_uninstall_checkbox, can_force)

    def _refresh_uninstall_edge_components_card_state(self):
        state = "disabled"
        if (AdvancedStartup.is_administrator()
                and any(cb.get() == 1 for cb in (
                    self.uninstall_edge_checkbox,
                    self.uninstall_webview2_checkbox,
                    self.uninstall_edgeupdate_checkbox))):
            state = "normal"
        self._set_card_state(self.uninstall_edge_components_card, state)

    def _refresh_uninstall_edge_components_state(self):
        self._refresh_uninstall_edge_components_options_state()
        self._refresh_uninstall_edge_components_card_state()

    def _run_uninstall_edge_components(self):
        self.uninstall_edge_components_card.configure(state="disabled")
        self.update_idletasks()

        worker = UninstallEdgeComponents(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            force_uninstall=self.uninstall_force_uninstall_checkbox.get() == 1,
            uninstall_edge=self.uninstall_edge_checkbox.get() == 1,
            uninstall_webview2=self.uninstall_webview2_checkbox.get() == 1,
            uninstall_edgeupdate=self.uninstall_edgeupdate_checkbox.get() == 1
        )

        self._run_operation(
            worker.execute,
            "pages.uninstaller.uninstall_edge_components",
            on_completion=lambda: self._refresh_uninstall_edge_components_state()
        )
    # ~ End of Uninstall Edge Components ~

    # ~ Operation Completion Hook ~
    def _on_operation_completed(self):
        # Refresh the state of Microsoft PC Manager version display on the Home page.
        if self.on_mspcm_version_changed:
            self.on_mspcm_version_changed()
    # ~ End of Operation Completion Hook ~
