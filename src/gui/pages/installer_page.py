from tkinter import ttk

import darkdetect
import sv_ttk

from core.advanced_startup import AdvancedStartup
from core.program_logger import ProgramLogger
from gui.widgets.expander import ExpanderFrame
from gui.widgets.scrollable_frame import ScrollableFrame


class InstallerPage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Installer Page initialized.")

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

        # Installer page title.
        title_label = ttk.Label(content_frame, text=self.translator.translate("installer_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # --- Row: Install Microsoft Edge WebView2 Runtime Expander ---
        install_webview2_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_microsoft_edge_webview2_runtime"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        install_webview2_expander.pack(fill="x", pady=10)

        install_webview2_expander_label = ttk.Label(
            install_webview2_expander.content_frame,
            text=self.translator.translate("install_microsoft_edge_webview2_runtime_description"),
            font=(self.font_family, 10)
        )
        install_webview2_expander.add_widget(install_webview2_expander_label)

        # --- Row: Install via AppxManifest.xml Expander ---
        if AdvancedStartup.is_devmode() or AdvancedStartup.is_debugmode():
            install_via_appxmanifest_expander = ExpanderFrame(
                content_frame,
                title=self.translator.translate("install_via_appxmanifest"),
                font=(self.font_family, 10, "bold"),
                width=40,
                expanded=False
            )
            install_via_appxmanifest_expander.pack(fill="x", pady=10)

            install_via_appxmanifest_expander_label = ttk.Label(
                install_via_appxmanifest_expander.content_frame,
                text=self.translator.translate("install_via_appxmanifest_description"),
                font=(self.font_family, 10)
            )
            install_via_appxmanifest_expander.add_widget(install_via_appxmanifest_expander_label)

        # --- Row: Install via DISM for All Users Expander ---
        install_via_dism_for_all_users_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_via_dism_for_all_users"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        install_via_dism_for_all_users_expander.pack(fill="x", pady=10)

        install_via_dism_for_all_users_expander_label = ttk.Label(
            install_via_dism_for_all_users_expander.content_frame,
            text=self.translator.translate("install_via_dism_for_all_users_description"),
            font=(self.font_family, 10)
        )
        install_via_dism_for_all_users_expander.add_widget(install_via_dism_for_all_users_expander_label)

        # --- Row: Install via Microsoft Store Expander ---
        install_via_msstore_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_via_microsoft_store"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        install_via_msstore_expander.pack(fill="x", pady=10)

        install_via_msstore_expander_label = ttk.Label(
            install_via_msstore_expander.content_frame,
            text=self.translator.translate("install_via_microsoft_store_description"),
            font=(self.font_family, 10)
        )
        install_via_msstore_expander.add_widget(install_via_msstore_expander_label)

        # --- Row: Install via PowerShell for All Users Expander ---
        install_via_powershell_for_all_users_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_via_powershell_for_all_users"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        install_via_powershell_for_all_users_expander.pack(fill="x", pady=10)

        install_via_powershell_for_all_users_expander_label = ttk.Label(
            install_via_powershell_for_all_users_expander.content_frame,
            text=self.translator.translate("install_via_powershell_for_all_users_description"),
            font=(self.font_family, 10)
        )
        install_via_powershell_for_all_users_expander.add_widget(install_via_powershell_for_all_users_expander_label)

        # --- Row: Install via PowerShell for Current User Expander ---
        install_via_powershell_for_current_user_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_via_powershell_for_current_user"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=True
        )
        install_via_powershell_for_current_user_expander.pack(fill="x", pady=10)

        install_via_powershell_for_current_user_expander_label = ttk.Label(
            install_via_powershell_for_current_user_expander.content_frame,
            text=self.translator.translate("install_via_powershell_for_current_user_description"),
            font=(self.font_family, 10)
        )
        install_via_powershell_for_current_user_expander.add_widget(install_via_powershell_for_current_user_expander_label)

        # --- Row: Install via WinGet Expander ---
        install_via_winget_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("install_via_winget"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        install_via_winget_expander.pack(fill="x", pady=10)

        install_via_winget_expander_label = ttk.Label(
            install_via_winget_expander.content_frame,
            text=self.translator.translate("install_via_winget_description"),
            font=(self.font_family, 10)
        )
        install_via_winget_expander.add_widget(install_via_winget_expander_label)

        # --- Row: Reinstall via PowerShell Expander ---
        reinstall_via_powershell_expander = ExpanderFrame(
            content_frame,
            title=self.translator.translate("reinstall_via_powershell"),
            font=(self.font_family, 10, "bold"),
            width=40,
            expanded=False
        )
        reinstall_via_powershell_expander.pack(fill="x", pady=10)

        reinstall_via_powershell_expander_label = ttk.Label(
            reinstall_via_powershell_expander.content_frame,
            text=self.translator.translate("reinstall_via_powershell_description"),
            font=(self.font_family, 10)
        )
        reinstall_via_powershell_expander.add_widget(reinstall_via_powershell_expander_label)
