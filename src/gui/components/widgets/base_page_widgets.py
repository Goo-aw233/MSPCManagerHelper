import tkinter

import customtkinter

from gui.components.scrollable_frame import ScrollableFrame
from gui.components.task_coordinator import task_coordinator


class BaseWidgets:
    scroll_frame: ScrollableFrame
    font_family: str

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

            # Fail-safe: default new action widgets to disable. Section-end refresh
            # functions immediately override this with the correct state.
            widget_kwargs.setdefault("state", "disabled")

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None

    @staticmethod
    def _set_card_state(card, state):
        # While an operation is running, no action card may be enabled.
        if task_coordinator.is_busy():
            state = "disabled"
        card.configure(state=state)

    def _set_entry_group_state(self, enabled, entry, button=None):
        if button is not None:
            button.configure(state="normal" if enabled else "disabled")
        entry.unbind("<Button-1>")
        entry.configure(state="normal")
        if not enabled:
            entry.bind("<Button-1>", self._block_entry_event)

    @staticmethod
    def _set_entry_text(entry, text):
        entry.delete(0, tkinter.END)
        entry.insert(0, text)

    @staticmethod
    def _block_entry_event(_):
        return "break"
