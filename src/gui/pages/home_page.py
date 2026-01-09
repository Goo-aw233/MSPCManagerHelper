import customtkinter
from core.app_metadata import AppMetadata


class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(parent, fg_color="transparent")
        self.app_translator = app_translator
        self.font_family = font_family

        # Main Layout configuration (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Page Title Label
        self.page_title_label = customtkinter.CTkLabel(
            self,
            text=self.app_translator.translate("home_page"),
            font=customtkinter.CTkFont(family=self.font_family, size=24, weight="bold")
        )
        self.page_title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Scrollable Content
        self.scroll_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # --- Welcome Section ---
        self._create_section_label(self.app_translator.translate("welcome_title"))

        self.welcome_group = self._create_group_frame()

        # Welcome Header
        self.welcome_header_frame = customtkinter.CTkFrame(self.welcome_group, fg_color="transparent")
        self.welcome_header_frame.pack(fill="x", padx=16, pady=(16, 12))

        self.welcome_title_label = customtkinter.CTkLabel(
            self.welcome_header_frame,
            text=f"{self.app_translator.translate('welcome_to')} {AppMetadata.APP_NAME}",
            font=customtkinter.CTkFont(family=self.font_family, size=14),
            anchor="w"
        )
        self.welcome_title_label.pack(fill="x")

        # Welcome Description Textbox
        self.welcome_description_textbox = customtkinter.CTkTextbox(
            self.welcome_header_frame,
            font=customtkinter.CTkFont(family=self.font_family, size=12),
            text_color=("gray50", "gray70"),
            fg_color="transparent",
            height=70,
            wrap="word",
            activate_scrollbars=False,  # Disable Scrollbars
            border_width=0
        )
        self.welcome_description_textbox.pack(fill="x", pady=(4, 0))
        self.welcome_description_textbox.insert("1.0", self.app_translator.translate("welcome_message"))
        self.welcome_description_textbox.configure(state="disabled")
        # Disable Text Selection
        self.welcome_description_textbox.bind("<Button-1>", lambda e: "break")  # Disable Single Click
        self.welcome_description_textbox.bind("<B1-Motion>", lambda e: "break")  # Disable Click & Drag
        self.welcome_description_textbox.bind("<Double-Button-1>", lambda e: "break")  # Disable Double Click
        self.welcome_description_textbox.bind("<Triple-Button-1>", lambda e: "break")  # Disable Triple Click
        # --- End of Welcome Section ---

    def _create_section_label(self, text):
        label = customtkinter.CTkLabel(
            self.scroll_frame,
            text=text,
            font=customtkinter.CTkFont(family=self.font_family, size=16, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(20, 10))

    def _create_group_frame(self):
        frame = customtkinter.CTkFrame(
            self.scroll_frame,
            fg_color=("gray95", "#202020"),
            corner_radius=4,
            border_width=1,
            border_color=("gray90", "#2b2b2b")
        )
        frame.pack(fill="x", padx=20, pady=0)
        return frame
