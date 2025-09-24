import customtkinter
import threading
import tkinter

from CTkToolTip import CTkToolTip
from core.utils.compute_files_hash import ComputeFilesHash
from core.utils.get_microsoft_edge_webview2_runtime_version import GetMicrosoftEdgeWebView2RuntimeVersion
from core.utils.open_developer_settings import OpenDeveloperSettings
from core.utils.open_product_documentation import OpenProductDocumentation
from core.utils.repair_microsoftedgeupdate_not_working import RepairMicrosoftEdgeUpdateNotWorking
from core.utils.restart_service import RestartService
from core.utils.switch_regions import SwitchRegions
from core.utils.view_installed_antivirus_products import ViewInstalledAntiVirusProducts
from ..modules.program_settings import ProgramSettings


class UtilsPageFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font_family=None, translator=None, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, *args, **kwargs)
        self.font_family = font_family
        self.translator = translator
        self.compute_hash_util = ComputeFilesHash(translator=self.translator)
        self.get_webview2_version_util = GetMicrosoftEdgeWebView2RuntimeVersion(translator=self.translator)
        self.open_dev_settings_util = OpenDeveloperSettings(translator=self.translator)
        self.open_prod_doc_util = OpenProductDocumentation(translator=self.translator)
        self.repair_edgeupdate_util = RepairMicrosoftEdgeUpdateNotWorking(translator=self.translator)
        self.restart_service_util = RestartService(translator=self.translator)
        self.switch_regions_util = SwitchRegions(translator=self.translator)
        self.view_antivirus_util = ViewInstalledAntiVirusProducts(translator=self.translator)

        # 配置网格权重
        self.grid_columnconfigure(0, weight=1)
        # 初始化主框架的行计数器
        current_row = 0

        """----- Page Configurations -----"""

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.translator.translate("utils_page"),
            font=(self.font_family, 20, "bold"),
            anchor="center"
        )
        self.title_label.grid(row=current_row, column=0, pady=(20, 10), sticky="ew")
        self.title_label.bind("<Configure>", lambda event: self.title_label.configure(
            wraplength=self.title_label.winfo_width() - 20))
        current_row += 1

        # Create Tab View
        self.tab_view = customtkinter.CTkTabview(self, corner_radius=8, border_width=1)
        self.tab_view.grid(row=current_row, column=0, padx=20, pady=10, sticky="nsew")
        self.tab_view._segmented_button.configure(font=(self.font_family, 12))
        self.grid_rowconfigure(current_row, weight=1)  # Allow tab view to expand vertically
        current_row += 1

        # Add Tabs
        features_tab_name = self.translator.translate("features_tab")
        event_output_tab_name = self.translator.translate("event_output_tab")
        self.tab_view.add(features_tab_name)
        self.tab_view.add(event_output_tab_name)

        # Configure Features Tab
        features_tab = self.tab_view.tab(features_tab_name)
        features_tab.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab = 0

        # !Compute Files Hash Frame
        self.compute_files_hash_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.compute_files_hash_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(10, 5), sticky="ew")
        self.compute_files_hash_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_compute_hash_frame = 0
        self.compute_files_hash_title_label = customtkinter.CTkLabel(
            self.compute_files_hash_frame,
            text=self.translator.translate("compute_files_hash"),
            font=(self.font_family, 16, "bold")
        )
        self.compute_files_hash_title_label.grid(row=current_row_in_compute_hash_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.compute_files_hash_title_label.bind("<Configure>", lambda event: self.compute_files_hash_title_label.configure(
            wraplength=self.compute_files_hash_frame.winfo_width() - 20))
        current_row_in_compute_hash_frame += 1

        self.compute_files_hash_description_label = customtkinter.CTkLabel(
            self.compute_files_hash_frame,
            text=self.translator.translate("compute_files_hash_description"),
            font=(self.font_family, 12)
        )
        self.compute_files_hash_description_label.grid(row=current_row_in_compute_hash_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.compute_files_hash_description_label.bind("<Configure>", lambda event: self.compute_files_hash_description_label.configure(
            wraplength=self.compute_files_hash_frame.winfo_width() - 20))
        current_row_in_compute_hash_frame += 1

        # Checkboxes Frame for Hash Algorithms
        self.hash_checkboxes_frame = customtkinter.CTkFrame(self.compute_files_hash_frame, fg_color="transparent")
        self.hash_checkboxes_frame.grid(row=current_row_in_compute_hash_frame, column=0, padx=10, pady=(0, 5), sticky="ew")
        current_row_in_compute_hash_frame += 1

        hash_algorithms = [
            "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512",
            "BLAKE2b", "BLAKE2s", "SHA3-224", "SHA3-256", "SHA3-384",
            "SHA3-512", "SHAKE-128", "SHAKE-256"
        ]

        self.hash_checkboxes = {}
        num_columns = 3  # Arrange Checkboxes in 3 Columns
        for i, algo in enumerate(hash_algorithms):
            row = i // num_columns
            col = i % num_columns
            self.hash_checkboxes_frame.grid_columnconfigure(col, weight=1)
            
            checkbox = customtkinter.CTkCheckBox(
                self.hash_checkboxes_frame,
                text=algo,
                font=(self.font_family, 12),
                command=self._update_compute_hash_button_state
            )
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            # Store Checkbox With A Key Matching the Algorithm Name in Lowercase
            self.hash_checkboxes[algo.lower().replace("-", "_")] = checkbox

        # Execute Button
        self.compute_hash_button = customtkinter.CTkButton(
            self.compute_files_hash_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_compute_hash_button_click
        )
        self.compute_hash_button.grid(row=current_row_in_compute_hash_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_compute_hash_frame += 1

        # Set Initial State of the Button
        self._update_compute_hash_button_state()

        # !Get Microsoft Edge WebView2 Runtime Version Frame
        self.get_webview2_version_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.get_webview2_version_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.get_webview2_version_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_get_version_frame = 0
        self.get_webview2_version_title_label = customtkinter.CTkLabel(
            self.get_webview2_version_frame,
            text=self.translator.translate("get_microsoft_edge_webview2_runtime_version"),
            font=(self.font_family, 16, "bold")
        )
        self.get_webview2_version_title_label.grid(row=current_row_in_get_version_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.get_webview2_version_title_label.bind("<Configure>", lambda event: self.get_webview2_version_title_label.configure(
            wraplength=self.get_webview2_version_frame.winfo_width() - 20))
        current_row_in_get_version_frame += 1

        self.get_webview2_version_description_label = customtkinter.CTkLabel(
            self.get_webview2_version_frame,
            text=self.translator.translate("get_microsoft_edge_webview2_runtime_version_description"),
            font=(self.font_family, 12)
        )
        self.get_webview2_version_description_label.grid(row=current_row_in_get_version_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.get_webview2_version_description_label.bind("<Configure>", lambda event: self.get_webview2_version_description_label.configure(
            wraplength=self.get_webview2_version_frame.winfo_width() - 20))
        current_row_in_get_version_frame += 1

        # Checkboxes Frame for WebView2 Versions
        self.webview2_checkboxes_frame = customtkinter.CTkFrame(self.get_webview2_version_frame, fg_color="transparent")
        self.webview2_checkboxes_frame.grid(row=current_row_in_get_version_frame, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.webview2_checkboxes_frame.grid_columnconfigure(0, weight=1)
        self.webview2_checkboxes_frame.grid_columnconfigure(1, weight=1)
        current_row_in_get_version_frame += 1

        self.webview2_checkboxes = {}
        self.webview2_checkboxes["global"] = customtkinter.CTkCheckBox(
            self.webview2_checkboxes_frame,
            text=self.translator.translate("global_microsoft_edge_webview2_runtime_version"),
            font=(self.font_family, 12),
            command=self._update_get_webview2_version_button_state
        )
        self.webview2_checkboxes["global"].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.global_webview2_path_tooltip = CTkToolTip(
            self.webview2_checkboxes["global"],
            message="%ProgramFiles(x86)%\\Microsoft\\EdgeWebView",
            corner_radius=8
        )

        self.webview2_checkboxes["system"] = customtkinter.CTkCheckBox(
            self.webview2_checkboxes_frame,
            text=self.translator.translate("system_microsoft_edge_webview2_runtime_version"),
            font=(self.font_family, 12),
            command=self._update_get_webview2_version_button_state
        )
        self.webview2_checkboxes["system"].grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.system_webview2_path_tooltip = CTkToolTip(
            self.webview2_checkboxes["system"],
            message="%SystemRoot%\\System32\\Microsoft-Edge-WebView",
            corner_radius=8
        )

        # Execute Button for WebView2 Version
        self.get_webview2_version_button = customtkinter.CTkButton(
            self.get_webview2_version_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_get_webview2_version_button_click
        )
        self.get_webview2_version_button.grid(row=current_row_in_get_version_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_get_version_frame += 1

        # Set Initial State of the Button
        self._update_get_webview2_version_button_state()

        # !Open Developer Settings Frame
        self.open_dev_settings_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.open_dev_settings_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.open_dev_settings_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_dev_settings_frame = 0
        self.open_dev_settings_title_label = customtkinter.CTkLabel(
            self.open_dev_settings_frame,
            text=self.translator.translate("open_developer_settings"),
            font=(self.font_family, 16, "bold")
        )
        self.open_dev_settings_title_label.grid(row=current_row_in_dev_settings_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.open_dev_settings_title_label.bind("<Configure>", lambda event: self.open_dev_settings_title_label.configure(
            wraplength=self.open_dev_settings_frame.winfo_width() - 20))
        current_row_in_dev_settings_frame += 1

        self.open_dev_settings_description_label = customtkinter.CTkLabel(
            self.open_dev_settings_frame,
            text=self.translator.translate("open_developer_settings_description"),
            font=(self.font_family, 12)
        )
        self.open_dev_settings_description_label.grid(row=current_row_in_dev_settings_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.open_dev_settings_description_label.bind("<Configure>", lambda event: self.open_dev_settings_description_label.configure(
            wraplength=self.open_dev_settings_frame.winfo_width() - 20))
        current_row_in_dev_settings_frame += 1

        # Execute Button for Open Developer Settings
        self.open_dev_settings_button = customtkinter.CTkButton(
            self.open_dev_settings_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_open_dev_settings_button_click
        )
        self.open_dev_settings_button.grid(row=current_row_in_dev_settings_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_dev_settings_frame += 1

        # !Open Product Documentation Frame
        self.open_prod_doc_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.open_prod_doc_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.open_prod_doc_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_prod_doc_frame = 0
        self.open_prod_doc_title_label = customtkinter.CTkLabel(
            self.open_prod_doc_frame,
            text=self.translator.translate("open_product_documentation"),
            font=(self.font_family, 16, "bold")
        )
        self.open_prod_doc_title_label.grid(row=current_row_in_prod_doc_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.open_prod_doc_title_label.bind("<Configure>", lambda event: self.open_prod_doc_title_label.configure(
            wraplength=self.open_prod_doc_frame.winfo_width() - 20))
        current_row_in_prod_doc_frame += 1

        self.open_prod_doc_description_label = customtkinter.CTkLabel(
            self.open_prod_doc_frame,
            text=self.translator.translate("open_product_documentation_description"),
            font=(self.font_family, 12)
        )
        self.open_prod_doc_description_label.grid(row=current_row_in_prod_doc_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.open_prod_doc_description_label.bind("<Configure>", lambda event: self.open_prod_doc_description_label.configure(
            wraplength=self.open_prod_doc_frame.winfo_width() - 20))
        current_row_in_prod_doc_frame += 1

        # Execute Button for Open Product Documentation
        self.open_prod_doc_button = customtkinter.CTkButton(
            self.open_prod_doc_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_open_prod_doc_button_click
        )
        self.open_prod_doc_button.grid(row=current_row_in_prod_doc_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_prod_doc_frame += 1

        # !Repair MicrosoftEdgeUpdate Not Working Frame
        self.repair_edgeupdate_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.repair_edgeupdate_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.repair_edgeupdate_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_repair_edgeupdate_frame = 0
        self.repair_edgeupdate_title_label = customtkinter.CTkLabel(
            self.repair_edgeupdate_frame,
            text=self.translator.translate("repair_microsoftedgeupdate_not_working"),
            font=(self.font_family, 16, "bold")
        )
        self.repair_edgeupdate_title_label.grid(row=current_row_in_repair_edgeupdate_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.repair_edgeupdate_title_label.bind("<Configure>", lambda event: self.repair_edgeupdate_title_label.configure(
            wraplength=self.repair_edgeupdate_frame.winfo_width() - 20))
        current_row_in_repair_edgeupdate_frame += 1

        self.repair_edgeupdate_description_label = customtkinter.CTkLabel(
            self.repair_edgeupdate_frame,
            text=self.translator.translate("repair_microsoftedgeupdate_not_working_description"),
            font=(self.font_family, 12)
        )
        self.repair_edgeupdate_description_label.grid(row=current_row_in_repair_edgeupdate_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.repair_edgeupdate_description_label.bind("<Configure>", lambda event: self.repair_edgeupdate_description_label.configure(
            wraplength=self.repair_edgeupdate_frame.winfo_width() - 20))
        current_row_in_repair_edgeupdate_frame += 1

        # Checkboxes Frame for Repair Options
        self.repair_edgeupdate_checkboxes_frame = customtkinter.CTkFrame(self.repair_edgeupdate_frame, fg_color="transparent")
        self.repair_edgeupdate_checkboxes_frame.grid(row=current_row_in_repair_edgeupdate_frame, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.repair_edgeupdate_checkboxes_frame.grid_columnconfigure(0, weight=1)
        current_row_in_repair_edgeupdate_frame += 1

        self.repair_edgeupdate_checkboxes = {}
        self.repair_edgeupdate_checkboxes["restore_edgeupdate_ifeo_key"] = customtkinter.CTkCheckBox(
            self.repair_edgeupdate_checkboxes_frame,
            text=self.translator.translate("restore_edgeupdate_ifeo_key"),
            font=(self.font_family, 12),
            command=self._update_repair_edgeupdate_button_state
        )
        self.repair_edgeupdate_checkboxes["restore_edgeupdate_ifeo_key"].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.restore_edgeupdate_ifeo_key_tooltip = CTkToolTip(
            self.repair_edgeupdate_checkboxes["restore_edgeupdate_ifeo_key"],
            message=self.translator.translate("restore_edgeupdate_ifeo_reg_key_to_default_tip"),
            corner_radius=8
        )

        self.repair_edgeupdate_checkboxes["remove_edge_parent_folder"] = customtkinter.CTkCheckBox(
            self.repair_edgeupdate_checkboxes_frame,
            text=self.translator.translate("remove_microsoft_edge_parent_folder"),
            font=(self.font_family, 12),
            command=self._on_remove_edge_parent_folder_toggle
        )
        self.repair_edgeupdate_checkboxes["remove_edge_parent_folder"].grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.remove_edge_parent_folder_tooltip = CTkToolTip(
            self.repair_edgeupdate_checkboxes["remove_edge_parent_folder"],
            message=self.translator.translate("delete_microsoft_edge_webview2_parent_folder_tip"),
            corner_radius=8
        )

        self.repair_edgeupdate_checkboxes["remove_webview2_folder"] = customtkinter.CTkCheckBox(
            self.repair_edgeupdate_checkboxes_frame,
            text=self.translator.translate("remove_microsoft_edge_webview2_folder"),
            font=(self.font_family, 12),
            command=self._update_repair_edgeupdate_button_state
        )
        self.repair_edgeupdate_checkboxes["remove_webview2_folder"].grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.remove_webview2_folder_tooltip = CTkToolTip(
            self.repair_edgeupdate_checkboxes["remove_webview2_folder"],
            message=self.translator.translate("delete_microsoft_edge_webview2_folder_tip"),
            corner_radius=8
        )

        # Execute Button for Repair
        self.repair_edgeupdate_button = customtkinter.CTkButton(
            self.repair_edgeupdate_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_repair_edgeupdate_button_click
        )
        self.repair_edgeupdate_button.grid(row=current_row_in_repair_edgeupdate_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_repair_edgeupdate_frame += 1

        # Set Initial State of the Button
        self._update_repair_edgeupdate_button_state()

        # !Restart Service Frame
        self.restart_service_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.restart_service_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.restart_service_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_restart_service_frame = 0
        self.restart_service_title_label = customtkinter.CTkLabel(
            self.restart_service_frame,
            text=self.translator.translate("restart_service"),
            font=(self.font_family, 16, "bold")
        )
        self.restart_service_title_label.grid(row=current_row_in_restart_service_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.restart_service_title_label.bind("<Configure>", lambda event: self.restart_service_title_label.configure(
            wraplength=self.restart_service_frame.winfo_width() - 20))
        current_row_in_restart_service_frame += 1

        self.restart_service_description_label = customtkinter.CTkLabel(
            self.restart_service_frame,
            text=self.translator.translate("restart_service_description"),
            font=(self.font_family, 12)
        )
        self.restart_service_description_label.grid(row=current_row_in_restart_service_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.restart_service_description_label.bind("<Configure>", lambda event: self.restart_service_description_label.configure(
            wraplength=self.restart_service_frame.winfo_width() - 20))
        current_row_in_restart_service_frame += 1

        # Execute Button for Restart Service
        self.restart_service_button = customtkinter.CTkButton(
            self.restart_service_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_restart_service_button_click
        )
        self.restart_service_button.grid(row=current_row_in_restart_service_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_restart_service_frame += 1

        # !Switch Regions Frame
        self.switch_regions_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.switch_regions_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 5), sticky="ew")
        self.switch_regions_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_switch_regions_frame = 0
        self.switch_regions_title_label = customtkinter.CTkLabel(
            self.switch_regions_frame,
            text=self.translator.translate("switch_regions"),
            font=(self.font_family, 16, "bold")
        )
        self.switch_regions_title_label.grid(row=current_row_in_switch_regions_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.switch_regions_title_label.bind("<Configure>", lambda event: self.switch_regions_title_label.configure(
            wraplength=self.switch_regions_frame.winfo_width() - 20))
        current_row_in_switch_regions_frame += 1

        self.switch_regions_description_label = customtkinter.CTkLabel(
            self.switch_regions_frame,
            text=self.translator.translate("switch_regions_description"),
            font=(self.font_family, 12)
        )
        self.switch_regions_description_label.grid(row=current_row_in_switch_regions_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.switch_regions_description_label.bind("<Configure>", lambda event: self.switch_regions_description_label.configure(
            wraplength=self.switch_regions_frame.winfo_width() - 20))
        current_row_in_switch_regions_frame += 1

        # Checkbox for Old Version
        self.switch_regions_old_version_checkbox = customtkinter.CTkCheckBox(
            self.switch_regions_frame,
            text=self.translator.translate("microsoft_pc_manager_version_less_than_3_14_0_0"),
            font=(self.font_family, 12),
            command=self._on_switch_regions_old_version_toggle
        )
        self.switch_regions_old_version_checkbox.grid(row=current_row_in_switch_regions_frame, column=0, padx=10, pady=5, sticky="w")
        self.switch_regions_old_version_tooltip = CTkToolTip(
            self.switch_regions_old_version_checkbox,
            message=self.translator.translate("modify_registry_to_switch_regions"),
            corner_radius=8
        )
        current_row_in_switch_regions_frame += 1

        # Entry for Region Code (Initially Hidden)
        self.region_code_entry = customtkinter.CTkEntry(
            self.switch_regions_frame,
            placeholder_text=self.translator.translate("please_enter_the_region_code_to_continue")
        )
        self.region_code_entry.bind("<KeyRelease>", lambda event: self._update_switch_regions_button_state())
        # This Widget is Managed By the Checkbox Command, So It's Not Gridded Here Initially

        # Execute Button for Switch Regions
        self.switch_regions_button = customtkinter.CTkButton(
            self.switch_regions_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_switch_regions_button_click
        )
        self.switch_regions_button.grid(row=current_row_in_switch_regions_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_switch_regions_frame += 1

        # Set Initial State of the Button
        self._update_switch_regions_button_state()

        # !View Installed Antivirus Products Frame
        self.view_antivirus_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.view_antivirus_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10), sticky="ew")
        self.view_antivirus_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_view_antivirus_frame = 0
        self.view_antivirus_title_label = customtkinter.CTkLabel(
            self.view_antivirus_frame,
            text=self.translator.translate("view_installed_antivirus_products"),
            font=(self.font_family, 16, "bold")
        )
        self.view_antivirus_title_label.grid(row=current_row_in_view_antivirus_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.view_antivirus_title_label.bind("<Configure>", lambda event: self.view_antivirus_title_label.configure(
            wraplength=self.view_antivirus_frame.winfo_width() - 20))
        current_row_in_view_antivirus_frame += 1

        self.view_antivirus_description_label = customtkinter.CTkLabel(
            self.view_antivirus_frame,
            text=self.translator.translate("view_installed_antivirus_products_description"),
            font=(self.font_family, 12)
        )
        self.view_antivirus_description_label.grid(row=current_row_in_view_antivirus_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.view_antivirus_description_label.bind("<Configure>", lambda event: self.view_antivirus_description_label.configure(
            wraplength=self.view_antivirus_frame.winfo_width() - 20))
        current_row_in_view_antivirus_frame += 1

        # Execute Button for View Installed Antivirus Products
        self.view_antivirus_button = customtkinter.CTkButton(
            self.view_antivirus_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_view_antivirus_button_click
        )
        self.view_antivirus_button.grid(row=current_row_in_view_antivirus_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_view_antivirus_frame += 1

        # Configure Event Output Tab
        event_output_tab = self.tab_view.tab(event_output_tab_name)
        event_output_tab.grid_columnconfigure(0, weight=1)
        event_output_tab.grid_rowconfigure(0, weight=1)

        self.event_output_textbox = customtkinter.CTkTextbox(
            event_output_tab,
            font=(self.font_family, 12),
            wrap="word"
        )
        self.event_output_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.event_output_textbox.configure(state=customtkinter.DISABLED)

        # Create a Context Menu for the Event Output Textbox
        self.context_menu = tkinter.Menu(self, tearoff=0)
        self.context_menu.add_command(label=self.translator.translate("copy"), command=self._copy_text_from_textbox)

        # Bind Right-click to Show Context Menu
        self.event_output_textbox.bind("<Button-3>", self._show_context_menu)

        """----- Page Configurations END -----"""

    """----- Event Configurations -----"""

    def _show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _copy_text_from_textbox(self):
        try:
            # Try to Get Selected Text
            selected_text = self.event_output_textbox.get("sel.first", "sel.last")
            if selected_text:
                self.clipboard_clear()
                self.clipboard_append(selected_text)
        except tkinter.TclError:
            # If No Text is Selected, Copy All Text
            all_text = self.event_output_textbox.get("1.0", "end-1c")  # -1c to exclude trailing newline
            if all_text:
                self.clipboard_clear()
                self.clipboard_append(all_text)

    def _update_compute_hash_button_state(self):
        # Checks If Any Hash Algorithm Checkbox is Selected and Updates the Button State
        is_any_selected = any(checkbox.get() == 1 for checkbox in self.hash_checkboxes.values())
        if is_any_selected:
            self.compute_hash_button.configure(state=customtkinter.NORMAL)
        else:
            self.compute_hash_button.configure(state=customtkinter.DISABLED)

    def _update_get_webview2_version_button_state(self):
        # Checks If Any WebView2 Version Checkbox is Selected and Updates the Button State
        is_any_selected = any(checkbox.get() == 1 for checkbox in self.webview2_checkboxes.values())
        if is_any_selected:
            self.get_webview2_version_button.configure(state=customtkinter.NORMAL)
        else:
            self.get_webview2_version_button.configure(state=customtkinter.DISABLED)

    def _update_repair_edgeupdate_button_state(self):
        # Checks If Any Repair EdgeUpdate Checkbox Is Selected and Updates the Button State
        is_any_selected = any(checkbox.get() == 1 for checkbox in self.repair_edgeupdate_checkboxes.values())
        if is_any_selected:
            self.repair_edgeupdate_button.configure(state=customtkinter.NORMAL)
        else:
            self.repair_edgeupdate_button.configure(state=customtkinter.DISABLED)

    def _on_remove_edge_parent_folder_toggle(self):
        # Handles the Logic When the 'remove_edge_parent_folder' Checkbox is Toggled
        remove_parent_folder_checkbox = self.repair_edgeupdate_checkboxes["remove_edge_parent_folder"]
        remove_webview2_folder_checkbox = self.repair_edgeupdate_checkboxes["remove_webview2_folder"]

        if remove_parent_folder_checkbox.get() == 1:
            # If Parent Folder Removal is Checked, Disable and Uncheck WebView2 Folder Removal
            remove_webview2_folder_checkbox.deselect()
            remove_webview2_folder_checkbox.configure(state=customtkinter.DISABLED)
        else:
            # If Parent Folder Removal is Unchecked, Enable WebView2 Folder Removal
            remove_webview2_folder_checkbox.configure(state=customtkinter.NORMAL)

        # Update the Main Button State After Any Change
        self._update_repair_edgeupdate_button_state()

    def _update_switch_regions_button_state(self, event=None):
        # If the Old Version Checkbox is Checked, the Button State Depends On the Entry Field
        if self.switch_regions_old_version_checkbox.get() == 1:
            if self.region_code_entry.get().strip() == "":
                self.switch_regions_button.configure(state=customtkinter.DISABLED)
            else:
                self.switch_regions_button.configure(state=customtkinter.NORMAL)
        # If the Old Version Checkbox is Not Checked, the Button Should Always be Enabled.
        else:
            self.switch_regions_button.configure(state=customtkinter.NORMAL)

    def _on_switch_regions_old_version_toggle(self):
        # Show or Hide the Region Code Entry Based On the Checkbox State
        if self.switch_regions_old_version_checkbox.get() == 1:
            # The Entry Should be Placed After the Checkbox
            checkbox_row = self.switch_regions_old_version_checkbox.grid_info()["row"]
            self.region_code_entry.grid(row=checkbox_row + 1, column=0, padx=10, pady=(0, 5), sticky="ew")
            # Move the Button Down
            self.switch_regions_button.grid(row=checkbox_row + 2, column=0, padx=10, pady=(5, 10), sticky="ew")
        else:
            # Hide the Entry And Move the Button Back Up
            self.region_code_entry.grid_forget()
            checkbox_row = self.switch_regions_old_version_checkbox.grid_info()["row"]
            self.switch_regions_button.grid(row=checkbox_row + 1, column=0, padx=10, pady=(5, 10), sticky="ew")
        # Update Button State Whenever the Toggle Changes
        self._update_switch_regions_button_state()

    def on_compute_hash_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.compute_hash_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Hash Computation in a Separate Thread
        thread = threading.Thread(target=self.run_hash_computation_thread)
        thread.daemon = True
        thread.start()

    def on_get_webview2_version_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.get_webview2_version_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Get Version in a Separate Thread
        thread = threading.Thread(target=self.run_get_version_thread)
        thread.daemon = True
        thread.start()

    def on_open_dev_settings_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.open_dev_settings_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Open Settings in a Separate Thread
        thread = threading.Thread(target=self.run_open_dev_settings_thread)
        thread.daemon = True
        thread.start()

    def on_open_prod_doc_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.open_prod_doc_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Open Documentation in a Separate Thread
        thread = threading.Thread(target=self.run_open_prod_doc_thread)
        thread.daemon = True
        thread.start()

    def on_repair_edgeupdate_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.repair_edgeupdate_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Repair in a Separate Thread
        thread = threading.Thread(target=self.run_repair_edgeupdate_thread)
        thread.daemon = True
        thread.start()

    def on_restart_service_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.restart_service_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Restart Service in a Separate Thread
        thread = threading.Thread(target=self.run_restart_service_thread)
        thread.daemon = True
        thread.start()

    def on_switch_regions_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.switch_regions_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Switch Regions in a Separate Thread
        thread = threading.Thread(target=self.run_switch_regions_thread)
        thread.daemon = True
        thread.start()

    def on_view_antivirus_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.view_antivirus_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the View Antivirus in a Separate Thread
        thread = threading.Thread(target=self.run_view_antivirus_thread)
        thread.daemon = True
        thread.start()

    def run_hash_computation_thread(self):
        # Get Selected Algorithms From Checkboxes
        selected_algorithms = {
            key: checkbox.get() == 1 for key, checkbox in self.hash_checkboxes.items()
        }

        # Call the Utility Function
        result = self.compute_hash_util.compute_files_hash(selected_algorithms)
        
        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "compute_hash")

    def run_get_version_thread(self):
        # Get Selected Versions From Checkboxes
        selected_versions = {
            key: checkbox.get() == 1 for key, checkbox in self.webview2_checkboxes.items()
        }

        # Call the Utility Function
        result = self.get_webview2_version_util.get_microsoft_edge_webview2_runtime_version(selected_versions)
        
        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "get_version")

    def run_open_dev_settings_thread(self):
        # Call the Utility Function
        result = self.open_dev_settings_util.open_developer_settings()
        
        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "open_dev_settings")

    def run_open_prod_doc_thread(self):
        # Call the Utility Function
        result = self.open_prod_doc_util.open_product_documentation()
        
        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "open_prod_doc")

    def run_repair_edgeupdate_thread(self):
        # Get Selected Repair Options From Checkboxes
        selected_options = {
            key: checkbox.get() == 1 for key, checkbox in self.repair_edgeupdate_checkboxes.items()
        }

        # Call the Utility Function
        result = self.repair_edgeupdate_util.repair_microsoftedgeupdate_not_working(selected_options)
        
        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "repair_edgeupdate")

    def run_restart_service_thread(self):
        # Call the Utility Function
        result = self.restart_service_util.restart_service()

        # Update the GUI from the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "restart_service")

    def run_switch_regions_thread(self):
        is_old_version = self.switch_regions_old_version_checkbox.get() == 1
        region_code = self.region_code_entry.get() if is_old_version else None
        result = self.switch_regions_util.execute_switch(is_old_version, region_code)
        # Schedule the UI Update On the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "switch_regions")

    def run_view_antivirus_thread(self):
        if ProgramSettings.is_compatibility_mode_enabled():
            result = self.view_antivirus_util.view_in_compatibility_mode()
        else:
            result = self.view_antivirus_util.view_in_normal_mode()
        # Schedule the UI Update On the Main Thread
        self.after(0, self.update_output_and_reenable_button, result, "view_antivirus")

    def update_output_and_reenable_button(self, result, source_button_id):
        # Update the Event Output Textbox
        self.event_output_textbox.configure(state=customtkinter.NORMAL)
        self.event_output_textbox.delete("1.0", "end")
        self.event_output_textbox.insert("end", result)
        self.event_output_textbox.configure(state=customtkinter.DISABLED)

        # Re-enable the Correct Button
        if source_button_id == "compute_hash":
            self.compute_hash_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
            self._update_compute_hash_button_state()
        elif source_button_id == "get_version":
            self.get_webview2_version_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
            self._update_get_webview2_version_button_state()
        elif source_button_id == "open_dev_settings":
            self.open_dev_settings_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
        elif source_button_id == "open_prod_doc":
            self.open_prod_doc_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
        elif source_button_id == "repair_edgeupdate":
            self.repair_edgeupdate_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
            self._update_repair_edgeupdate_button_state()
        elif source_button_id == "restart_service":
            self.restart_service_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
        elif source_button_id == "switch_regions":
            self.switch_regions_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
            self._update_switch_regions_button_state()
        elif source_button_id == "view_antivirus":
            self.view_antivirus_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))

        # Switch to the Event Output Tab to Show the Result
        self.tab_view.set(self.translator.translate("event_output_tab"))

        # Scroll the Main Frame to the Top
        self._parent_canvas.yview_moveto(0)

        """----- Event Configurations END -----"""
