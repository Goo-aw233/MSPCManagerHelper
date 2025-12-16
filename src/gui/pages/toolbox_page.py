from tkinter import ttk

import darkdetect
import sv_ttk

from core.program_logger import ProgramLogger
from gui.widgets.scrollable_frame import ScrollableFrame
from modules.toolbox import *


class ToolboxPage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Toolbox Page initialized.")

    def create_widgets(self):
        """
        Use `#.TButton` instead of using `TButton` directly.
        E.g.: `Nav.TButton`, `Nav.Accent.TButton`, etc.
        """
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=(self.font_family, 10, "bold"))
        style.configure("ToolboxPage.TButton", font=(self.font_family, 10))

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

        # Toolbox Page Title
        title_label = ttk.Label(content_frame, text=self.translator.translate("toolbox_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # ======================= Program Update Frame Section =======================
        program_update_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("program_update"), padding=10)
        program_update_frame.pack(fill="x", padx=10, pady=5)

        # --- Row 1: Update from GitHub Button and Description ---
        update_from_github_row_frame = ttk.Frame(program_update_frame)
        update_from_github_row_frame.pack(anchor="w", fill="x")
        update_from_github_row_frame.grid_columnconfigure(0, weight=1)

        update_from_github_description_label = ttk.Label(
            update_from_github_row_frame,
            text=self.translator.translate("update_from_github_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        update_from_github_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        update_from_github_button = ttk.Button(
            update_from_github_row_frame,
            text=self.translator.translate("update_from_github"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadProgramFromGitHub(self.logger).execute(),
        )
        update_from_github_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _update_from_github_wrap(e):
            btn_w = update_from_github_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            update_from_github_description_label.config(wraplength=wrap)
        update_from_github_row_frame.bind("<Configure>", _update_from_github_wrap)

        # --- Row 2: Update from OneDrive Button and Description ---
        update_from_onedrive_row_frame = ttk.Frame(program_update_frame)
        update_from_onedrive_row_frame.pack(anchor="w", fill="x", pady=(10, 0))
        update_from_onedrive_row_frame.grid_columnconfigure(0, weight=1)

        update_from_onedrive_description_label = ttk.Label(
            update_from_onedrive_row_frame,
            text=self.translator.translate("update_from_onedrive_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        update_from_onedrive_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        update_from_onedrive_button = ttk.Button(
            update_from_onedrive_row_frame,
            text=self.translator.translate("update_from_onedrive"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadProgramFromOneDrive(self.logger).execute()
        )
        update_from_onedrive_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _update_from_onedrive_wrap(e):
            btn_w = update_from_onedrive_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            update_from_onedrive_description_label.config(wraplength=wrap)
        update_from_onedrive_row_frame.bind("<Configure>", _update_from_onedrive_wrap)
        # ======================= End of Program Update Frame Section =======================

        # ======================= Microsoft PC Manager Update Frame Section =======================
        mspcm_update_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("microsoft_pc_manager_update"), padding=10)
        mspcm_update_frame.pack(fill="x", padx=10, pady=5)

        # --- Row 1: Update from Azure Button and Description ---
        update_mspcm_azure_row_frame = ttk.Frame(mspcm_update_frame)
        update_mspcm_azure_row_frame.pack(anchor="w", fill="x")
        update_mspcm_azure_row_frame.grid_columnconfigure(0, weight=1)

        update_mspcm_azure_description_label = ttk.Label(
            update_mspcm_azure_row_frame,
            text=self.translator.translate("update_microsoft_pc_manager_from_azure_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        update_mspcm_azure_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        update_mspcm_azure_button = ttk.Button(
            update_mspcm_azure_row_frame,
            text=self.translator.translate("update_from_azure"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadMicrosoftPCManagerApplicationPackageFromAzureBlob(self.logger).execute()
        )
        update_mspcm_azure_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _update_mspcm_azure_wrap(e):
            btn_w = update_mspcm_azure_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            update_mspcm_azure_description_label.config(wraplength=wrap)
        update_mspcm_azure_row_frame.bind("<Configure>", _update_mspcm_azure_wrap)

        # --- Row 2: Update from OneDrive Button and Description ---
        update_mspcm_onedrive_row_frame = ttk.Frame(mspcm_update_frame)
        update_mspcm_onedrive_row_frame.pack(anchor="w", fill="x", pady=(10, 0))
        update_mspcm_onedrive_row_frame.grid_columnconfigure(0, weight=1)

        update_mspcm_onedrive_description_label = ttk.Label(
            update_mspcm_onedrive_row_frame,
            text=self.translator.translate("update_microsoft_pc_manager_from_onedrive_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        update_mspcm_onedrive_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        update_mspcm_onedrive_button = ttk.Button(
            update_mspcm_onedrive_row_frame,
            text=self.translator.translate("update_from_onedrive"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadMicrosoftPCManagerApplicationPackageFromOneDrive(self.logger).execute()
        )
        update_mspcm_onedrive_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _update_mspcm_onedrive_wrap(e):
            btn_w = update_mspcm_onedrive_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            update_mspcm_onedrive_description_label.config(wraplength=wrap)
        update_mspcm_onedrive_row_frame.bind("<Configure>", _update_mspcm_onedrive_wrap)
        # ======================= End of Microsoft PC Manager Update Frame Section =======================

        # ======================= Runtime Download Frame Section =======================
        runtime_download_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("runtime_download"), padding=10)
        runtime_download_frame.pack(fill="x", padx=10, pady=5)

        # --- Row 1: Download Microsoft Edge WebView2 Runtime ---
        download_webview2_row_frame = ttk.Frame(runtime_download_frame)
        download_webview2_row_frame.pack(anchor="w", fill="x")
        download_webview2_row_frame.grid_columnconfigure(0, weight=1)

        download_webview2_description_label = ttk.Label(
            download_webview2_row_frame,
            text=self.translator.translate("download_webview2_runtime_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        download_webview2_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        download_webview2_button = ttk.Button(
            download_webview2_row_frame,
            text=self.translator.translate("download_webview2_runtime"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadMicrosoftEdgeWebView2Runtime(self.logger).execute()
        )
        download_webview2_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _download_webview2_wrap(e):
            btn_w = download_webview2_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            download_webview2_description_label.config(wraplength=wrap)
        download_webview2_row_frame.bind("<Configure>", _download_webview2_wrap)

        # --- Row 2: Download Windows App Runtime ---
        download_windows_app_runtime_row_frame = ttk.Frame(runtime_download_frame)
        download_windows_app_runtime_row_frame.pack(anchor="w", fill="x", pady=(10, 0))
        download_windows_app_runtime_row_frame.grid_columnconfigure(0, weight=1)

        download_windows_app_runtime_description_label = ttk.Label(
            download_windows_app_runtime_row_frame,
            text=self.translator.translate("download_windows_app_runtime_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        download_windows_app_runtime_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        download_windows_app_runtime_button = ttk.Button(
            download_windows_app_runtime_row_frame,
            text=self.translator.translate("download_windows_app_runtime"),
            style="ToolboxPage.TButton",
            command=lambda: DownloadWindowsAppRuntimeFromMicrosoftLearn(self.logger).execute()
        )
        download_windows_app_runtime_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _download_windows_app_runtime_wrap(e):
            btn_w = download_windows_app_runtime_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            download_windows_app_runtime_description_label.config(wraplength=wrap)
        download_windows_app_runtime_row_frame.bind("<Configure>", _download_windows_app_runtime_wrap)
        # ======================= End of Runtime Download Frame Section =======================
