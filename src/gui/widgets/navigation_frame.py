from typing import Callable, Dict

import customtkinter

from core.program_metadata import ProgramMetadata
from core.program_settings import ProgramSettings


class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, master, translator, font_family: str, on_nav: Callable[[str], None]):
        self.translator = translator
        self.on_nav = on_nav
        self.font_family = font_family
        self.colors = self._get_palette()
        super().__init__(master, fg_color=self.colors["nav_bg"], corner_radius=0)

        self.nav_buttons: Dict[str, customtkinter.CTkButton] = {}
        self.active_key: str | None = None
        self.grid_rowconfigure(99, weight=1)

        self._build_header()
        self._build_navigation()

    def _get_palette(self) -> Dict[str, str]:
        appearance = ProgramSettings.get_effective_theme_mode().lower()
        if appearance == "dark":
            return {
                "accent": "#3aa0ff",
                "accent_hover": "#2d8cdf",
                "nav_bg": "#1f1f1f",
                "nav_hover": "#2a2a2a",
                "text_primary": "#f5f5f5",
                "text_secondary": "#9aa0a6",
            }
        return {
            "accent": "#0f6cbd",
            "accent_hover": "#115ea3",
            "nav_bg": "#f2f2f2",
            "nav_hover": "#e5f1fb",
            "text_primary": "#1b1b1b",
            "text_secondary": "#5a5a5a",
        }

    def _build_header(self) -> None:
        self.header_label = customtkinter.CTkLabel(
            self,
            text=f"{ProgramMetadata.PROGRAM_NAME}",
            font=(self.font_family, 20, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w",
        )
        self.header_label.grid(row=0, column=0, padx=16, pady=(18, 10), sticky="w")

    def _build_navigation(self) -> None:
        pages = [
            ("home", "home_page"),
            ("maintenance", "maintenance_page"),
            ("installer", "installer_page"),
            ("uninstaller", "uninstaller_page"),
            ("utilities", "utilities_page"),
            ("toolbox", "toolbox_page"),
            ("about", "about_page"),
            ("settings", "settings_page"),
        ]

        for index, (name, translation_key) in enumerate(pages, start=1):
            button = customtkinter.CTkButton(
                self,
                text=self.translator.translate(translation_key),
                anchor="w",
                width=196,
                height=38,
                font=(self.font_family, 14),
                fg_color="transparent",
                hover_color=self.colors["nav_hover"],
                text_color=self.colors["text_primary"],
                corner_radius=4,
                command=lambda target=name: self._on_nav_clicked(target),
            )
            button.grid(row=index, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[name] = button

    def _on_nav_clicked(self, key: str) -> None:
        if self.on_nav:
            self.on_nav(key)
        self.set_active(key)

    def set_active(self, key: str) -> None:
        self.active_key = key
        for name, button in self.nav_buttons.items():
            if name == key:
                button.configure(fg_color=self.colors["accent"], text_color="#ffffff", hover_color=self.colors["accent_hover"])
            else:
                button.configure(fg_color="transparent", text_color=self.colors["text_primary"], hover_color=self.colors["nav_hover"])

    def refresh_palette(self) -> None:
        self.colors = self._get_palette()
        self.configure(fg_color=self.colors["nav_bg"])

        self.header_label.configure(text_color=self.colors["text_primary"])
        for _, button in self.nav_buttons.items():
            button.configure(text_color=self.colors["text_primary"], hover_color=self.colors["nav_hover"], fg_color="transparent")

        if self.active_key:
            self.set_active(self.active_key)
