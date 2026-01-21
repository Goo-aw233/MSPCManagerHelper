import tkinter

import customtkinter


class InstallerPage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout configuration (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("installer_page"),
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
            state="disabled"
        )
        self.events_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Right-Click Menu for Events Textbox
        self.right_click_menu = tkinter.Menu(self.events_textbox, tearoff=0)
        self.right_click_menu.add_command(label=self.app_translator.translate("copy_button"), command=self._copy_events)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=self.app_translator.translate("clear_button"),
                                          command=self._clear_events)

        self.events_textbox.bind("<Button-3>", self._show_right_click_menu)


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
