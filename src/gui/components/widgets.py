import customtkinter


class BaseWidgets:
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

    def _create_actions_card(self, parent, title, description, widget_constructor=None, **widget_kwargs):
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


class AboutPageWidgets(BaseWidgets):
    def _create_info_card(self, parent, title, description, widget_constructor=None, description_command=None,
                              **widget_kwargs):
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
                text_color=("#1f6aa5", "#3a7ebf") if description_command else ("gray50", "gray70"),
                anchor="w",
                cursor="hand2" if description_command else "arrow"
            )
            desc_label.pack(fill="x")

            if description_command:
                desc_label.bind("<Button-1>", lambda event: description_command())

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None


class HomePageWidgets(BaseWidgets):
    def _create_section_label_with_button(self, text, button_text, command):
        container = customtkinter.CTkFrame(self.scroll_frame, fg_color="transparent")
        container.pack(fill="x", padx=25, pady=(20, 10))

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(side="left")

        button = customtkinter.CTkButton(
            container,
            text=button_text,
            font=customtkinter.CTkFont(family=self.font_family, size=12),
            command=command
        )
        button.pack(side="right")
        return button

    def _create_info_textbox_card(self, parent, title, description, widget_constructor=None,
                                  enable_text_selection=False, activate_scrollbars=False, min_height=50,
                                  max_height=130, **widget_kwargs):
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
            # Auto-adjust height based on newlines (approx 22px per line + padding).
            line_count = description.count("\n") + 1
            content_height = line_count * 22 + 10
            textbox_height = min(max(min_height, content_height), max_height)
            show_scrollbars = activate_scrollbars and content_height > max_height

            desc_textbox = customtkinter.CTkTextbox(
                text_frame,
                font=customtkinter.CTkFont(family=self.font_family, size=12),
                text_color="gray50",    # CTkTextbox does not support dual-mode text_color ("gray50", "gray70").
                fg_color="transparent",
                wrap="word",
                height=textbox_height,
                activate_scrollbars=show_scrollbars,
                border_width=0
            )
            desc_textbox.pack(fill="x", pady=(0, 5))
            desc_textbox.insert("1.0", description)
            desc_textbox.configure(state="disabled")
            # Disable Text Selection
            if not enable_text_selection:
                desc_textbox.bind("<Button-1>", lambda e: "break")  # Disable Single Click
                desc_textbox.bind("<B1-Motion>", lambda e: "break")  # Disable Click & Drag
                desc_textbox.bind("<Double-Button-1>", lambda e: "break")  # Disable Double Click
                desc_textbox.bind("<Triple-Button-1>", lambda e: "break")  # Disable Triple Click
                # Keep Arrow Instead of Cursor
                desc_textbox.bind("<Enter>", lambda e: desc_textbox.configure(cursor="arrow"))
                desc_textbox.bind("<Leave>", lambda e: desc_textbox.configure(cursor="arrow"))

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None


class SettingsPageWidgets(BaseWidgets):
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

            # For OptionMenu, also set the dropdown font.
            if widget_constructor == customtkinter.CTkOptionMenu and "dropdown_font" not in widget_kwargs:
                widget_kwargs["dropdown_font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
