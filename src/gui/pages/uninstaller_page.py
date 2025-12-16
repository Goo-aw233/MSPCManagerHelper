from tkinter import ttk

import darkdetect
import sv_ttk

from core.program_logger import ProgramLogger
from gui.widgets.expander import ExpanderFrame
from gui.widgets.scrollable_frame import ScrollableFrame


class UninstallerPage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Uninstaller Page initialized.")

    def create_widgets(self):
        """
        Use `#.TButton` instead of using `TButton` directly.
        E.g.: `Nav.TButton`, `Nav.Accent.TButton`, etc.
        """
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=(self.font_family, 10, "bold"))

        # Use the theme background so the canvas matches the rest of UI.
        theme = sv_ttk.get_theme() if hasattr(sv_ttk, "get_theme") else (darkdetect.theme().lower() if darkdetect.theme() else "light")
        if theme == "dark":
            default_bg = "#1c1c1c"
            # default_fg = "#fafafa"
        else:
            default_bg = "#fafafa"
            # default_fg = "#1c1c1c"
        frame_bg = style.lookup("TFrame", "background") or default_bg
        # text_fg = style.lookup("TLabel", "foreground") or default_fg

        # Page-level Scrollable Frame (Shared Component)
        scrollable = ScrollableFrame(self, bg=frame_bg)
        scrollable.pack(fill="both", expand=True)
        content_frame = scrollable.content_frame

        # Uninstaller page title.
        title_label = ttk.Label(content_frame, text=self.translator.translate("uninstaller_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # --- Row: Uninstall Beta Expander ---
        uninstall_beta_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("uninstall_beta"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        uninstall_beta_expander.pack(fill="x", pady=10)

        uninstall_beta_expander_label = ttk.Label(
            uninstall_beta_expander.content_frame,
            text=self.translator.translate("uninstall_beta_description"),
            font=(self.font_family, 10)
        )
        uninstall_beta_expander.add_widget(uninstall_beta_expander_label)

        # --- Row: Uninstall via DISM for All Users Expander ---
        uninstall_via_dism_all_users_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("uninstall_via_dism_for_all_users"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        uninstall_via_dism_all_users_expander.pack(fill="x", pady=10)

        uninstall_via_dism_all_users_expander_label = ttk.Label(
            uninstall_via_dism_all_users_expander.content_frame,
            text=self.translator.translate("uninstall_via_dism_for_all_users_description"),
            font=(self.font_family, 10)
        )
        uninstall_via_dism_all_users_expander.add_widget(uninstall_via_dism_all_users_expander_label)

        # --- Row: Uninstall via PowerShell for All Users Expander ---
        uninstall_via_powershell_all_users_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("uninstall_via_powershell_for_all_users"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        uninstall_via_powershell_all_users_expander.pack(fill="x", pady=10)

        uninstall_via_powershell_all_users_expander_label = ttk.Label(
            uninstall_via_powershell_all_users_expander.content_frame,
            text=self.translator.translate("uninstall_via_powershell_for_all_users_description"),
            font=(self.font_family, 10)
        )
        uninstall_via_powershell_all_users_expander.add_widget(uninstall_via_powershell_all_users_expander_label)

        # --- Row: Uninstall via PowerShell for Current User Expander ---
        uninstall_via_powershell_current_user_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("uninstall_via_powershell_for_current_user"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        uninstall_via_powershell_current_user_expander.pack(fill="x", pady=10)

        uninstall_via_powershell_current_user_expander_label = ttk.Label(
            uninstall_via_powershell_current_user_expander.content_frame,
            text=self.translator.translate("uninstall_via_powershell_for_current_user_description"),
            font=(self.font_family, 10)
        )
        uninstall_via_powershell_current_user_expander.add_widget(uninstall_via_powershell_current_user_expander_label)
