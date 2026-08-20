import customtkinter

from core import AppLogger
from gui.components import (
    EventsTextbox,
    OperationRunner,
    ScrollableFrame,
    task_coordinator
)


class BaseInfoPageFrame(customtkinter.CTkFrame):
    """USAGE EXAMPLE:

    class SamplePage(BaseInfoPageFrame, SamplePageWidgets):
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

            # Build the page content with the widget mixin helpers
            # (e.g. AboutPageWidgets provides _create_info_card).
            self._create_section_label(self.app_translator.translate("sample_section"))
            group = self._create_group_frame()
            self._create_info_card(
                group,
                title=self.app_translator.translate("sample_title"),
                description=self.app_translator.translate("sample_description")
            )
    """

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
        self.scroll_frame = ScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)


class BaseFuncPageFrame(BaseInfoPageFrame):
    """USAGE EXAMPLE:

    class SamplePage(BaseFuncPageFrame, BaseWidgets):
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

            # Register the action cards protected by the global operation lock.
            self._operation_cards = [
                (self.sample_card, self._refresh_sample_card_state),
            ]
            self._register_operation_cards()

        def _refresh_sample_card_state(self):
            # _set_card_state also keeps the card disabled while another
            # operation is running.
            self._set_card_state(self.sample_card, "normal")

        def _run_sample_operation(self):
            # Runs with the global lock: rejects if busy, disables every
            # registered card, and restores them on completion.
            self._run_operation(
                operation_func=lambda: self.events_textbox.log_to_events("Sample operation finished."),
                operation_name_key="sample_operation"
            )
    """

    def __init__(self, parent, app_translator, font_family, page_title_key, events_textbox_wrap="none",
                 on_mspcm_version_changed=None):
        super().__init__(parent, app_translator, font_family, page_title_key)

        # Refresh Microsoft PC Manager version display on the Home page. (Optional, from MainWindow)
        self.on_mspcm_version_changed = on_mspcm_version_changed

        # Reuse the layout of BaseInfoPageFrame, but destroy its scroll_frame so that a suitable layout can be recreated in BaseFuncPageFrame.
        self.scroll_frame.destroy()
        self.scroll_frame = None

        # Shared Tab Switching Area
        self.tabview = customtkinter.CTkTabview(
            self,
            fg_color="transparent",
            segmented_button_font=customtkinter.CTkFont(family=self.font_family, size=14, weight="bold")
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.tabview.grid_columnconfigure(0, weight=1)

        self.features_tab_name = self.app_translator.translate("pages.common.features_tab")
        self.events_tab_name = self.app_translator.translate("pages.common.events_tab")

        self.tabview.add(self.features_tab_name)
        self.tabview.add(self.events_tab_name)
        self.tabview.set(self.features_tab_name)

        # Scrollable Content (Features Tab)
        self.scroll_frame = ScrollableFrame(
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
        operation_name = self.app_translator.translate(operation_name_key)

        # Global operation lock: reject the operation if another one is running.
        if not task_coordinator.try_acquire(operation_name):
            self.logger.warning(
                f"Operation '{operation_name}' rejected: another operation "
                f"('{task_coordinator.current_operation()}') is already running.")
            self.events_textbox.log_to_events(
                self.app_translator.translate("pages.common.operation_rejected_busy").format(
                    operation_name=task_coordinator.current_operation()))
            return

        # Disable every registered action card while this operation is running.
        task_coordinator.disable_all()
        self.update_idletasks()

        def _on_completion():
            # Release the global lock first, then let every registered card
            # recompute its own state before running the caller's completion
            # callback.
            task_coordinator.release()
            task_coordinator.restore_all()
            if on_completion:
                on_completion()
            self._on_operation_completed()

        OperationRunner.run(self, operation_func, operation_name_key, _on_completion)

    def _register_operation_cards(self):
        # Register every (card, refresh) pair so the global operation lock can
        # disable all cards while one operation runs and restore them after.
        for card, refresh in getattr(self, "_operation_cards", ()):
            task_coordinator.register(self, card, refresh)

    def _on_operation_completed(self):
        """Hook invoked on the main thread after every operation completes.

        Subclasses override this to react to a finished operation.
        """
        pass
