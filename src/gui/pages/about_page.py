import os
import subprocess
import tkinter
import webbrowser
from tkinter import messagebox, ttk

from core.program_logger import ProgramLogger
from core.program_metadata import ProgramMetadata
from gui.widgets.scrollable_frame import ScrollableFrame


class AboutPage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("About Page initialized.")

    def create_widgets(self):
        """
        Use `#.TButton` instead of using `TButton` directly.
        E.g.: `Nav.TButton`, `Nav.Accent.TButton`, etc.
        """
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=(self.font_family, 10, "bold"))
        style.configure("AboutPage.TButton", font=(self.font_family, 10))

        # Use the theme background so the canvas matches the rest of UI.
        frame_bg = style.lookup("TFrame", "background") or self.cget("background")
        text_fg = style.lookup("TLabel", "foreground") or "#000000"

        # Page-level Scrollable Frame (Shared Component)
        scrollable = ScrollableFrame(self, bg=frame_bg)
        scrollable.pack(fill="both", expand=True)
        content_frame = scrollable.content_frame

        # About Page Title
        title_label = ttk.Label(content_frame, text=self.translator.translate("about_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # ======================= Basic Information Frame Section =======================
        basic_information_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("program_information"))
        basic_information_frame.pack(padx=10, pady=10, fill="x")

        # Program version + download channels displayed inline in same row.
        version_and_download_frame = ttk.Frame(basic_information_frame)
        version_and_download_frame.pack(anchor="w", padx=10, pady=5, fill="x")

        # Version Label
        version_label = ttk.Label(version_and_download_frame,
                                text=f"{self.translator.translate('program_version')}: {ProgramMetadata.PROGRAM_VERSION}",
                                font=(self.font_family, 10))
        version_label.pack(side="left")

        # Two download channel links, displayed inline after version, with hard-coded suffixes.
        download_links = [
            ("https://github.com/Goo-aw233/MSPCManagerHelper/releases", " 1 (GitHub)"),
            ("https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA",
             " 2 (OneDrive)")
        ]

        for url, suffix in download_links:
            display_text = f"{self.translator.translate('program_download_channel')}{suffix}"
            link = ttk.Label(version_and_download_frame,
                            text=display_text,
                            foreground="#0078D7",
                            cursor="hand2",
                            font=(self.font_family, 10, "underline"))
            link.pack(side="left", padx=5)
            # bind with default parameter to avoid closure capture problem in loop.
            link.bind("<Button-1>", lambda e, url_to_open=url: webbrowser.open_new(url_to_open))

        # Project Contributors Frame in basic_information_frame
        contributors_frame = ttk.Frame(basic_information_frame)
        contributors_frame.pack(anchor="w", padx=10, pady=5, fill="x")

        # Project Contributors Label
        ttk.Label(contributors_frame, text=self.translator.translate("project_contributors") + ":",
                  font=(self.font_family, 10)).pack(side="left")

        # Contributors with their links.
        contributors = {
            "ArcticFoxPro": "https://github.com/ArcticFoxPro",
            "GuCATs": "https://github.com/Goo-aw233",
            "LuYang114": "https://github.com/LuYang114",
            "zwJimRaynor": "https://github.com/zwJimRaynor"
        }

        # Create and pack contributor links.
        for contributor, contributor_url in contributors.items():
            link = ttk.Label(contributors_frame, text=contributor, foreground="#0078D7", cursor="hand2",
                            font=(self.font_family, 10, "underline"))
            link.pack(side="left", padx=5)
            link.bind("<Button-1>", lambda e, url_to_open=contributor_url: webbrowser.open_new(url_to_open))

        # Localization Translators in basic_information_frame
        localization_translators = self._get_localization_translators()
        if localization_translators:
            localization_frame = ttk.Frame(basic_information_frame)
            localization_frame.pack(anchor="w", padx=10, pady=5, fill="x")

            ttk.Label(localization_frame, text=self.translator.translate("localization_translator") + ":",
                      font=(self.font_family, 10)).pack(side="left")

            for username, display_name in localization_translators:
                github_profile_url = f"https://github.com/{username}"
                link = ttk.Label(localization_frame, text=display_name, foreground="#0078D7", cursor="hand2",
                                 font=(self.font_family, 10, "underline"))
                link.pack(side="left", padx=5)
                link.bind("<Button-1>", lambda e, url_to_open=github_profile_url: webbrowser.open_new(url_to_open))
    
        # Source Code Repo Frame in basic_information_frame
        source_code_repo_frame = ttk.Frame(basic_information_frame)
        source_code_repo_frame.pack(anchor="w", padx=10, pady=5, fill="x")

        # Source Code Repo Label
        ttk.Label(source_code_repo_frame, text=self.translator.translate("project_source_code_repo") + ":",
                  font=(self.font_family, 10)).pack(side="left")
        
        # Project Source Code Repo Link
        github_repo_url = "https://github.com/Goo-aw233/MSPCManagerHelper"
        github_repo_link = ttk.Label(source_code_repo_frame,
                            text="GitHub",
                            foreground="#0078D7",
                            cursor="hand2",
                            font=(self.font_family, 10, "underline"))
        github_repo_link.pack(side="left", padx=5)
        github_repo_link.bind("<Button-1>", lambda e, url_to_open=github_repo_url: webbrowser.open_new(url_to_open))

        # License Frame in basic_information_frame
        license_frame = ttk.Frame(basic_information_frame)
        license_frame.pack(anchor="w", padx=10, pady=5, fill="x")

        # License Label
        ttk.Label(license_frame, text=self.translator.translate('open_source_license') + ":",
                  font=(self.font_family, 10)).pack(side="left")
        
        # License Link
        license_url = "https://github.com/Goo-aw233/MSPCManagerHelper/blob/main/LICENSE.txt"
        license_link = ttk.Label(license_frame,
                                text=f"{ProgramMetadata.PROGRAM_LICENSE}",
                                foreground="#0078D7",
                                cursor="hand2",
                                font=(self.font_family, 10, "underline"))
        license_link.pack(side="left", padx=5)
        license_link.bind("<Button-1>", lambda e, url_to_open=license_url: webbrowser.open_new(url_to_open))
        # ======================= End of Basic Information Frame Section =======================

        # ======================= Terms of Use Frame Section =======================
        terms_of_use_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("terms_of_use"))
        terms_of_use_frame.pack(padx=10, pady=(0, 10), fill="x")

        # Card-like container using tkinter.Frame to support custom border.
        border_color = style.lookup("TLabel", "background") or "#cfcfcf"
        card = tkinter.Frame(terms_of_use_frame, background=frame_bg, highlightbackground=border_color,
                             highlightthickness=1, bd=0)
        card.pack(fill="both", padx=10, pady=5, expand=True)

        # The inner frame to hold text + scrollbar (small padding).
        terms_inner_frame = ttk.Frame(card)
        terms_inner_frame.pack(fill="both", expand=True, padx=6, pady=6)

        terms_of_use_text_box = tkinter.Text(
            terms_inner_frame,
            wrap="word",
            height=8,
            font=(self.font_family, 10),
            bg=frame_bg,
            fg=text_fg,
            insertbackground=text_fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=6, pady=6
        )
        terms_of_use_text_box.pack(side="left", fill="both", expand=True)

        # Vertical themed scrollbar local to the text area.
        terms_of_use_text_scrollbar = ttk.Scrollbar(terms_inner_frame, orient="vertical",
                                                    command=terms_of_use_text_box.yview)
        terms_of_use_text_scrollbar.pack(side="right", fill="y")
        terms_of_use_text_box.configure(yscrollcommand=terms_of_use_text_scrollbar.set)

        # Populate and set readonly.
        terms_of_use_text = self.translator.translate("terms_of_use_content")
        if terms_of_use_text:
            terms_of_use_text_box.insert("1.0", terms_of_use_text)
        terms_of_use_text_box.configure(state="disabled")
        # ======================= End of Terms of Use Frame Section =======================

        # ======================= Privacy Policy Frame Section =======================
        privacy_policy_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("privacy_policy"))
        privacy_policy_frame.pack(padx=10, pady=(0, 10), fill="x")

        privacy_card = tkinter.Frame(privacy_policy_frame, background=frame_bg, highlightbackground=border_color,
                                     highlightthickness=1, bd=0)
        privacy_card.pack(fill="both", padx=10, pady=5, expand=True)

        privacy_inner_frame = ttk.Frame(privacy_card)
        privacy_inner_frame.pack(fill="both", expand=True, padx=6, pady=6)

        privacy_text_box = tkinter.Text(
            privacy_inner_frame,
            wrap="word",
            height=8,
            font=(self.font_family, 10),
            bg=frame_bg,
            fg=text_fg,
            insertbackground=text_fg,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=6, pady=6
        )
        privacy_text_box.pack(side="left", fill="both", expand=True)

        privacy_text_scrollbar = ttk.Scrollbar(privacy_inner_frame, orient="vertical", command=privacy_text_box.yview)
        privacy_text_scrollbar.pack(side="right", fill="y")
        privacy_text_box.configure(yscrollcommand=privacy_text_scrollbar.set)

        # Populate and set readonly.
        privacy_text = self.translator.translate("privacy_policy_content")
        if privacy_text:
            privacy_text_box.insert("1.0", privacy_text)
        privacy_text_box.configure(state="disabled")

        # Button container placed under the card but inside the LabelFrame.
        privacy_button_frame = ttk.Frame(privacy_policy_frame)
        privacy_button_frame.pack(anchor="w", padx=10, pady=(0, 8), fill="x")
        privacy_button_frame.grid_columnconfigure(0, weight=1)

        privacy_settings_description_label = ttk.Label(
            privacy_button_frame,
            text=self.translator.translate("privacy_settings_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        privacy_settings_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        privacy_settings_button = ttk.Button(
            privacy_button_frame,
            text=self.translator.translate("privacy_settings"),
            style="AboutPage.TButton",
            command=self._open_privacy_settings
        )
        privacy_settings_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _privacy_settings_wrap(e):
            btn_w = privacy_settings_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            privacy_settings_description_label.config(wraplength=wrap)
        privacy_button_frame.bind("<Configure>", _privacy_settings_wrap)
        # ======================= End of Privacy Policy Frame Section =======================

        # ======================= Get Help Frame Section =======================
        get_help_frame = ttk.LabelFrame(content_frame, text=self.translator.translate("get_help"))
        get_help_frame.pack(padx=10, pady=(0, 10), fill="x")

        # --- Row 1: Get Help Button and Description ---
        get_help_row_frame = ttk.Frame(get_help_frame)
        get_help_row_frame.pack(anchor="w", padx=10, pady=(5, 8), fill="x")
        get_help_row_frame.grid_columnconfigure(0, weight=1)

        get_help_description_label = ttk.Label(
            get_help_row_frame,
            text=self.translator.translate("redirect_to_official_website_to_get_help"),
            font=(self.font_family, 10),
            justify="left"
        )
        get_help_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        get_help_button = ttk.Button(
            get_help_row_frame,
            text=self.translator.translate("get_help"),
            style="AboutPage.TButton",
            command=self._on_get_help_button_click
        )
        get_help_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _get_help_wrap(e):
            btn_w = get_help_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            get_help_description_label.config(wraplength=wrap)
        get_help_row_frame.bind("<Configure>", _get_help_wrap)

        # --- Row 2: Official Website Button and Description ---
        official_website_row_frame = ttk.Frame(get_help_frame)
        official_website_row_frame.pack(anchor="w", padx=10, pady=(0, 8), fill="x")
        official_website_row_frame.grid_columnconfigure(0, weight=1)

        official_website_description_label = ttk.Label(
            official_website_row_frame,
            text=self.translator.translate("official_website_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        official_website_description_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        official_website_button = ttk.Button(
            official_website_row_frame,
            text=self.translator.translate("official_website"),
            style="AboutPage.TButton",
            command=lambda: webbrowser.open_new("https://pcmanager.microsoft.com")
        )
        official_website_button.grid(row=0, column=1, sticky="e", padx=(6, 8))

        def _official_website_wrap(e):
            btn_w = official_website_button.winfo_width() or 0
            wrap = max(20, e.width - btn_w - 20)
            official_website_description_label.config(wraplength=wrap)
        official_website_row_frame.bind("<Configure>", _official_website_wrap)
        # ======================= End of Get Help Frame Section =======================

    def _get_localization_translators(self):
        translations = getattr(self.translator, "translations", {})
        if not isinstance(translations, dict):
            return []

        keys = list(translations.keys())
        # Attempt to find the start and end indices.
        try:
            start_index = keys.index("__localization_translator_list__") + 1
            end_index = keys.index("__localization_translator_list_end__")
        except ValueError:
            # If the markers are missing, return an empty list.
            return []

        translator_list_result = []
        for key in keys[start_index:end_index]:
            # Filter out additional internal markers (starting with "__").
            if key.startswith("__"):
                continue
            display_name = translations.get(key, key)
            translator_list_result.append((key, display_name))
        return translator_list_result

    def _open_privacy_settings(self):
        privacy_settings_uri = "ms-settings:privacy"

        try:
            os.startfile(privacy_settings_uri)
            self.logger.info("Opened privacy settings via os.startfile.")
        except Exception as e_os:
            self.logger.warning(f"os.startfile failed: {e_os}. Trying CMD fallback...")

            cmd_success = False
            try:
                subprocess.run(
                    ["cmd.exe", "/C", "start", "Privacy Settings", f"{privacy_settings_uri}"],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                self.logger.info("Opened privacy settings via CMD.")
                cmd_success = True
            except Exception as e_cmd:
                self.logger.warning(f"CMD start failed: {e_cmd}. Trying webbrowser fallback...")

            if not cmd_success:
                powershell_success = False
                try:
                    subprocess.run(
                        ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{privacy_settings_uri}'"],
                        check=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    self.logger.info("Opened privacy settings via PowerShell Start-Process.")
                    powershell_success = True
                except Exception as e_windows_powersshell:
                    self.logger.warning(f"PowerShell Start-Process failed: {e_windows_powersshell}. Trying webbrowser fallback...")

                if not powershell_success:
                    try:
                        webbrowser.open(privacy_settings_uri)
                        self.logger.info("Opened privacy settings via webbrowser.")
                    except Exception as e_webbrowser:
                        self.logger.error(f"Failed to open privacy settings via all methods. Error: {e_webbrowser}")

    def _on_get_help_button_click(self):
        messagebox.showinfo(
            title=self.translator.translate("info"),
            message=self.translator.translate("redirect_to_official_website_to_get_help")
        )
        webbrowser.open_new("https://pcmanager.microsoft.com")
        self.logger.info("Redirected user to official website for help.")
