import customtkinter

from core import AppLogger
from gui.components import (
    EventsTextbox,
    OperationRunner
)


class BaseInfoPageFrame(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family, page_title_key):
        super().__init__(parent, fg_color="transparent")
        self.logger = AppLogger.get_logger()
        self.log_file_path = AppLogger.get_log_file_path()
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout Configuration (grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate(page_title_key), # Translation key for the page title.
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    """
    USAGE EXAMPLE:

    class SamplePage(BaseInfoPageFrame):
        def __init__(self, parent, app_translator, font_family):
            super().__init__(
                parent=parent,
                app_translator=app_translator,
                font_family=font_family,
                page_title_key="sample_page"    # Translation key for the page title.
            )

            # Add page widgets into self.scroll_frame.
            # Example:
            # customtkinter.CTkLabel(
            #     self.scroll_frame,
            #     text=self.app_translator.translate("sample_text"),
            #     font=customtkinter.CTkFont(family=self.font_family)
            # ).pack(fill="x", padx=20, pady=10)
    """


class BaseFuncPageFrame(BaseInfoPageFrame):
    def __init__(self, parent, app_translator, font_family, page_title_key, events_textbox_wrap="none"):
        super().__init__(parent, app_translator, font_family, page_title_key)

        # Reuse the layout of BaseInfoPageFrame, but destroy its scroll_frame so that a suitable layout can be recreated in BaseFuncPageFrame.
        self.scroll_frame.destroy()
        self.scroll_frame = None

        # Shared Tab Switching Area
        self.tabview = customtkinter.CTkTabview(self, fg_color="transparent")
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.tabview.grid_columnconfigure(0, weight=1)
        self.tabview._segmented_button.configure(
            font=customtkinter.CTkFont(family=self.font_family, size=14, weight="bold")
        )

        self.features_tab_name = self.app_translator.translate("pages.common.features_tab")
        self.events_tab_name = self.app_translator.translate("pages.common.events_tab")

        self.tabview.add(self.features_tab_name)
        self.tabview.add(self.events_tab_name)
        self.tabview.set(self.features_tab_name)

        # Scrollable Content (Features Tab)
        self.scroll_frame = customtkinter.CTkScrollableFrame(
            self.tabview.tab(self.features_tab_name),
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Events Textbox (Events Tab)
        self.events_textbox = EventsTextbox(
            self.tabview.tab(self.events_tab_name),
            self.app_translator,
            self.font_family,
            wrap=events_textbox_wrap
        )

    # ~~~ UI/Events Functions ~~~
    def _run_operation(self, operation_func, operation_name_key, on_completion=None):
        OperationRunner.run(self, operation_func, operation_name_key, on_completion)

    """
    USAGE EXAMPLE:

    class SamplePage(BaseFuncPageFrame):
        def __init__(self, parent, app_translator, font_family):
            super().__init__(
                parent=parent,
                app_translator=app_translator,
                font_family=font_family,
                page_title_key="sample_page",   # Translation key for the page title.
                events_textbox_wrap="none"
            )

            # Add feature widgets into self.scroll_frame (Features tab).
            # Example:
            # customtkinter.CTkButton(
            #     self.scroll_frame,
            #     text=self.app_translator.translate("pages.common.execute"),
            #     command=self._run_sample_operation
            # ).pack(padx=20, pady=10)

        def _run_sample_operation(self):
            self._run_operation(
                operation_func=lambda: self.events_textbox.log_to_events("Sample operation finished."),
                operation_name_key="sample_operation"
            )
    """
