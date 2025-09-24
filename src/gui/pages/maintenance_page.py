import customtkinter
import tkinter


class MaintenancePageFrame(customtkinter.CTkScrollableFrame):
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
            text=self.translator.translate("maintenance_page"),
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

        # Repair Feature Frame
        self.repair_feature_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.repair_feature_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(10, 5), sticky="ew")
        self.repair_feature_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_repair_frame = 0
        self.repair_feature_title_label = customtkinter.CTkLabel(
            self.repair_feature_frame,
            text=self.translator.translate("repair_microsoft_pc_manager"),
            font=(self.font_family, 16, "bold")
        )
        self.repair_feature_title_label.grid(row=current_row_in_repair_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.repair_feature_title_label.bind("<Configure>", lambda event: self.repair_feature_title_label.configure(
            wraplength=self.repair_feature_frame.winfo_width() - 20))
        current_row_in_repair_frame += 1

        self.repair_feature_description_label = customtkinter.CTkLabel(
            self.repair_feature_frame,
            text=self.translator.translate("repair_microsoft_pc_manager_description"),
            font=(self.font_family, 12)
        )
        self.repair_feature_description_label.grid(row=current_row_in_repair_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.repair_feature_description_label.bind("<Configure>", lambda event: self.repair_feature_description_label.configure(
            wraplength=self.repair_feature_frame.winfo_width() - 20))
        current_row_in_repair_frame += 1

        # Logs Collection Feature Frame
        self.logs_collection_frame = customtkinter.CTkFrame(features_tab, corner_radius=8, border_width=1)
        self.logs_collection_frame.grid(row=current_row_in_features_tab, column=0, padx=0, pady=(5, 10), sticky="ew")
        self.logs_collection_frame.grid_columnconfigure(0, weight=1)
        current_row_in_features_tab += 1

        current_row_in_logs_frame = 0
        self.logs_collection_title_label = customtkinter.CTkLabel(
            self.logs_collection_frame,
            text=self.translator.translate("microsoft_pc_manager_logs_collection"),
            font=(self.font_family, 16, "bold")
        )
        self.logs_collection_title_label.grid(row=current_row_in_logs_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.logs_collection_title_label.bind("<Configure>", lambda event: self.logs_collection_title_label.configure(
            wraplength=self.logs_collection_frame.winfo_width() - 20))
        current_row_in_logs_frame += 1

        self.logs_collection_description_label = customtkinter.CTkLabel(
            self.logs_collection_frame,
            text=self.translator.translate("microsoft_pc_manager_logs_collection_description"),
            font=(self.font_family, 12)
        )
        self.logs_collection_description_label.grid(row=current_row_in_logs_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.logs_collection_description_label.bind("<Configure>", lambda event: self.logs_collection_description_label.configure(
            wraplength=self.logs_collection_frame.winfo_width() - 20))
        current_row_in_logs_frame += 1

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
