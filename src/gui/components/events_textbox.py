import tkinter

import customtkinter


class EventsTextbox:
    def __init__(self, parent, app_translator, font_family, wrap="none"):
        self.app_translator = app_translator
        self.font_family = font_family
        self.parent = parent

        self.description_label = customtkinter.CTkLabel(
            parent,
            text=self.app_translator.translate("events_textbox_description"),
            font=customtkinter.CTkFont(family=self.font_family, size=13),
            anchor="center"
        )
        self.description_label.pack(fill="x", padx=12, pady=(10, 0))

        self.textbox = customtkinter.CTkTextbox(
            parent,
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            state="disabled",
            wrap=wrap
        )
        self.textbox._textbox.configure(tabs=("5c",))
        self.textbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_click_menu = tkinter.Menu(self.textbox, tearoff=0)
        self.right_click_menu.add_command(label=self.app_translator.translate("copy_button"),
                                          command=self.copy_events)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=self.app_translator.translate("clear_button"),
                                          command=self.clear_events)

        self.textbox.bind("<Button-3>", self.show_right_click_menu)

    """
    USAGE EXAMPLE:

    class MyPage(customtkinter.CTkFrame):
        def __init__(self, parent, app_translator, font_family):
            super().__init__(parent)

            # 1. Create Events Textbox:
            self.events_textbox = EventsTextbox(
                parent=self,
                app_translator=app_translator,
                font_family=font_family,
                wrap="none" # All Events Textboxes use "none" to avoid line breaks.
            )
            # `wrap` is optional, "word" makes it wrap at word boundaries, "char" wraps at character boundaries.

        def func(self):
            # 2. Log Message to Events Textbox:
            self.events_textbox.log_to_events("Processing...")

            # 3. Clear Events Textbox:
            self.events_textbox.clear_events()
    """

    def show_right_click_menu(self, event):
        if hasattr(self.parent, "winfo_toplevel"):
            root = self.parent.winfo_toplevel()
            if hasattr(root, "_apply_appearance_mode"):
                bg = root._apply_appearance_mode(["#e3e3e3", "#333333"])
                fg = root._apply_appearance_mode(["#191919", "#e2e2e2"])
                active_bg = root._apply_appearance_mode(["#bebebe", "#464646"])
                active_fg = root._apply_appearance_mode(["#191919", "#e2e2e2"])
            else:
                bg = "#e3e3e3" if customtkinter.get_appearance_mode() == "Light" else "#333333"
                fg = "#191919" if customtkinter.get_appearance_mode() == "Light" else "#e2e2e2"
                active_bg = "#bebebe" if customtkinter.get_appearance_mode() == "Light" else "#464646"
                active_fg = "#191919" if customtkinter.get_appearance_mode() == "Light" else "#e2e2e2"
        else:
            bg = "#e3e3e3" if customtkinter.get_appearance_mode() == "Light" else "#333333"
            fg = "#191919" if customtkinter.get_appearance_mode() == "Light" else "#e2e2e2"
            active_bg = "#bebebe" if customtkinter.get_appearance_mode() == "Light" else "#464646"
            active_fg = "#191919" if customtkinter.get_appearance_mode() == "Light" else "#e2e2e2"

        self.right_click_menu.configure(
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=active_fg,
            font=(self.font_family, 10)
        )
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def copy_events(self):
        try:
            selected_text = self.textbox.get("sel.first", "sel.last")
            self.parent.clipboard_clear()
            self.parent.clipboard_append(selected_text)
        except tkinter.TclError:
            all_text = self.textbox.get("1.0", "end-1c")
            if all_text:
                self.parent.clipboard_clear()
                self.parent.clipboard_append(all_text)

    def clear_events(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

    def log_to_events(self, message):
        self.parent.after(0, self._append_to_events_textbox, message)

    def _append_to_events_textbox(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def get_textbox(self):
        return self.textbox
