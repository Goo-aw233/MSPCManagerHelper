import threading
import tkinter

import customtkinter
from CTkToolTip import CTkToolTip

from core.advanced_startup import AdvancedStartup
from core.app_logger import AppLogger
from core.app_settings import AppSettings
from core.get_mspcm_version import GetMSPCMVersion
from core.system_checks import OptionalChecks, PrerequisiteChecks
from modules.utilities import *


class UtilitiesPage(customtkinter.CTkFrame):
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
            text=self.app_translator.translate("utilities_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Tab Switching
        self.tabview = customtkinter.CTkTabview(self, fg_color="transparent")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.tabview.grid_columnconfigure(0, weight=1)
        self.tabview._segmented_button.configure(
            font=customtkinter.CTkFont(family=self.font_family, size=14, weight="bold"))

        self.features_tab_name = self.app_translator.translate("features_tab")
        self.events_tab_name = self.app_translator.translate("events_tab")

        self.tabview.add(self.features_tab_name)
        self.tabview.add(self.events_tab_name)
        self.tabview.set(self.features_tab_name)

        # Scrollable Content (Features Tab)
        self.scroll_frame = customtkinter.CTkScrollableFrame(self.tabview.tab(self.features_tab_name),
                                                             fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Events Textbox (Events Tab)
        self.events_textbox_description = customtkinter.CTkLabel(
            self.tabview.tab(self.events_tab_name),
            text=self.app_translator.translate("events_textbox_description"),
            font=customtkinter.CTkFont(family=self.font_family, size=13),
            anchor="center"
        )
        self.events_textbox_description.pack(fill="x", padx=12, pady=(10, 0))

        self.events_textbox = customtkinter.CTkTextbox(
            self.tabview.tab(self.events_tab_name),
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            state="disabled",
            wrap="none"
        )
        # Configure tab stops: "5c" means a tab stop at 5cm.
        self.events_textbox._textbox.configure(tabs=("5c",))
        self.events_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Right-Click Menu for Events Textbox
        self.right_click_menu = tkinter.Menu(self.events_textbox, tearoff=0)
        self.right_click_menu.add_command(label=self.app_translator.translate("copy_button"),
                                          command=self._copy_events)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=self.app_translator.translate("clear_button"),
                                          command=self._clear_events)

        self.events_textbox.bind("<Button-3>", self._show_right_click_menu)

        # === File Management ===
        self._create_section_label(self.app_translator.translate("file_management"))

        file_management_frame = self._create_group_frame()

        # --- Compute Files Hashes ---
        self.compute_files_hashes_card = self._create_settings_card(
            file_management_frame,
            title=self.app_translator.translate("compute_files_hashes_title"),
            description=self.app_translator.translate("compute_files_hashes_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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
            text=self.app_translator.translate("select_all"),
            command=self._toggle_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.select_all_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.uppercase_all_results = customtkinter.CTkCheckBox(
            self.hash_checkboxes_frame,
            text=self.app_translator.translate("uppercase_all_results"),
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
            "shake_128": "shake_128_tooltip",
            "shake_256": "shake_256_tooltip",
            "blake2b": "blake2b_tooltip",
            "blake2s": "blake2s_tooltip"
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
        self._create_section_label(self.app_translator.translate("open_to_section"))

        open_to_frame = self._create_group_frame()

        # --- Open Developer Settings ---
        self.open_developer_settings_card = self._create_settings_card(
            open_to_frame,
            title=self.app_translator.translate("open_developer_settings_title"),
            description=self.app_translator.translate("open_developer_settings_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
            command=lambda: OpenDeveloperSettings.open_developer_settings(
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )

        # --- Separator ---
        self._create_separator(open_to_frame)

        # --- Open Microsoft PC Manager Documentation ---
        self.open_mspcm_doc_card = self._create_settings_card(
            open_to_frame,
            title=self.app_translator.translate("open_mspcm_doc_title"),
            description=self.app_translator.translate("open_mspcm_doc_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
            command=lambda: OpenMSPCMDoc.open_mspcm_doc(
                logger=self.logger,
                log_file_path=self.log_file_path,
                app_translator=self.app_translator
            )
        )
        # === End of Open To ===

        # === Maintenance Management ===
        self._create_section_label(self.app_translator.translate("maintenance_management"))

        # --- Get Dependencies Versions ---
        get_dependencies_versions_frame = self._create_group_frame()
        get_dependencies_versions_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.get_dependencies_versions_card = self._create_settings_card(
            get_dependencies_versions_frame,
            title=self.app_translator.translate("get_dependencies_versions_title"),
            description=self.app_translator.translate("get_dependencies_versions_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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
            text=self.app_translator.translate("system_webview2_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_dependencies_checkbox_change
        )
        self.checkbox_system_webview2.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_system_webview2, message=fr"%SystemRoot%\System32\Microsoft-Edge-WebView",
                   font=(self.font_family, 12))

        # Global WebView2
        self.checkbox_global_webview2 = customtkinter.CTkCheckBox(
            self.dependencies_types_frame,
            text=self.app_translator.translate("global_webview2_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_dependencies_checkbox_change
        )
        self.checkbox_global_webview2.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_global_webview2, message=fr"%ProgramFiles(x86)%\Microsoft\EdgeWebView",
                   font=(self.font_family, 12))

        # Windows App Runtime
        self.checkbox_windows_app_runtime = customtkinter.CTkCheckBox(
            self.dependencies_types_frame,
            text=self.app_translator.translate("windows_app_runtime_checkbox"),
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
        self.repair_edge_webview_2_installation_card = self._create_settings_card(
            repair_edge_webview_2_installation_frame,
            title=self.app_translator.translate("repair_edge_webview_2_installation_title"),
            description=self.app_translator.translate("repair_edge_webview_2_installation_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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

        # Restore IFEO Registry
        self.checkbox_restore_ifeo_registry = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("restore_ifeo_registry_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_restore_ifeo_registry.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_restore_ifeo_registry,
                   message=self.app_translator.translate("restore_ifeo_registry_tooltip"), font=(self.font_family, 12))

        # Remove WebView2 Directory
        self.checkbox_remove_webview2_dir = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("remove_webview2_dir_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_remove_webview2_dir.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_remove_webview2_dir, message=fr"%ProgramFiles(x86)%\Microsoft\EdgeWebView",
                   font=(self.font_family, 12))

        # Remove WebView2 Parent Directory
        self.checkbox_remove_webview2_parent_dir = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("remove_webview2_parent_dir_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_remove_webview2_parent_dir.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_remove_webview2_parent_dir, message=fr"%ProgramFiles(x86)%\Microsoft",
                   font=(self.font_family, 12))

        # End Related Processes
        self.checkbox_end_related_processes = customtkinter.CTkCheckBox(
            self.webview2_repair_options_frame,
            text=self.app_translator.translate("end_related_processes_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family, weight="bold"),
            command=self._on_webview2_repair_checkbox_change
        )
        self.checkbox_end_related_processes.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_end_related_processes,
                   message=self.app_translator.translate("end_related_processes_tooltip"), font=(self.font_family, 12))
        self.checkbox_end_related_processes.configure(state="disabled")

        # Checkbox Configuration
        if not AdvancedStartup.is_administrator():
            self.checkbox_restore_ifeo_registry.configure(state="disabled")
            self.checkbox_remove_webview2_dir.configure(state="disabled")
            self.checkbox_remove_webview2_parent_dir.configure(state="disabled")
            self.checkbox_end_related_processes.configure(state="disabled")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility="reg.exe"):
            self.checkbox_restore_ifeo_registry.configure(state="disabled")
            self.logger.warning("reg.exe is not available. Disabling IFEO Registry Repair Checkbox.")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility=["cmd.exe", "powershell.exe"]):
            self.checkbox_remove_webview2_dir.configure(state="disabled")
            self.logger.warning("cmd.exe or powershell.exe is not available. Disabling WebView2 Directory Removal Checkbox.")
            self.checkbox_remove_webview2_parent_dir.configure(state="disabled")
            self.logger.warning("cmd.exe or powershell.exe is not available. Disabling WebView2 Parent Directory Removal Checkbox.")

        if AppSettings.is_take_ownership_enabled() and not OptionalChecks.check_windows_utilities_availability(target_utility=["taskkill.exe"]):
            self.checkbox_end_related_processes.configure(state="disabled")
            self.logger.warning("taskkill.exe is not available. Disabling End Related Processes Checkbox.")

        self.repair_edge_webview_2_installation_card.configure(state="disabled")

        # --- Restart Services ---
        restart_services_frame = self._create_group_frame()
        restart_services_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.restart_services_card = self._create_settings_card(
            restart_services_frame,
            title=self.app_translator.translate("restart_services_title"),
            description=self.app_translator.translate("restart_services_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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
            text=self.app_translator.translate("stable_version_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_stable_version.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_stable_version, message="Microsoft.MicrosoftPCManager_8wekyb3d8bbwe",
                   font=(self.font_family, 12))

        # PCManager Service
        self.checkbox_beta_version = customtkinter.CTkCheckBox(
            self.mspcm_services_checkboxes_frame,
            text=self.app_translator.translate("beta_version_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_beta_version.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_beta_version, message=self.app_translator.translate("beta_version_tooltip"),
                   font=(self.font_family, 12))

        # PC Manager Service
        self.checkbox_store_beta_version = customtkinter.CTkCheckBox(
            self.mspcm_services_checkboxes_frame,
            text=self.app_translator.translate("store_beta_version_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_services_checkbox_change
        )
        self.checkbox_store_beta_version.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        CTkToolTip(self.checkbox_store_beta_version, message="Microsoft.PCManager_8wekyb3d8bbwe",
                   font=(self.font_family, 12))

        # Checkbox Configuration
        mspcm_version = GetMSPCMVersion.get_microsoft_pc_manager_version()
        if mspcm_version:
            self.checkbox_stable_version.configure(state="normal")
            self.checkbox_store_beta_version.configure(state="normal")
        else:
            self.checkbox_stable_version.configure(state="disabled")
            self.checkbox_store_beta_version.configure(state="disabled")

        mspcm_beta_version = GetMSPCMVersion.get_microsoft_pc_manager_beta_version()
        if mspcm_beta_version:
            self.checkbox_beta_version.configure(state="normal")
        else:
            self.checkbox_beta_version.configure(state="disabled")
        
        self.restart_services_card.configure(state="disabled")

        # --- Switch Regions ---
        switch_regions_frame = self._create_group_frame()
        switch_regions_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.switch_regions_card = self._create_settings_card(
            switch_regions_frame,
            title=self.app_translator.translate("switch_regions_title"),
            description=self.app_translator.translate("switch_regions_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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

        self.mspcm_version_var = tkinter.StringVar(value="v3_14_0_0_and_higher")

        # ≥ 3.14.0.0
        self.radiobutton_v3_14_0_0_and_higher = customtkinter.CTkRadioButton(
            self.mspcm_version_radiobutton_frame,
            text=self.app_translator.translate("v3_14_0_0_and_higher_radiobutton"),
            variable=self.mspcm_version_var,
            value="v3_14_0_0_and_higher",
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_version_radiobutton_change
        )
        self.radiobutton_v3_14_0_0_and_higher.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # < 3.14.0.0
        self.radiobutton_lower_than_v3_14_0_0 = customtkinter.CTkRadioButton(
            self.mspcm_version_radiobutton_frame,
            text=self.app_translator.translate("lower_than_v3_14_0_0_radiobutton"),
            variable=self.mspcm_version_var,
            value="lower_than_v3_14_0_0",
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_mspcm_version_radiobutton_change
        )
        self.radiobutton_lower_than_v3_14_0_0.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.switch_regions_card.configure(state="normal")

        # --- View Installed Security Products ---
        view_installed_security_products_frame = self._create_group_frame()
        self.view_installed_security_products_card = self._create_settings_card(
            view_installed_security_products_frame,
            title=self.app_translator.translate("view_installed_security_products_title"),
            description=self.app_translator.translate("view_installed_security_products_description"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("execute_button"),
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
            text=self.app_translator.translate("antivirus_product_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_antivirus_product.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Antispyware
        self.checkbox_antispyware_product = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("antispyware_product_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_antispyware_product.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Firewall
        self.checkbox_firewall_product = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("firewall_product_checkbox"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._on_security_products_checkbox_change
        )
        self.checkbox_firewall_product.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Output as Raw Data
        self.output_as_raw_data_checkbox = customtkinter.CTkCheckBox(
            self.security_products_types_frame,
            text=self.app_translator.translate("output_as_raw_data_checkbox"),
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

        hasher = ComputeFilesHashes(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self._log_to_events,
            selected_algos=[k for k, v in self.hash_checkbox_widgets.items() if v.get() == 1],
            uppercase_results=self.uppercase_all_results.get() == 1
        )

        files = hasher.select_files()
        if not files:
            self._log_to_events(self.app_translator.translate("user_has_canceled_the_operation"))
            self._update_compute_button_state()
            return

        self._run_operation(
            lambda: hasher.compute(files),
            "compute_files_hashes_title",
            on_completion=self._update_compute_button_state
        )
    # ~ End of Compute File Hashes ~

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
            log_callback=self._log_to_events,
            selected_dependencies=selected_dependencies
        )

        self._run_operation(
            getter.execute,
            "get_dependencies_versions_title",
            on_completion=self._on_dependencies_checkbox_change
        )
    # ~ End of Get Dependencies Versions ~

    # ~ Repair Microsoft Edge WebView2 Installation ~
    def _on_webview2_repair_checkbox_change(self):
        # Uncheck the WebView2 folder when selecting to remove the parent folder.
        if self.checkbox_remove_webview2_parent_dir.get() == 1:
            self.checkbox_remove_webview2_dir.deselect()
            self.checkbox_remove_webview2_dir.configure(state="disabled")
        else:
            self.checkbox_remove_webview2_dir.configure(state="normal")

        if (
            self.checkbox_remove_webview2_dir.get() == 1 or
            self.checkbox_remove_webview2_parent_dir.get() == 1
        ):
            self.checkbox_end_related_processes.configure(state="normal")
        else:
            self.checkbox_end_related_processes.deselect()
            self.checkbox_end_related_processes.configure(state="disabled")

        if (
            self.checkbox_restore_ifeo_registry.get() == 1 or
            self.checkbox_remove_webview2_dir.get() == 1 or
            self.checkbox_remove_webview2_parent_dir.get() == 1 or
            self.checkbox_end_related_processes.get() == 1
        ):
            self.repair_edge_webview_2_installation_card.configure(state="normal")
        else:
            self.repair_edge_webview_2_installation_card.configure(state="disabled")

    def _run_repair_edge_webview2_installation(self):
        self.repair_edge_webview_2_installation_card.configure(state="disabled")
        self.update_idletasks()

        selected_edge_wv2_repair_options = {
            "restore_ifeo_registry": self.checkbox_restore_ifeo_registry.get() == 1,
            "remove_webview2_dir": self.checkbox_remove_webview2_dir.get() == 1,
            "remove_webview2_parent_dir": self.checkbox_remove_webview2_parent_dir.get() == 1,
            "end_related_processes": self.checkbox_end_related_processes.get() == 1
        }

        repairer = RepairEdgeWebView2Installation(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self._log_to_events,
            selected_edge_wv2_repair_options=selected_edge_wv2_repair_options
        )

        self._run_operation(
            repairer.execute,
            "repair_edge_webview_2_installation_title",
            on_completion=self._on_webview2_repair_checkbox_change
        )
    # ~ End of Repair Microsoft Edge WebView2 Installation ~

    # ~ Restart Services ~
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
            log_callback=self._log_to_events,
            selected_services=selected_services
        )

        self._run_operation(
            lambda: restarter.execute(),
            "restart_services_title",
            on_completion=lambda: self.restart_services_card.configure(state="normal")
        )
    # ~ End of Restart Services ~

    # ~ Switch Regions ~
    def _on_mspcm_version_radiobutton_change(self):
        value = self.mspcm_version_var.get()
        if value == "v3_14_0_0_and_higher":
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
            log_callback=self._log_to_events,
            selected_mspcm_version=self.mspcm_version_var.get(),
            font_family=self.font_family
        )

        self._run_operation(
            lambda: switcher.execute(),
            "switch_regions_title",
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
            log_callback=self._log_to_events,
            selected_security_product=selected_products,
            output_as_raw_data=self.output_as_raw_data_checkbox.get() == 1
        )

        self._run_operation(
            lambda: viewer.execute(),
            "view_installed_security_products_title",
            on_completion=lambda: self.view_installed_security_products_card.configure(state="normal")
        )
    # ~ End of View Installed Security Products ~

    # ~~~ GUI/Events Functions ~~~
    def _run_operation(self, operation_func, operation_name_key, on_completion=None):
        self.tabview.set(self.events_tab_name)
        operation_name = self.app_translator.translate(operation_name_key)
        message = (
            f"{self.app_translator.translate('executing_operation_with_name').format(operation_name=operation_name)}\n"
            f"{self.app_translator.translate('please_wait_for_completion')}\n"
        )
        self.logger.info(f"Executing Operation: {operation_name}")

        # Reset Events Textbox on Main Thread
        self.events_textbox.configure(state="normal")
        self.events_textbox.delete("1.0", "end")
        self.events_textbox.insert("end", message + "\n")
        self.events_textbox.see("end")
        self.events_textbox.configure(state="disabled")

        def _thread_target():
            try:
                operation_func()
                self._log_to_events(
                    self.app_translator.translate("operation_completed").format(operation_name=operation_name))
                self.logger.info(f"Completed Operation: {operation_name}")
            except Exception as e:
                self.logger.error(f"Error Executing {operation_name}: {e}")
                self._log_to_events(f"Error: {e}")
            finally:
                if on_completion:
                    self.after(0, on_completion)

        threading.Thread(target=_thread_target, daemon=True).start()

    def _show_right_click_menu(self, event):
        bg = self._apply_appearance_mode(["#e3e3e3", "#333333"])
        fg = self._apply_appearance_mode(["#191919", "#e2e2e2"])
        active_bg = self._apply_appearance_mode(["#bebebe", "#464646"])
        active_fg = self._apply_appearance_mode(["#191919", "#e2e2e2"])

        self.right_click_menu.configure(
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=active_fg,
            font=(self.font_family, 10)
        )
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def _copy_events(self):
        try:
            selected_text = self.events_textbox.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tkinter.TclError:
            # Copy All Text If No Selection
            all_text = self.events_textbox.get("1.0", "end-1c")
            if all_text:
                self.clipboard_clear()
                self.clipboard_append(all_text)

    def _clear_events(self):
        self.events_textbox.configure(state="normal")
        self.events_textbox.delete("1.0", "end")
        self.events_textbox.configure(state="disabled")

    def _log_to_events(self, message):
        self.after(0, self._append_to_events_textbox, message)

    def _append_to_events_textbox(self, message):
        self.events_textbox.configure(state="normal")
        self.events_textbox.insert("end", message + "\n")
        self.events_textbox.see("end")
        self.events_textbox.configure(state="disabled")

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
        separator = customtkinter.CTkFrame(parent, height=2, fg_color=("gray90", "#2b2b2b"))
        separator.pack(fill="x", padx=10)
        return separator

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
