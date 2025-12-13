from tkinter import ttk

from core.program_logger import ProgramLogger
from gui.widgets.expander import ExpanderFrame
from gui.widgets.scrollable_frame import ScrollableFrame


class MaintenancePage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Maintenance Page initialized.")

    def create_widgets(self):
        """
        Use `#.TButton` instead of using `TButton` directly.
        E.g.: `Nav.TButton`, `Nav.Accent.TButton`, etc.
        """
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=(self.font_family, 10, "bold"))

        # Use the theme background so the canvas matches the rest of UI.
        frame_bg = style.lookup("TFrame", "background") or self.cget("background")
        # text_fg = style.lookup("TLabel", "foreground") or "#000000"

        # Page-level Scrollable Frame (Shared Component)
        scrollable = ScrollableFrame(self, bg=frame_bg)
        scrollable.pack(fill="both", expand=True)
        content_frame = scrollable.content_frame

        # Maintenance page title.
        title_label = ttk.Label(content_frame, text=self.translator.translate("maintenance_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # --- Row: Logs Collection Expander ---
        logs_collection_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("logs_collection"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        logs_collection_expander.pack(fill="x", pady=10)

        logs_collection_expander_label = ttk.Label(
            logs_collection_expander.content_frame,
            text=self.translator.translate("logs_collection_description"),
            font=(self.font_family, 10)
        )
        logs_collection_expander.add_widget(logs_collection_expander_label)

        # --- Row: Repair Microsoft PC Manager Expander ---
        repair_mspcm_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("repair_microsoft_pc_manager"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        repair_mspcm_expander.pack(fill="x", pady=10)

        repair_mspcm_expander_label = ttk.Label(
            repair_mspcm_expander.content_frame,
            text=self.translator.translate("repair_microsoft_pc_manager_description"),
            font=(self.font_family, 10)
        )
        repair_mspcm_expander.add_widget(repair_mspcm_expander_label)
