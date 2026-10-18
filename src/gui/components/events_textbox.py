import customtkinter

from .widgets.content_menu import ContentMenu


class EventsTextbox:
    def __init__(self, parent, app_translator, font_family, wrap="none"):
        self.app_translator = app_translator
        self.font_family = font_family
        self.parent = parent

        self.description_label = customtkinter.CTkLabel(
            parent,
            text=self.app_translator.translate("pages.common.events_textbox_description"),
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

        self.content_menu = ContentMenu(
            parent=self.textbox,
            textbox=self.textbox,
            app_translator=self.app_translator,
            font_family=self.font_family,
            actions=[
                ContentMenu.CLEAR,
                ContentMenu.COPY,
                None,
                ContentMenu.SELECT_ALL
            ],
        )
        self.content_menu.bind_to()

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

    def clear_events(self):
        self.content_menu.clear_content()

    def log_to_events(self, message):
        self.parent.after(0, self._append_to_events_textbox, message)

    def _append_to_events_textbox(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
