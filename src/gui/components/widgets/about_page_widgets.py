import customtkinter

from .base_page_widgets import BaseWidgets


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
                desc_label.bind("<Button-1>", lambda _: description_command())

        # Widget Column
        if widget_constructor:
            # Inject font family if not present and if the widget supports it (most CTk widgets do).
            if "font" not in widget_kwargs:
                widget_kwargs["font"] = customtkinter.CTkFont(family=self.font_family)

            widget = widget_constructor(container, **widget_kwargs)
            widget.pack(side="right", padx=5)
            return widget
        return None
