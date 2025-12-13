from tkinter import ttk

class ExpanderFrame(ttk.Frame):
    def __init__(self, parent, title, font=None, expanded=False, width=20, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.expanded = expanded
        self.title = title
        self.font = font
        self.width = width

        self._create_widgets()
        self._update_content_visibility()

    def _create_widgets(self):
        """
        USEAGE:

        <expander> = ExpanderFrame(
            <content_frame>,                               # Parent Container
            title="<title>",                               # Title Text
            font=(self.font_family, <size>, "<weight>"),   # Button Font
            expanded=False,                                # Initially Expanded
            width=<width>                                  # Button Width
        )
        <expander>.pack(fill="x", pady=10)                 # Pack Expander Frame

        <sample_label> = ttk.Label(
            <expander>.<content_frame>,                    # Parent Container
            text="<content_text>",                         # Content Text
            font=(self.font_family, ...)                   # Content Font
        )
        <expander>.add_widget(<sample_label>)
        """

        # Outer Main Frame, Unified Left and Right Spacing
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="x", padx=12, pady=0)

        # Title Button, With State Indicator
        self.toggle_btn = ttk.Button(
            self.main_frame,
            text=self._get_title_text(),
            style="Expander.TButton",
            command=self.toggle,
            width=self.width
        )
        self.toggle_btn.pack(fill="x", pady=(10, 2))

        # Content Area with Border
        self.content_frame = ttk.Frame(
            self.main_frame,
            borderwidth=1,
            relief="solid",
            padding=(12, 8)
        )
        self.content_frame.pack(fill="both", expand=True, pady=(0, 10))
        self.content_frame.bind("<Configure>", self._on_content_resize) # Handle Resize

        # Set sv-ttk Theme Style
        style = ttk.Style(self)
        style.configure(
            "Expander.TButton",
            font=self.font,
            padding=(12, 8),
            anchor="w"
        )

    def _get_title_text(self):
        collapsed_icon = "▸"
        expanded_icon = "▾"
        return (expanded_icon if self.expanded else collapsed_icon) + " " + self.title

    def toggle(self):
        self.expanded = not self.expanded
        self.toggle_btn.config(text=self._get_title_text())
        self._update_content_visibility()

    def _update_content_visibility(self):
        if self.expanded:
            self.content_frame.pack(fill="both", expand=True)
        else:
            self.content_frame.pack_forget()

    def _on_content_resize(self, event):
        wrap_width = max(event.width - 24, 50)  # Subtract the left and right padding, minimum 50.
        for child in self.content_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(wraplength=wrap_width, anchor="w", justify="left")

    def add_widget(self, widget):
        widget.pack(in_=self.content_frame, fill="x", pady=4)
