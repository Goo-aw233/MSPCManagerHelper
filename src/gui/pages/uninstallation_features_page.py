import customtkinter
import threading
import tkinter

from core.uninstallation.uninstall_microsoft_pc_manager_beta import UninstallMicrosoftPCManagerBeta


class UninstallationFeaturesPageFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font_family=None, translator=None, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, *args, **kwargs)
        self.font_family = font_family
        self.translator = translator
        self.uninstall_beta_util = UninstallMicrosoftPCManagerBeta(translator=self.translator)

        # 配置网格权重
        self.grid_columnconfigure(0, weight=1)
        # 初始化主框架的行计数器
        current_row = 0

        """----- Page Configurations -----"""

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.translator.translate("uninstallation_features_page"),
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

        # Uninstall Microsoft PC Manager Beta Frame
        self.uninstall_beta_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.uninstall_beta_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(10, 5), sticky="ew")
        self.uninstall_beta_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_uninstall_beta_frame = 0
        self.uninstall_beta_title_label = customtkinter.CTkLabel(
            self.uninstall_beta_frame,
            text=self.translator.translate("uninstall_microsoft_pc_manager_beta"),
            font=(self.font_family, 16, "bold")
        )
        self.uninstall_beta_title_label.grid(row=current_row_in_uninstall_beta_frame, column=0, padx=10, pady=(10, 5),
                                             sticky="w")
        self.uninstall_beta_title_label.bind("<Configure>",
                                             lambda event: self.uninstall_beta_title_label.configure(
                                                 wraplength=self.uninstall_beta_frame.winfo_width() - 20))
        current_row_in_uninstall_beta_frame += 1

        self.uninstall_beta_description_label = customtkinter.CTkLabel(
            self.uninstall_beta_frame,
            text=self.translator.translate("uninstall_microsoft_pc_manager_beta_description"),
            font=(self.font_family, 12)
        )
        self.uninstall_beta_description_label.grid(row=current_row_in_uninstall_beta_frame, column=0, padx=10,
                                                   pady=(0, 10),
                                                   sticky="ew")
        self.uninstall_beta_description_label.bind("<Configure>",
                                                   lambda event: self.uninstall_beta_description_label.configure(
                                                       wraplength=self.uninstall_beta_frame.winfo_width() - 20))
        current_row_in_uninstall_beta_frame += 1
        
        # Checkbox for Cleanup
        self.cleanup_checkbox = customtkinter.CTkCheckBox(
            self.uninstall_beta_frame,
            text=self.translator.translate("cleanup_after_uninstallation"),
            font=(self.font_family, 12)
        )
        self.cleanup_checkbox.grid(row=current_row_in_uninstall_beta_frame, column=0, padx=10, pady=(0, 5), sticky="w")
        current_row_in_uninstall_beta_frame += 1

        # Execute Button
        self.uninstall_beta_button = customtkinter.CTkButton(
            self.uninstall_beta_frame,
            text=self.translator.translate("execute"),
            font=(self.font_family, 14, "bold"),
            command=self.on_uninstall_beta_button_click
        )
        self.uninstall_beta_button.grid(row=current_row_in_uninstall_beta_frame, column=0, padx=10, pady=(5, 10), sticky="ew")
        current_row_in_uninstall_beta_frame += 1

        # Uninstall via DISM for All Users Frame
        self.uninstall_dism_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.uninstall_dism_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                       sticky="ew")
        self.uninstall_dism_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_uninstall_dism_frame = 0
        self.uninstall_dism_title_label = customtkinter.CTkLabel(
            self.uninstall_dism_frame,
            text=self.translator.translate("uninstall_via_dism_for_all_users"),
            font=(self.font_family, 16, "bold")
        )
        self.uninstall_dism_title_label.grid(row=current_row_in_uninstall_dism_frame, column=0, padx=10, pady=(10, 5),
                                             sticky="w")
        self.uninstall_dism_title_label.bind("<Configure>",
                                             lambda event: self.uninstall_dism_title_label.configure(
                                                 wraplength=self.uninstall_dism_frame.winfo_width() - 20))
        current_row_in_uninstall_dism_frame += 1

        self.uninstall_dism_description_label = customtkinter.CTkLabel(
            self.uninstall_dism_frame,
            text=self.translator.translate("uninstall_via_dism_for_all_users_description"),
            font=(self.font_family, 12)
        )
        self.uninstall_dism_description_label.grid(row=current_row_in_uninstall_dism_frame, column=0, padx=10,
                                                   pady=(0, 10),
                                                   sticky="ew")
        self.uninstall_dism_description_label.bind("<Configure>",
                                                   lambda event: self.uninstall_dism_description_label.configure(
                                                       wraplength=self.uninstall_dism_frame.winfo_width() - 20))
        current_row_in_uninstall_dism_frame += 1

        # Uninstall via PowerShell for All Users Frame
        self.uninstall_powershell_all_users_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.uninstall_powershell_all_users_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                               sticky="ew")
        self.uninstall_powershell_all_users_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_powershell_all_users_frame = 0
        self.uninstall_powershell_all_users_title_label = customtkinter.CTkLabel(
            self.uninstall_powershell_all_users_frame,
            text=self.translator.translate("uninstall_via_powershell_for_all_users"),
            font=(self.font_family, 16, "bold")
        )
        self.uninstall_powershell_all_users_title_label.grid(row=current_row_in_powershell_all_users_frame, column=0, padx=10,
                                                     pady=(10, 5),
                                                     sticky="w")
        self.uninstall_powershell_all_users_title_label.bind("<Configure>",
                                                     lambda event: self.uninstall_powershell_all_users_title_label.configure(
                                                         wraplength=self.uninstall_powershell_all_users_frame.winfo_width() - 20))
        current_row_in_powershell_all_users_frame += 1

        self.uninstall_powershell_all_users_description_label = customtkinter.CTkLabel(
            self.uninstall_powershell_all_users_frame,
            text=self.translator.translate("uninstall_via_powershell_for_all_users_description"),
            font=(self.font_family, 12)
        )
        self.uninstall_powershell_all_users_description_label.grid(row=current_row_in_powershell_all_users_frame, column=0,
                                                           padx=10, pady=(0, 10),
                                                           sticky="ew")
        self.uninstall_powershell_all_users_description_label.bind("<Configure>",
                                                           lambda event: self.uninstall_powershell_all_users_description_label.configure(
                                                               wraplength=self.uninstall_powershell_all_users_frame.winfo_width() - 20))
        current_row_in_powershell_all_users_frame += 1

        # Uninstall via PowerShell for Current User Frame
        self.uninstall_powershell_current_user_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.uninstall_powershell_current_user_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10),
                                                  sticky="ew")
        self.uninstall_powershell_current_user_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_powershell_current_user_frame = 0
        self.uninstall_powershell_current_user_title_label = customtkinter.CTkLabel(
            self.uninstall_powershell_current_user_frame,
            text=self.translator.translate("uninstall_via_powershell_for_current_user"),
            font=(self.font_family, 16, "bold")
        )
        self.uninstall_powershell_current_user_title_label.grid(row=current_row_in_powershell_current_user_frame, column=0,
                                                        padx=10, pady=(10, 5),
                                                        sticky="w")
        self.uninstall_powershell_current_user_title_label.bind("<Configure>",
                                                        lambda event: self.uninstall_powershell_current_user_title_label.configure(
                                                            wraplength=self.uninstall_powershell_current_user_frame.winfo_width() - 20))
        current_row_in_powershell_current_user_frame += 1

        self.uninstall_powershell_current_user_description_label = customtkinter.CTkLabel(
            self.uninstall_powershell_current_user_frame,
            text=self.translator.translate("uninstall_via_powershell_for_current_user_description"),
            font=(self.font_family, 12)
        )
        self.uninstall_powershell_current_user_description_label.grid(row=current_row_in_powershell_current_user_frame, column=0,
                                                              padx=10, pady=(0, 10),
                                                              sticky="ew")
        self.uninstall_powershell_current_user_description_label.bind("<Configure>",
                                                              lambda event: self.uninstall_powershell_current_user_description_label.configure(
                                                                  wraplength=self.uninstall_powershell_current_user_frame.winfo_width() - 20))
        current_row_in_powershell_current_user_frame += 1

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

    def on_uninstall_beta_button_click(self):
        # Disable Button to Prevent Multiple Clicks
        self.uninstall_beta_button.configure(state=customtkinter.DISABLED, text=self.translator.translate("processing"))

        # Run the Uninstallation Beta in a Separate Thread
        thread = threading.Thread(target=self.run_uninstall_beta_thread)
        thread.daemon = True
        thread.start()

    def run_uninstall_beta_thread(self):
        cleanup = self.cleanup_checkbox.get() == 1
        result = self.uninstall_beta_util.uninstall_microsoft_pc_manager_beta(cleanup=cleanup)
        self.after(0, self.update_output_and_reenable_button, result, "uninstall_beta")

    def update_output_and_reenable_button(self, result, source_button_id):
        # Update the Event Output Textbox
        self.event_output_textbox.configure(state=customtkinter.NORMAL)
        self.event_output_textbox.delete("1.0", "end")
        self.event_output_textbox.insert("end", result)
        self.event_output_textbox.configure(state=customtkinter.DISABLED)

        # Re-enable the Correct Button
        if source_button_id == "uninstall_beta":
            self.uninstall_beta_button.configure(state=customtkinter.NORMAL, text=self.translator.translate("execute"))
        elif source_button_id == "uninstall_for_all_users_via_dism":
            pass
        elif source_button_id == "uninstall_for_all_users":
            pass
        elif source_button_id == "uninstall_for_current_user":
            pass

        # Switch to the Event Output Tab to Show the Result
        self.tab_view.set(self.translator.translate("event_output_tab"))

        # Scroll the Main Frame to the Top
        self._parent_canvas.yview_moveto(0)

        """----- Event Configurations END -----"""
