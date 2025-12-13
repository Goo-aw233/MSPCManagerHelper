from tkinter import ttk

from core.program_logger import ProgramLogger
from gui.widgets.expander import ExpanderFrame
from gui.widgets.scrollable_frame import ScrollableFrame


class UtilitiesPage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Utilities Page initialized.")

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

        # Utilities page title.
        title_label = ttk.Label(content_frame, text=self.translator.translate("utilities_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # --- Row: Compute File Hash Expander ---
        compute_file_hash_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("compute_file_hash"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        compute_file_hash_expander.pack(fill="x", pady=10)

        compute_file_hash_expander_label = ttk.Label(
            compute_file_hash_expander.content_frame,
            text=self.translator.translate("compute_file_hash_description"),
            font=(self.font_family, 10)
        )
        compute_file_hash_expander.add_widget(compute_file_hash_expander_label)

        # --- Row: Get Microsoft PC Manager Dependencies Version Expander ---
        get_mspcm_deps_version_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("get_microsoft_pc_manager_dependencies_version"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        get_mspcm_deps_version_expander.pack(fill="x", pady=10)

        get_mspcm_deps_version_expander_label = ttk.Label(
            get_mspcm_deps_version_expander.content_frame,
            text=self.translator.translate("get_microsoft_pc_manager_dependencies_version_description"),
            font=(self.font_family, 10)
        )
        get_mspcm_deps_version_expander.add_widget(get_mspcm_deps_version_expander_label)

        #  --- Row: Open Developer Settings Expander ---
        open_developer_settings_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("open_developer_settings"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        open_developer_settings_expander.pack(fill="x", pady=10)

        open_developer_settings_expander_label = ttk.Label(
            open_developer_settings_expander.content_frame,
            text=self.translator.translate("open_developer_settings_description"),
            font=(self.font_family, 10)
        )
        open_developer_settings_expander.add_widget(open_developer_settings_expander_label)

        # --- Row: Open Product Documentation Expander ---
        open_product_documentation_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("open_product_documentation"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        open_product_documentation_expander.pack(fill="x", pady=10)

        open_product_documentation_expander_label = ttk.Label(
            open_product_documentation_expander.content_frame,
            text=self.translator.translate("open_product_documentation_description"),
            font=(self.font_family, 10)
        )
        open_product_documentation_expander.add_widget(open_product_documentation_expander_label)

        # --- Row: Repair MicrosoftEdgeUpdate Not Working Expander ---
        repair_edge_update_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("repair_microsoftedgeupdate_not_working"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        repair_edge_update_expander.pack(fill="x", pady=10)

        repair_edge_update_expander_label = ttk.Label(
            repair_edge_update_expander.content_frame,
            text=self.translator.translate("repair_microsoftedgeupdate_not_working_description"),
            font=(self.font_family, 10)
        )
        repair_edge_update_expander.add_widget(repair_edge_update_expander_label)

        # --- Row: Restart services Expander ---
        restart_services_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("restart_services"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        restart_services_expander.pack(fill="x", pady=10)

        restart_services_expander_label = ttk.Label(
            restart_services_expander.content_frame,
            text=self.translator.translate("restart_services_description"),
            font=(self.font_family, 10)
        )
        restart_services_expander.add_widget(restart_services_expander_label)

        # --- Row: Switch regions Expander ---
        switch_regions_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("switch_regions"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        switch_regions_expander.pack(fill="x", pady=10)

        switch_regions_expander_label = ttk.Label(
            switch_regions_expander.content_frame,
            text=self.translator.translate("switch_regions_description"),
            font=(self.font_family, 10)
        )
        switch_regions_expander.add_widget(switch_regions_expander_label)

        # --- Row: View Installed AntiVirus Products Expander ---
        view_installed_av_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("view_installed_antivirus_products"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        view_installed_av_expander.pack(fill="x", pady=10)

        view_installed_av_expander_label = ttk.Label(
            view_installed_av_expander.content_frame,
            text=self.translator.translate("view_installed_antivirus_products_description"),
            font=(self.font_family, 10)
        )
        view_installed_av_expander.add_widget(view_installed_av_expander_label)
