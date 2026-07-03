import tkinter

import customtkinter

from gui.components import (
    BaseWidgets
)
from modules.installer import (
    InstallViaMicrosoftStore
)
from .base_page_frame import BaseFuncPageFrame


class InstallerPage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.installer",
            events_textbox_wrap="none"
        )

        # === Online Install Section ===
        self._create_section_label(self.app_translator.translate("pages.installer.online_install"))

        # --- Install Via Microsoft Store ---
        install_via_msstore_frame = self._create_group_frame()
        install_via_msstore_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.install_via_msstore_card = self._create_actions_card(
            parent=install_via_msstore_frame,
            title=self.app_translator.translate("pages.installer.install_via_msstore"),
            description=self.app_translator.translate("pages.installer.install_via_msstore_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_install_via_msstore,
            state=self._update_install_via_msstore_state()
        )

        self._create_separator(install_via_msstore_frame)

        # - Open Options -
        self.open_options_frame = customtkinter.CTkScrollableFrame(
            install_via_msstore_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.open_options_frame.pack(fill="x", padx=10, pady=5)

        self.open_msstore_var = tkinter.StringVar(value="open_msstore")

        # Open Microsoft Store
        self.open_msstore_radiobutton = customtkinter.CTkRadioButton(
            self.open_options_frame,
            text=self.app_translator.translate("pages.installer.open_msstore"),
            variable=self.open_msstore_var,
            value="open_msstore",
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.open_msstore_radiobutton.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Open Microsoft Store Web Page
        self.open_msstore_web_radiobutton = customtkinter.CTkRadioButton(
            self.open_options_frame,
            text=self.app_translator.translate("pages.installer.open_msstore_web"),
            variable=self.open_msstore_var,
            value="open_msstore_web",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.open_msstore_web_radiobutton.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Download Online Installer
        self.download_online_installer_radiobutton = customtkinter.CTkRadioButton(
            self.open_options_frame,
            text=self.app_translator.translate("pages.installer.download_online_installer"),
            variable=self.open_msstore_var,
            value="download_online_installer",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.download_online_installer_radiobutton.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        # === End of Online Install Section ===


    # ~~~ Features Functions ~~~
    # ~ Install Via Microsoft Store ~
    @staticmethod
    def _update_install_via_msstore_state():
        return "normal"

    def _run_install_via_msstore(self):
        self.install_via_msstore_card.configure(state="disabled")
        self.update_idletasks()

        installer = InstallViaMicrosoftStore(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            open_method=self.open_msstore_var.get()
        )

        self._run_operation(
            installer.execute,
            "pages.installer.install_via_msstore",
            on_completion=lambda: self.install_via_msstore_card.configure(
                state=self._update_install_via_msstore_state()
            )
        )
    # ~ End of Install Via Microsoft Store ~
