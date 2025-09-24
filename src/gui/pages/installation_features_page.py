import customtkinter
import tkinter


class InstallationFeaturesPageFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font_family=None, translator=None, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, *args, **kwargs)
        self.font_family = font_family
        self.translator = translator

        # 配置网格权重
        self.grid_columnconfigure(0, weight=1)
        # 初始化主框架的行计数器
        current_row = 0

        """----- Page Configurations -----"""

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.translator.translate("installation_features_page"),
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

        # Install Microsoft Edge WebView2 Runtime Frame
        self.install_webview2_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_webview2_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(10, 5), sticky="ew")
        self.install_webview2_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_webview2_frame = 0
        self.install_webview2_title_label = customtkinter.CTkLabel(
            self.install_webview2_frame,
            text=self.translator.translate("install_microsoft_edge_webview2_runtime"),
            font=(self.font_family, 16, "bold")
        )
        self.install_webview2_title_label.grid(row=current_row_in_webview2_frame, column=0, padx=10, pady=(10, 5),
                                               sticky="w")
        self.install_webview2_title_label.bind("<Configure>",
                                               lambda event: self.install_webview2_title_label.configure(
                                                   wraplength=self.install_webview2_frame.winfo_width() - 20))
        current_row_in_webview2_frame += 1

        self.install_webview2_description_label = customtkinter.CTkLabel(
            self.install_webview2_frame,
            text=self.translator.translate("install_microsoft_edge_webview2_runtime_description"),
            font=(self.font_family, 12)
        )
        self.install_webview2_description_label.grid(row=current_row_in_webview2_frame, column=0, padx=10,
                                                     pady=(0, 10),
                                                     sticky="ew")
        self.install_webview2_description_label.bind("<Configure>",
                                                     lambda event: self.install_webview2_description_label.configure(
                                                         wraplength=self.install_webview2_frame.winfo_width() - 20))
        current_row_in_webview2_frame += 1

        # Install via AppxManifest Frame
        self.install_via_appxmanifest_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_via_appxmanifest_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                                 sticky="ew")
        self.install_via_appxmanifest_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_appxmanifest_frame = 0
        self.install_via_appxmanifest_title_label = customtkinter.CTkLabel(
            self.install_via_appxmanifest_frame,
            text=self.translator.translate("install_via_appxmanifest"),
            font=(self.font_family, 16, "bold")
        )
        self.install_via_appxmanifest_title_label.grid(row=current_row_in_appxmanifest_frame, column=0, padx=10,
                                                       pady=(10, 5),
                                                       sticky="w")
        self.install_via_appxmanifest_title_label.bind("<Configure>",
                                                       lambda event: self.install_via_appxmanifest_title_label.configure(
                                                           wraplength=self.install_via_appxmanifest_frame.winfo_width() - 20))
        current_row_in_appxmanifest_frame += 1

        self.install_via_appxmanifest_description_label = customtkinter.CTkLabel(
            self.install_via_appxmanifest_frame,
            text=self.translator.translate("install_via_appxmanifest_description"),
            font=(self.font_family, 12)
        )
        self.install_via_appxmanifest_description_label.grid(row=current_row_in_appxmanifest_frame, column=0,
                                                             padx=10, pady=(0, 10),
                                                             sticky="ew")
        self.install_via_appxmanifest_description_label.bind("<Configure>",
                                                             lambda event: self.install_via_appxmanifest_description_label.configure(
                                                                 wraplength=self.install_via_appxmanifest_frame.winfo_width() - 20))
        current_row_in_appxmanifest_frame += 1

        # Install via DISM for All Users Frame
        self.install_via_dism_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_via_dism_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10), sticky="ew")
        self.install_via_dism_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_dism_frame = 0
        self.install_via_dism_title_label = customtkinter.CTkLabel(
            self.install_via_dism_frame,
            text=self.translator.translate("install_via_dism_for_all_users"),
            font=(self.font_family, 16, "bold")
        )
        self.install_via_dism_title_label.grid(row=current_row_in_dism_frame, column=0, padx=10, pady=(10, 5),
                                               sticky="w")
        self.install_via_dism_title_label.bind("<Configure>",
                                               lambda event: self.install_via_dism_title_label.configure(
                                                   wraplength=self.install_via_dism_frame.winfo_width() - 20))
        current_row_in_dism_frame += 1

        self.install_via_dism_description_label = customtkinter.CTkLabel(
            self.install_via_dism_frame,
            text=self.translator.translate("install_via_dism_for_all_users_description"),
            font=(self.font_family, 12)
        )
        self.install_via_dism_description_label.grid(row=current_row_in_dism_frame, column=0, padx=10, pady=(0, 10),
                                                     sticky="ew")
        self.install_via_dism_description_label.bind("<Configure>",
                                                     lambda event: self.install_via_dism_description_label.configure(
                                                         wraplength=self.install_via_dism_frame.winfo_width() - 20))
        current_row_in_dism_frame += 1

        # Install via Microsoft Store Frame
        self.install_via_ms_store_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_via_ms_store_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                             sticky="ew")
        self.install_via_ms_store_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_ms_store_frame = 0
        self.install_via_ms_store_title_label = customtkinter.CTkLabel(
            self.install_via_ms_store_frame,
            text=self.translator.translate("install_via_microsoft_store"),
            font=(self.font_family, 16, "bold")
        )
        self.install_via_ms_store_title_label.grid(row=current_row_in_ms_store_frame, column=0, padx=10,
                                                   pady=(10, 5),
                                                   sticky="w")
        self.install_via_ms_store_title_label.bind("<Configure>",
                                                   lambda event: self.install_via_ms_store_title_label.configure(
                                                       wraplength=self.install_via_ms_store_frame.winfo_width() - 20))
        current_row_in_ms_store_frame += 1

        self.install_via_ms_store_description_label = customtkinter.CTkLabel(
            self.install_via_ms_store_frame,
            text=self.translator.translate("install_via_microsoft_store_description"),
            font=(self.font_family, 12)
        )
        self.install_via_ms_store_description_label.grid(row=current_row_in_ms_store_frame, column=0, padx=10,
                                                         pady=(0, 10),
                                                         sticky="ew")
        self.install_via_ms_store_description_label.bind("<Configure>",
                                                         lambda event: self.install_via_ms_store_description_label.configure(
                                                             wraplength=self.install_via_ms_store_frame.winfo_width() - 20))
        current_row_in_ms_store_frame += 1

        # Install via PowerShell for Current User Frame
        self.install_via_powershell_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_via_powershell_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                               sticky="ew")
        self.install_via_powershell_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_powershell_frame = 0
        self.install_via_powershell_title_label = customtkinter.CTkLabel(
            self.install_via_powershell_frame,
            text=self.translator.translate("install_via_powershell_for_current_user"),
            font=(self.font_family, 16, "bold")
        )
        self.install_via_powershell_title_label.grid(row=current_row_in_powershell_frame, column=0, padx=10,
                                                     pady=(10, 5),
                                                     sticky="w")
        self.install_via_powershell_title_label.bind("<Configure>",
                                                     lambda event: self.install_via_powershell_title_label.configure(
                                                         wraplength=self.install_via_powershell_frame.winfo_width() - 20))
        current_row_in_powershell_frame += 1

        self.install_via_powershell_description_label = customtkinter.CTkLabel(
            self.install_via_powershell_frame,
            text=self.translator.translate("install_via_powershell_for_current_user_description"),
            font=(self.font_family, 12)
        )
        self.install_via_powershell_description_label.grid(row=current_row_in_powershell_frame, column=0, padx=10,
                                                           pady=(0, 10),
                                                           sticky="ew")
        self.install_via_powershell_description_label.bind("<Configure>",
                                                           lambda event: self.install_via_powershell_description_label.configure(
                                                               wraplength=self.install_via_powershell_frame.winfo_width() - 20))
        current_row_in_powershell_frame += 1

        # Install via WinGet Frame
        self.install_via_winget_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.install_via_winget_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                           sticky="ew")
        self.install_via_winget_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_winget_frame = 0
        self.install_via_winget_title_label = customtkinter.CTkLabel(
            self.install_via_winget_frame,
            text=self.translator.translate("install_via_winget"),
            font=(self.font_family, 16, "bold")
        )
        self.install_via_winget_title_label.grid(row=current_row_in_winget_frame, column=0, padx=10, pady=(10, 5),
                                                 sticky="w")
        self.install_via_winget_title_label.bind("<Configure>",
                                                 lambda event: self.install_via_winget_title_label.configure(
                                                     wraplength=self.install_via_winget_frame.winfo_width() - 20))
        current_row_in_winget_frame += 1

        self.install_via_winget_description_label = customtkinter.CTkLabel(
            self.install_via_winget_frame,
            text=self.translator.translate("install_via_winget_description"),
            font=(self.font_family, 12)
        )
        self.install_via_winget_description_label.grid(row=current_row_in_winget_frame, column=0, padx=10,
                                                       pady=(0, 10),
                                                       sticky="ew")
        self.install_via_winget_description_label.bind("<Configure>",
                                                       lambda event: self.install_via_winget_description_label.configure(
                                                           wraplength=self.install_via_winget_frame.winfo_width() - 20))
        current_row_in_winget_frame += 1

        # Reinstall via PowerShell Frame
        self.reinstall_via_powershell_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.reinstall_via_powershell_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                                 sticky="ew")
        self.reinstall_via_powershell_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_reinstall_frame = 0
        self.reinstall_via_powershell_title_label = customtkinter.CTkLabel(
            self.reinstall_via_powershell_frame,
            text=self.translator.translate("reinstall_via_powershell"),
            font=(self.font_family, 16, "bold")
        )
        self.reinstall_via_powershell_title_label.grid(row=current_row_in_reinstall_frame, column=0, padx=10,
                                                       pady=(10, 5),
                                                       sticky="w")
        self.reinstall_via_powershell_title_label.bind("<Configure>",
                                                       lambda event: self.reinstall_via_powershell_title_label.configure(
                                                           wraplength=self.reinstall_via_powershell_frame.winfo_width() - 20))
        current_row_in_reinstall_frame += 1

        self.reinstall_via_powershell_description_label = customtkinter.CTkLabel(
            self.reinstall_via_powershell_frame,
            text=self.translator.translate("reinstall_via_powershell_description"),
            font=(self.font_family, 12)
        )
        self.reinstall_via_powershell_description_label.grid(row=current_row_in_reinstall_frame, column=0, padx=10,
                                                             pady=(0, 10),
                                                             sticky="ew")
        self.reinstall_via_powershell_description_label.bind("<Configure>",
                                                             lambda event: self.reinstall_via_powershell_description_label.configure(
                                                                 wraplength=self.reinstall_via_powershell_frame.winfo_width() - 20))
        current_row_in_reinstall_frame += 1

        # Update via Application Package Frame
        self.update_via_app_package_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.update_via_app_package_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                               sticky="ew")
        self.update_via_app_package_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_update_frame = 0
        self.update_via_app_package_title_label = customtkinter.CTkLabel(
            self.update_via_app_package_frame,
            text=self.translator.translate("update_via_application_package"),
            font=(self.font_family, 16, "bold")
        )
        self.update_via_app_package_title_label.grid(row=current_row_in_update_frame, column=0, padx=10,
                                                     pady=(10, 5),
                                                     sticky="w")
        self.update_via_app_package_title_label.bind("<Configure>",
                                                     lambda event: self.update_via_app_package_title_label.configure(
                                                         wraplength=self.update_via_app_package_frame.winfo_width() - 20))
        current_row_in_update_frame += 1

        self.update_via_app_package_description_label = customtkinter.CTkLabel(
            self.update_via_app_package_frame,
            text=self.translator.translate("update_via_application_package_description"),
            font=(self.font_family, 12)
        )
        self.update_via_app_package_description_label.grid(row=current_row_in_update_frame, column=0, padx=10,
                                                           pady=(0, 10),
                                                           sticky="ew")
        self.update_via_app_package_description_label.bind("<Configure>",
                                                           lambda event: self.update_via_app_package_description_label.configure(
                                                               wraplength=self.update_via_app_package_frame.winfo_width() - 20))
        current_row_in_update_frame += 1

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
