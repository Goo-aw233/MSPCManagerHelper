import threading
import time
import tkinter

import customtkinter
from CTkToolTip import CTkToolTip

from core import (
    AdvancedStartup,
    AppSettings,
    GetMSPCMVersion,
    OptionalChecks,
    PrerequisiteChecks
)
from gui.components import (
    BaseWidgets,
)
from .base_page_frame import BaseFuncPageFrame
from modules.utilities import (
    ComputeFilesHashes,
    GetDependenciesVersion,
    OpenDeveloperSettings,
    OpenMSPCMDoc,
    RepairEdgeWebView2Installation,
    RestartServices,
    SwitchRegions,
    ViewInstalledSecurityProducts
)


class UtilitiesPage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.utilities",
            events_textbox_wrap="none"
        )

        # === File Management ===
        self._create_section_label(self.app_translator.translate("pages.utilities.file_management"))

        file_management_frame = self._create_group_frame()

        # --- Compute Files Hashes ---
        self.compute_files_hashes_card = self._create_actions_card(
            file_management_frame,
            title=self.app_translator.translate("pages.utilities.compute_files_hashes"),
            description=self.app_translator.translate("pages.utilities.compute_files_hashes_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_compute_hashes
        )
        self.compute_files_hashes_card.configure(state="disabled")

        self._create_separator(file_management_frame)

        # - Hash Algorithm Checkboxes -
        self.hash_checkboxes_frame = customtkinter.CTkScrollableFrame(
            file_management_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.hash_checkboxes_frame.pack(fill="x", padx=10, pady=5)

        self.select_all_checkbox = customtkinter.CTkCheckBox(
            self.hash_checkboxes_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.select_all_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.uppercase_all_results = customtkinter.CTkCheckBox(
            self.hash_checkboxes_frame,
            text=self.app_translator.translate("pages.utilities.uppercase_all_results"),
            command=None,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.uppercase_all_results.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.hash_algos = {
            "md5": "MD5",
            "sha1": "SHA1",
            "sha224": "SHA224",
            "sha256": "SHA256",
            "sha384": "SHA384",
            "sha512": "SHA512",
            "sha3_224": "SHA3_224",
            "sha3_256": "SHA3_256",
            "sha3_384": "SHA3_384",
            "sha3_512": "SHA3_512",
            "shake_128": "Shake128",
            "shake_256": "Shake256",
            "blake2b": "Blake2b",
            "blake2s": "Blake2s"
        }
        self.hash_algo_tooltips = {
            "shake_128": "pages.utilities.shake_128_tooltip",
            "shake_256": "pages.utilities.shake_256_tooltip",
            "blake2b": "pages.utilities.blake2b_tooltip",
            "blake2s": "pages.utilities.blake2s_tooltip"
        }
        self.hash_checkbox_widgets = {}

        total_algos = len(self.hash_algos)
        row1_count = (total_algos + 1) // 2

        for i, (algo_key, algo_name) in enumerate(self.hash_algos.items()):
            cb = customtkinter.CTkCheckBox(
                self.hash_checkboxes_frame,
                text=algo_name,
                command=self._on_hash_checkbox_change,
                font=customtkinter.CTkFont(family=self.font_family)
            )

            if i < row1_count:
                r = 1
                c = i
            else:
                r = 2
                c = i - row1_count

            cb.grid(row=r, column=c, sticky="w", padx=10, pady=5)
            self.hash_checkbox_widgets[algo_key] = cb

            if algo_key in self.hash_algo_tooltips:
                CTkToolTip(cb, message=self.app_translator.translate(self.hash_algo_tooltips[algo_key]),
                           font=(self.font_family, 12))
        # === End of File Management ===

        # === Open To ===
        self._create_section_label(self.app_translator.translate("pages.utilities.open_to"))

        open_to_frame = self._create_group_frame()

        # --- Open Developer Settings ---
        self.open_developer_settings_card = self._create_actions_card(
            open_to_frame,
            title=self.app_translator.translate("pages.utilities.open_developer_settings"),
            description=self.app_translator.translate("pages.utilities.open_developer_settings_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=lambda: OpenDeveloperSettings.open_developer_settings(
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(open_to_frame)

        # --- Open Microsoft PC Manager Documentation ---
        self.open_mspcm_doc_card = self._create_actions_card(
            open_to_frame,
            title=self.app_translator.translate("pages.utilities.open_mspcm_doc"),
            description=self.app_translator.translate("pages.utilities.open_mspcm_doc_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=lambda: OpenMSPCMDoc.open_mspcm_doc(
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of Open To ===

        # === Maintenance Management ===
        self._create_section_label(self.app_translator.translate("pages.utilities.maintenance_management"))

        # --- Get Dependencies Versions ---
        get_dependencies_versions_frame = self._create_group_frame()
        get_dependencies_versions_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.get_dependencies_versions_card = self._create_actions_card(
            get_dependencies_versions_frame,
            title=self.app_translator.translate("pages.utilities.get_dependencies_versions"),
            description=self.app_translator.translate("pages.utilities.get_dependencies_versions_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_get_dependencies_versions
        )

        self._create_separator(get_dependencies_versions_frame)

        # - Dependencies Types Checkboxes -
        self.dependencies_types_frame = customtkinter.CTkScrollableFrame(
            get_dependencies_versions_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.dependencies_types_frame.pack(fill="x", padx=10, pady=5)

        # System WebView2
        self.checkbox_system_webview2 = customtkinter.CTkCheckBox(
            self.dependencies_types_frame,
            text=self.app_translator.translate("pages.utilities.system_webview2"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_dependencies_checkbox_change
        )
        self.checkbox_system_webview2.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_system_webview2, message=fr"%SystemRoot%\System32\Microsoft-Edge-WebView",
                   font=(self.font_family, 12))

        # Global WebView2
        self.checkbox_global_webview2 = customtkinter.CTkCheckBox(
            self.dependencies_types_frame,
            text=self.app_translator.translate("pages.utilities.global_webview2"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_dependencies_checkbox_change
        )
        self.checkbox_global_webview2.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_global_webview2, message=fr"%ProgramFiles(x86)%\Microsoft\EdgeWebView",
                   font=(self.font_family, 12))

        # Windows App Runtime
        self.checkbox_windows_app_runtime = customtkinter.CTkCheckBox(
            self.dependencies_types_frame,
            text=self.app_translator.translate("pages.utilities.windows_app_runtime"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_dependencies_checkbox_change
        )
        self.checkbox_windows_app_runtime.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Checkbox Configuration
        if not OptionalChecks.check_windows_utilities_availability(target_utility="powershell.exe"):
            self.checkbox_windows_app_runtime.configure(state="disabled")
            self.logger.warning("Windows PowerShell is not available. Disabling Windows App Runtime Dependency Check Checkbox.")

        self.get_dependencies_versions_card.configure(state="disabled")

        # --- Repair Microsoft Edge WebView2 Installation ---
        repair_edge_webview_2_installation_frame = self._create_group_frame()
        repair_edge_webview_2_installation_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.repair_edge_webview_2_installation_card = self._create_actions_card(
            repair_edge_webview_2_installation_frame,
            title=self.app_translator.translate("pages.utilities.repair_edge_webview_2_installation"),
            description=self.app_translator.translate("pages.utilities.repair_edge_webview_2_installation_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_repair_edge_webview2_installation
        )

        self._create_separator(repair_edge_webview_2_installation_frame)

        # - Microsoft Edge WebView2 Repair Options -
        self.webview2_repair_options_frame = customtkinter.CTkScrollableFrame(
            repair_edge_webview_2_installation_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.webview2_repair_options_frame.pack(fill="x", padx=10, pady=5)

        # Select All
        self.checkbox_webview2_select_all = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_select_all_change
        )
        self.checkbox_webview2_select_all.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # End Related Processes
        self.checkbox_end_related_processes = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.utilities.end_related_processes"),
            font=customtkinter.CTkFont(family=self.font_family, weight="bold"),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_end_related_processes.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_end_related_processes,
                   message=self.app_translator.translate("pages.utilities.end_related_processes_tooltip"), font=(self.font_family, 12))
        self.checkbox_end_related_processes.configure(state="disabled")

        # Restore IFEO Registry
        self.checkbox_restore_ifeo_registry = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.utilities.restore_ifeo_registry"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_restore_ifeo_registry.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_restore_ifeo_registry,
                   message=self.app_translator.translate("pages.utilities.restore_ifeo_registry_tooltip"), font=(self.font_family, 12))

        # Remove EdgeUpdate Registry
        self.checkbox_remove_edgeupdate_registry = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.utilities.remove_edgeupdate_registry"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_remove_edgeupdate_registry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_remove_edgeupdate_registry,
                   message=r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate",
                   font=(self.font_family, 12))

        # Remove WebView2 Directory
        self.checkbox_remove_webview2_dir = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.utilities.remove_webview2_dir"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_remove_webview2_dir.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_remove_webview2_dir, message=fr"%ProgramFiles(x86)%\Microsoft\EdgeWebView",
                   font=(self.font_family, 12))

        # Remove Edge Components Directory
        self.checkbox_remove_edge_components_dir = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("pages.utilities.remove_edge_components_dir"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_remove_edge_components_dir.grid(row=1, column=3, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_remove_edge_components_dir, message=fr"%ProgramFiles(x86)%\Microsoft",
                   font=(self.font_family, 12))

        # Checkbox Configuration
        if not AdvancedStartup.is_administrator():
            self.checkbox_webview2_select_all.configure(state="disabled")
            self.checkbox_restore_ifeo_registry.configure(state="disabled")
            self.checkbox_remove_edgeupdate_registry.configure(state="disabled")
            self.checkbox_remove_webview2_dir.configure(state="disabled")
            self.checkbox_remove_edge_components_dir.configure(state="disabled")
            self.checkbox_end_related_processes.configure(state="disabled")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility="reg.exe"):
            self.checkbox_restore_ifeo_registry.configure(state="disabled")
            self.checkbox_remove_edgeupdate_registry.configure(state="disabled")
            self.logger.warning("reg.exe is not available. Disabling registry repair checkboxes.")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility=["cmd.exe", "powershell.exe"]):
            self.checkbox_remove_webview2_dir.configure(state="disabled")
            self.logger.warning("cmd.exe or powershell.exe is not available. Disabling WebView2 Directory Removal Checkbox.")
            self.checkbox_remove_edge_components_dir.configure(state="disabled")
            self.logger.warning("cmd.exe or powershell.exe is not available. Disabling Edge Components Directory Removal Checkbox.")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility=["taskkill.exe"]):
            self.checkbox_end_related_processes.configure(state="disabled")
            self.logger.warning("taskkill.exe is not available. Disabling End Related Processes Checkbox.")

        self.repair_edge_webview_2_installation_card.configure(state="disabled")

        # --- Restart Services ---
        restart_services_frame = self._create_group_frame()
        restart_services_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.restart_services_card = self._create_actions_card(
            restart_services_frame,
            title=self.app_translator.translate("pages.utilities.restart_services"),
            description=self.app_translator.translate("pages.utilities.restart_services_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_restart_services
        )

        self._create_separator(restart_services_frame)

        # - Microsoft PC Manager Services Checkboxes -
        self.mspcm_services_checkboxes_frame = customtkinter.CTkScrollableFrame(
            restart_services_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.mspcm_services_checkboxes_frame.pack(fill="x", padx=10, pady=5)

        # PCManager Service Store
        self.checkbox_stable_version = customtkinter.CTkCheckBox(
            self.mspcm_services_checkboxes_frame,
            text=self.app_translator.translate("pages.utilities.stable_version"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_stable_version.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_stable_version, message="Microsoft.MicrosoftPCManager_8wekyb3d8bbwe",
                   font=(self.font_family, 12))

        # PCManager Service
        self.checkbox_beta_version = customtkinter.CTkCheckBox(
            self.mspcm_services_checkboxes_frame,
            text=self.app_translator.translate("pages.utilities.beta_version"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_beta_version.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_beta_version, message=self.app_translator.translate("pages.utilities.beta_version_tooltip"),
                   font=(self.font_family, 12))

        # PC Manager Service
        self.checkbox_store_beta_version = customtkinter.CTkCheckBox(
            self.mspcm_services_checkboxes_frame,
            text=self.app_translator.translate("pages.utilities.store_beta_version"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_store_beta_version.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_store_beta_version, message="Microsoft.PCManager_8wekyb3d8bbwe",
                   font=(self.font_family, 12))

        # Checkbox Configuration (Async to Avoid Blocking UI Refresh)
        self.checkbox_stable_version.configure(state="disabled")
        self.checkbox_store_beta_version.configure(state="disabled")
        self.checkbox_beta_version.configure(state="disabled")
        self._load_mspcm_versions_async()
        
        self.restart_services_card.configure(state="disabled")

        # --- Switch Regions ---
        switch_regions_frame = self._create_group_frame()
        switch_regions_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.switch_regions_card = self._create_actions_card(
            switch_regions_frame,
            title=self.app_translator.translate("pages.utilities.switch_regions"),
            description=self.app_translator.translate("pages.utilities.switch_regions_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_switch_regions
        )

        self._create_separator(switch_regions_frame)

        # - Microsoft PC Manager Version Radio Button -
        self.mspcm_version_radiobutton_frame = customtkinter.CTkScrollableFrame(switch_regions_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.mspcm_version_radiobutton_frame.pack(fill="x", padx=10, pady=5)

        self.mspcm_version_var = tkinter.StringVar(value="at_least_v3_14_0_0")

        # ≥ 3.14.0.0
        self.radiobutton_at_least_v3_14_0_0 = customtkinter.CTkRadioButton(
            self.mspcm_version_radiobutton_frame,
            text=self.app_translator.translate("pages.utilities.at_least_v3_14_0_0"),
            variable=self.mspcm_version_var,
            value="at_least_v3_14_0_0",
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_version_radiobutton_change
        )
        self.radiobutton_at_least_v3_14_0_0.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # < 3.14.0.0
        self.radiobutton_lower_than_v3_14_0_0 = customtkinter.CTkRadioButton(
            self.mspcm_version_radiobutton_frame,
            text=self.app_translator.translate("pages.utilities.lower_than_v3_14_0_0"),
            variable=self.mspcm_version_var,
            value="lower_than_v3_14_0_0",
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_version_radiobutton_change
        )
        self.radiobutton_lower_than_v3_14_0_0.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.switch_regions_card.configure(state="normal")

        # --- View Installed Security Products ---
        view_installed_security_products_frame = self._create_group_frame()
        self.view_installed_security_products_card = self._create_actions_card(
            view_installed_security_products_frame,
            title=self.app_translator.translate("pages.utilities.view_installed_security_products"),
            description=self.app_translator.translate("pages.utilities.view_installed_security_products_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_view_installed_security_products
        )

        self._create_separator(view_installed_security_products_frame)

        # - Security Products Types Checkboxes -
        self.security_products_types_frame = customtkinter.CTkScrollableFrame(
            view_installed_security_products_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.security_products_types_frame.pack(fill="x", padx=10, pady=5)

        # Antivirus
        self.checkbox_antivirus_product = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("pages.utilities.antivirus_product"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_antivirus_product.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Antispyware
        self.checkbox_antispyware_product = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("pages.utilities.antispyware_product"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_antispyware_product.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Firewall
        self.checkbox_firewall_product = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("pages.utilities.firewall_product"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_firewall_product.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Output as Raw Data
        self.output_as_raw_data_checkbox = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("pages.utilities.output_as_raw_data"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_output_raw_data_checkbox_change
        )
        self.output_as_raw_data_checkbox.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.output_as_raw_data_checkbox.configure(state="disabled")

        # Checkbox Configuration
        if PrerequisiteChecks.check_windows_server_levels(check_type="is_windows_server"):
            self.checkbox_antispyware_product.configure(state="disabled")
            self.checkbox_firewall_product.configure(state="disabled")

        self.view_installed_security_products_card.configure(state="disabled")
        # === End of Maintenance Management ===


    # ~~~ Features Functions ~~~
    # ~ Compute Files Hashes ~
    def _update_select_all_state(self):
        if all(cb.get() == 1 for cb in self.hash_checkbox_widgets.values()):
            self.select_all_checkbox.select()
        else:
            self.select_all_checkbox.deselect()
        self._update_compute_button_state()

    def _on_hash_checkbox_change(self):
        self._update_select_all_state()

    def _update_compute_button_state(self):
        if any(cb.get() == 1 for cb in self.hash_checkbox_widgets.values()):
            self.compute_files_hashes_card.configure(state="normal")
        else:
            self.compute_files_hashes_card.configure(state="disabled")

    def _toggle_select_all(self):
        state = self.select_all_checkbox.get()
        for cb in self.hash_checkbox_widgets.values():
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_compute_button_state()

    def _run_compute_hashes(self):
        self.compute_files_hashes_card.configure(state="disabled")
        self.update_idletasks()

        operation_name = self.app_translator.translate("pages.utilities.compute_files_hashes")

        hasher = ComputeFilesHashes(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_algos=[k for k, v in self.hash_checkbox_widgets.items() if v.get() == 1],
            uppercase_results=self.uppercase_all_results.get() == 1
        )

        files = hasher.select_files()
        if not files:
            # Keep cancel behavior consistent with normal operation flow.
            self.tabview.set(self.events_tab_name)
            self.events_textbox.clear_events()
            self.events_textbox.log_to_events(
                self.app_translator.translate("pages.common.executing_operation").format(operation_name=operation_name)
                + "\n"
                + self.app_translator.translate("pages.common.executing_operation_prompt")
                + "\n"
            )
            self.events_textbox.log_to_events(self.app_translator.translate("pages.common.canceled_operation"))
            self.logger.info(f"Executing Operation: {operation_name}")
            self.logger.info("The operation was canceled by the user.")
            self._update_compute_button_state()
            return

        self._run_operation(
            lambda: hasher.compute(files),
            "pages.utilities.compute_files_hashes",
            on_completion=self._update_compute_button_state
        )
    # ~ End of Compute Files Hashes ~

    # ~ Get Dependencies Versions ~
    def _on_dependencies_checkbox_change(self):
        if (
            self.checkbox_system_webview2.get() == 1 or
            self.checkbox_global_webview2.get() == 1 or
            self.checkbox_windows_app_runtime.get() == 1
        ):
            self.get_dependencies_versions_card.configure(state="normal")
        else:
            self.get_dependencies_versions_card.configure(state="disabled")

    def _run_get_dependencies_versions(self):
        self.get_dependencies_versions_card.configure(state="disabled")
        self.update_idletasks()

        selected_dependencies = []
        if self.checkbox_system_webview2.get() == 1:
            selected_dependencies.append("system_webview2")
        if self.checkbox_global_webview2.get() == 1:
            selected_dependencies.append("global_webview2")
        if self.checkbox_windows_app_runtime.get() == 1:
            selected_dependencies.append("windows_app_runtime")

        getter = GetDependenciesVersion(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_dependencies=selected_dependencies
        )

        self._run_operation(
            getter.execute,
            "pages.utilities.get_dependencies_versions",
            on_completion=self._on_dependencies_checkbox_change
        )
    # ~ End of Get Dependencies Versions ~

    # ~ Repair Microsoft Edge WebView2 Installation ~
    def _update_webview2_select_all_state(self):
        targets = [
            self.checkbox_restore_ifeo_registry,
            self.checkbox_remove_edgeupdate_registry,
            self.checkbox_remove_webview2_dir,
            self.checkbox_remove_edge_components_dir
        ]
        enabled_targets = [cb for cb in targets if cb.cget("state") != "disabled"]

        if not enabled_targets:
            self.checkbox_webview2_select_all.deselect()
            return

        if all(cb.get() == 1 for cb in enabled_targets):
            self.checkbox_webview2_select_all.select()
        else:
            self.checkbox_webview2_select_all.deselect()

    def _on_webview2_select_all_change(self):
        state = self.checkbox_webview2_select_all.get() == 1
        targets = [
            self.checkbox_restore_ifeo_registry,
            self.checkbox_remove_edgeupdate_registry,
            self.checkbox_remove_webview2_dir,
            self.checkbox_remove_edge_components_dir
        ]

        for cb in targets:
            if cb.cget("state") == "disabled":
                continue
            if state:
                cb.select()
            else:
                cb.deselect()

        self._on_webview2_repair_checkbox_change()

    def _on_webview2_repair_checkbox_change(self):
        # Uncheck the WebView2 directory when selecting to remove the Edge components directory.
        if self.checkbox_remove_edge_components_dir.get() == 1:
            self.checkbox_remove_webview2_dir.deselect()
            self.checkbox_remove_webview2_dir.configure(state="disabled")
        else:
            self.checkbox_remove_webview2_dir.configure(state="normal")

        if (
            self.checkbox_remove_webview2_dir.get() == 1 or
            self.checkbox_remove_edge_components_dir.get() == 1
        ):
            self.checkbox_end_related_processes.configure(state="normal")
        else:
            self.checkbox_end_related_processes.deselect()
            self.checkbox_end_related_processes.configure(state="disabled")

        if (
            self.checkbox_restore_ifeo_registry.get() == 1 or
            self.checkbox_remove_edgeupdate_registry.get() == 1 or
            self.checkbox_remove_webview2_dir.get() == 1 or
            self.checkbox_remove_edge_components_dir.get() == 1 or
            self.checkbox_end_related_processes.get() == 1
        ):
            self.repair_edge_webview_2_installation_card.configure(state="normal")
        else:
            self.repair_edge_webview_2_installation_card.configure(state="disabled")

        self._update_webview2_select_all_state()

    def _run_repair_edge_webview2_installation(self):
        self.repair_edge_webview_2_installation_card.configure(state="disabled")
        self.update_idletasks()

        selected_edge_webview2_repair_options = {
            "restore_ifeo_registry": self.checkbox_restore_ifeo_registry.get() == 1,
            "remove_edgeupdate_registry": self.checkbox_remove_edgeupdate_registry.get() == 1,
            "remove_webview2_dir": self.checkbox_remove_webview2_dir.get() == 1,
            "remove_edge_components_dir": self.checkbox_remove_edge_components_dir.get() == 1,
            "end_related_processes": self.checkbox_end_related_processes.get() == 1
        }

        repairer = RepairEdgeWebView2Installation(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_edge_webview2_repair_options=selected_edge_webview2_repair_options
        )

        self._run_operation(
            repairer.execute,
            "pages.utilities.repair_edge_webview_2_installation",
            on_completion=self._on_webview2_repair_checkbox_change
        )
    # ~ End of Repair Microsoft Edge WebView2 Installation ~

    # ~ Restart Services ~
    def _load_mspcm_versions_async(self):
        self.logger.debug("UtilitiesPage start async Microsoft PC Manager versions fetch.")
        threading.Thread(target=self._fetch_mspcm_versions, daemon=True).start()

    def _fetch_mspcm_versions(self):
        self.logger.debug("UtilitiesPage fetching Microsoft PC Manager versions in background thread.")
        start_fetch_mspcm_time = time.perf_counter()
        mspcm_version = GetMSPCMVersion.get_microsoft_pc_manager_version()
        mspcm_beta_version = GetMSPCMVersion.get_microsoft_pc_manager_beta_version()
        elapsed = time.perf_counter() - start_fetch_mspcm_time
        try:
            self.logger.debug(
                f"UtilitiesPage Fetch Microsoft PC Manager Versions Complete: Stable: {mspcm_version}, Beta: {mspcm_beta_version}"
            )
            self.logger.info(
                f"UtilitiesPage Fetch Microsoft PC Manager versions in: {elapsed:.5f} s"
            )
            self.after(0, lambda: self._apply_mspcm_versions(mspcm_version, mspcm_beta_version))
        except Exception:
            pass

    def _apply_mspcm_versions(self, mspcm_version, mspcm_beta_version):
        self.logger.debug("UtilitiesPage apply Microsoft PC Manager versions to UI.")
        if not self.winfo_exists():
            return

        if mspcm_version:
            self.checkbox_stable_version.configure(state="normal")
            self.checkbox_store_beta_version.configure(state="normal")
        else:
            self.checkbox_stable_version.configure(state="disabled")
            self.checkbox_store_beta_version.configure(state="disabled")

        if mspcm_beta_version:
            self.checkbox_beta_version.configure(state="normal")
        else:
            self.checkbox_beta_version.configure(state="disabled")

    def _on_mspcm_services_checkbox_change(self):
        if (
            self.checkbox_stable_version.get() == 1 or
            self.checkbox_beta_version.get() == 1 or
            self.checkbox_store_beta_version.get() == 1
        ):
            self.restart_services_card.configure(state="normal")
        else:
            self.restart_services_card.configure(state="disabled")

    def _run_restart_services(self):
        self.restart_services_card.configure(state="disabled")
        self.update_idletasks()

        selected_services = {
            "stable_version": self.checkbox_stable_version.get() == 1,
            "beta_version": self.checkbox_beta_version.get() == 1,
            "store_beta_version": self.checkbox_store_beta_version.get() == 1
        }

        restarter = RestartServices(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_services=selected_services
        )

        self._run_operation(
            lambda: restarter.execute(),
            "pages.utilities.restart_services",
            on_completion=lambda: self.restart_services_card.configure(state="normal")
        )
    # ~ End of Restart Services ~

    # ~ Switch Regions ~
    def _on_mspcm_version_radiobutton_change(self):
        value = self.mspcm_version_var.get()
        if value == "at_least_v3_14_0_0":
            self.switch_regions_card.configure(state="normal")
        elif value == "lower_than_v3_14_0_0":
            if AdvancedStartup.is_administrator():
                self.switch_regions_card.configure(state="normal")
            else:
                self.switch_regions_card.configure(state="disabled")
        else:
            self.switch_regions_card.configure(state="disabled")

    def _run_switch_regions(self):
        self.switch_regions_card.configure(state="disabled")
        self.update_idletasks()

        switcher = SwitchRegions(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_mspcm_version=self.mspcm_version_var.get(),
            font_family=self.font_family
        )

        self._run_operation(
            lambda: switcher.execute(),
            "pages.utilities.switch_regions",
            on_completion=lambda: self.switch_regions_card.configure(state="normal")
        )
    # ~ End of Switch Regions ~

    # ~ View Installed Security Products ~
    def _on_output_raw_data_checkbox_change(self):
        if (
            self.output_as_raw_data_checkbox.get() == 0 and
            self.checkbox_antivirus_product.get() == 1 and
            PrerequisiteChecks.check_windows_server_levels(check_type="is_windows_server")
        ):
            self.checkbox_antivirus_product.deselect()
            self._on_security_products_checkbox_change()

    def _on_security_products_checkbox_change(self):
        if (
            self.checkbox_antivirus_product.get() == 1 or
            self.checkbox_antispyware_product.get() == 1 or
            self.checkbox_firewall_product.get() == 1
        ):
            self.view_installed_security_products_card.configure(state="normal")
            self.output_as_raw_data_checkbox.configure(state="normal")

            if (
                self.checkbox_antivirus_product.get() == 1 and
                PrerequisiteChecks.check_windows_server_levels(check_type="is_windows_server")
            ):
                self.output_as_raw_data_checkbox.select()
        else:
            self.view_installed_security_products_card.configure(state="disabled")
            self.output_as_raw_data_checkbox.deselect()
            self.output_as_raw_data_checkbox.configure(state="disabled")

    def _run_view_installed_security_products(self):
        self.view_installed_security_products_card.configure(state="disabled")
        self.update_idletasks()

        selected_products = []
        if self.checkbox_antivirus_product.get() == 1:
            selected_products.append("antivirus")
        if self.checkbox_antispyware_product.get() == 1:
            selected_products.append("antispyware")
        if self.checkbox_firewall_product.get() == 1:
            selected_products.append("firewall")

        viewer = ViewInstalledSecurityProducts(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_security_product=selected_products,
            output_as_raw_data=self.output_as_raw_data_checkbox.get() == 1
        )

        self._run_operation(
            lambda: viewer.execute(),
            "pages.utilities.view_installed_security_products",
            on_completion=lambda: self.view_installed_security_products_card.configure(state="normal")
        )
    # ~ End of View Installed Security Products ~
