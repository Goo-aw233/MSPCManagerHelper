import tkinter
import tkinter.filedialog

import customtkinter
from CTkToolTip import CTkToolTip

from core import (
    AdvancedStartup,
    OptionalChecks
)
from gui.components import (
    BaseWidgets
)
from modules.installer import (
    InstallMicrosoftEdgeWebView2Runtime,
    InstallViaDISM,
    InstallViaMicrosoftStore,
    InstallViaPowerShellForCurrentUser,
    ReinstallViaPowerShell
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

        # --- Install via Microsoft Store ---
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
        self.open_msstore_options_frame = customtkinter.CTkScrollableFrame(
            install_via_msstore_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.open_msstore_options_frame.pack(fill="x", padx=10, pady=5)

        self.open_msstore_var = tkinter.StringVar(value="open_msstore")

        # Open Microsoft Store
        self.open_msstore_radiobutton = customtkinter.CTkRadioButton(
            self.open_msstore_options_frame,
            text=self.app_translator.translate("pages.installer.open_msstore"),
            variable=self.open_msstore_var,
            value="open_msstore",
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.open_msstore_radiobutton.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Open Microsoft Store Web Page
        self.open_msstore_web_radiobutton = customtkinter.CTkRadioButton(
            self.open_msstore_options_frame,
            text=self.app_translator.translate("pages.installer.open_msstore_web"),
            variable=self.open_msstore_var,
            value="open_msstore_web",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.open_msstore_web_radiobutton.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Download Online Installer
        self.download_online_installer_radiobutton = customtkinter.CTkRadioButton(
            self.open_msstore_options_frame,
            text=self.app_translator.translate("pages.installer.download_online_installer"),
            variable=self.open_msstore_var,
            value="download_online_installer",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.download_online_installer_radiobutton.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # --- Install Microsoft EdgeWebView2 Runtime ---
        install_webview2_frame = self._create_group_frame()
        install_webview2_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.install_webview2_card = self._create_actions_card(
            parent=install_webview2_frame,
            title=self.app_translator.translate("pages.installer.install_webview2"),
            description=self.app_translator.translate("pages.installer.install_webview2_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_install_webview2,
            state="normal"
        )

        self._create_separator(install_webview2_frame)

        # - Install Microsoft EdgeWebView2 Runtime Options -
        self.install_webview2_options_frame = customtkinter.CTkScrollableFrame(
            install_webview2_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.install_webview2_options_frame.pack(fill="x", padx=10, pady=5)

        self.install_webview2_installer_var = tkinter.StringVar(value="online_install")

        # Online Installer
        self.online_installer_radiobutton = customtkinter.CTkRadioButton(
            self.install_webview2_options_frame,
            text=self.app_translator.translate("pages.installer.online_installer"),
            variable=self.install_webview2_installer_var,
            value="online_install",
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.online_installer_radiobutton.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Offline Installer
        self.offline_installer_radiobutton = customtkinter.CTkRadioButton(
            self.install_webview2_options_frame,
            text=self.app_translator.translate("pages.installer.offline_installer"),
            variable=self.install_webview2_installer_var,
            value="offline_install",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.offline_installer_radiobutton.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Silent Install
        self.silent_install_checkbox = customtkinter.CTkCheckBox(
            self.install_webview2_options_frame,
            text=self.app_translator.translate("pages.installer.silent_install"),
            onvalue="silent_install",
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.silent_install_checkbox.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        # === End of Online Install Section ===

        # === Offline Install Section ===
        self._create_section_label(self.app_translator.translate("pages.installer.offline_install"))

        # --- Install via DISM ---
        install_via_dism_frame = self._create_group_frame()
        install_via_dism_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.install_via_dism_card = self._create_actions_card(
            parent=install_via_dism_frame,
            title=self.app_translator.translate("pages.installer.install_via_dism"),
            description=self.app_translator.translate("pages.installer.install_via_dism_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_install_via_dism,
            state="normal"
        )

        self._create_separator(install_via_dism_frame)

        # - Install via DISM Options -
        self.install_via_dism_options_frame = customtkinter.CTkScrollableFrame(
            install_via_dism_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=147
        )
        self.install_via_dism_options_frame.pack(fill="x", padx=10, pady=5)

        self.install_image_var = tkinter.StringVar(value="online_image")

        # Image Type Radio Buttons (in a sub-frame)
        self.image_type_frame = customtkinter.CTkFrame(
            self.install_via_dism_options_frame,
            fg_color="transparent"
        )
        self.image_type_frame.grid(row=0, column=0, sticky="w", padx=(10, 0), pady=5)

        # Online Image
        self.online_image_radiobutton = customtkinter.CTkRadioButton(
            self.image_type_frame,
            text=self.app_translator.translate("pages.common.online_image"),
            variable=self.install_image_var,
            value="online_image",
            command=self._toggle_offline_image_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.online_image_radiobutton.pack(side="left", padx=(0, 5))

        # Offline Image
        self.offline_image_radiobutton = customtkinter.CTkRadioButton(
            self.image_type_frame,
            text=self.app_translator.translate("pages.common.offline_image"),
            variable=self.install_image_var,
            value="offline_image",
            command=self._toggle_offline_image_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.offline_image_radiobutton.pack(side="left")
        CTkToolTip(self.offline_image_radiobutton,
                   self.app_translator.translate("pages.common.offline_image_tooltip"),
                   font=(self.font_family, 12))
        
        # Offline Image Path Entry
        self.offline_image_path_entry = customtkinter.CTkEntry(
            self.install_via_dism_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.offline_image_path_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.offline_image_path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)
        self.offline_image_path_entry.bind("<KeyRelease>", lambda _: self._update_install_via_dism_state())

        # Offline Image Path Select Button
        self.offline_image_path_select_button = customtkinter.CTkButton(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_offline_image_path
        )
        self.offline_image_path_select_button.grid(row=0, column=3, sticky="w", padx=(0, 10), pady=5)

        # Application Package
        self.app_package_var = tkinter.BooleanVar(value=True)
        self.app_package_checkbox = customtkinter.CTkCheckBox(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.installer.app_package"),
            variable=self.app_package_var,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold"),
            command=self._toggle_app_package_state
        )
        self.app_package_checkbox.grid(row=1, column=0, sticky="w", padx=(10, 0), pady=5)

        # Application Package Path Entry
        self.app_package_path_entry = customtkinter.CTkEntry(
            self.install_via_dism_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.app_package_path_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.app_package_path_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)
        self.app_package_path_entry.bind("<KeyRelease>", lambda _: self._update_install_via_dism_state())

        # Application Package Path Select Button
        self.app_package_path_select_button = customtkinter.CTkButton(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_app_package_path
        )
        self.app_package_path_select_button.grid(row=1, column=3, sticky="w", padx=(0, 10), pady=5)

        # License
        self.license_checkbox = customtkinter.CTkCheckBox(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.installer.license"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._toggle_license_state
        )
        self.license_checkbox.grid(row=2, column=0, sticky="w", padx=(10, 0), pady=5)

        # License Path Entry
        self.license_path_entry = customtkinter.CTkEntry(
            self.install_via_dism_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.license_path_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.license_path_entry.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)

        # License Path Select Button
        self.license_path_select_button = customtkinter.CTkButton(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_license_path,
            state="disabled"
        )
        self.license_path_select_button.grid(row=2, column=3, sticky="w", padx=(0, 10), pady=5)

        # Dependencies
        self.dependencies_checkbox = customtkinter.CTkCheckBox(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.installer.dependencies"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._toggle_dependencies_state
        )
        self.dependencies_checkbox.grid(row=3, column=0, sticky="w", padx=(10, 0), pady=5)

        # Dependencies Paths Entry
        self.dependencies_paths_entry = customtkinter.CTkEntry(
            self.install_via_dism_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.dependencies_paths_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.dependencies_paths_entry.grid(row=3, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)

        # Dependencies Paths Select Button
        self.dependencies_paths_select_button = customtkinter.CTkButton(
            self.install_via_dism_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_dependencies_paths,
            state="disabled"
        )
        self.dependencies_paths_select_button.grid(row=3, column=3, sticky="w", padx=(0, 10), pady=5)

        # Apply Initial Toggle States
        self._toggle_offline_image_state()
        self._toggle_app_package_state()
        self._toggle_license_state()
        self._toggle_dependencies_state()
        self._update_install_via_dism_state()

        # --- Install via Windows PowerShell for Current User ---
        install_via_powershell_current_user_frame = self._create_group_frame()
        install_via_powershell_current_user_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.install_via_powershell_current_user_card = self._create_actions_card(
            parent=install_via_powershell_current_user_frame,
            title=self.app_translator.translate("pages.installer.install_via_powershell_current_user"),
            description=self.app_translator.translate("pages.installer.install_via_powershell_current_user_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_install_via_powershell,
            state="normal"
        )

        self._create_separator(install_via_powershell_current_user_frame)

        # - Install via Windows PowerShell Options -
        self.install_via_powershell_current_user_options_frame = customtkinter.CTkScrollableFrame(
            install_via_powershell_current_user_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.install_via_powershell_current_user_options_frame.pack(fill="x", padx=10, pady=5)

        # Force Quit
        self.powershell_force_quit_var = tkinter.BooleanVar(value=False)
        self.powershell_force_quit_checkbox = customtkinter.CTkCheckBox(
            self.install_via_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.installer.force_quit"),
            variable=self.powershell_force_quit_var,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.powershell_force_quit_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        CTkToolTip(self.powershell_force_quit_checkbox,
                   self.app_translator.translate("pages.installer.force_quit_tooltip"),
                   font=(self.font_family, 12))

        # Application Package
        self.powershell_app_package_var = tkinter.BooleanVar(value=True)
        self.powershell_app_package_checkbox = customtkinter.CTkCheckBox(
            self.install_via_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.installer.app_package"),
            variable=self.powershell_app_package_var,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold"),
            command=self._toggle_powershell_app_package_state
        )
        self.powershell_app_package_checkbox.grid(row=1, column=0, sticky="w", padx=(10, 0), pady=5)

        # Application Package Path Entry
        self.powershell_app_package_path_entry = customtkinter.CTkEntry(
            self.install_via_powershell_current_user_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.app_package_path_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.powershell_app_package_path_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)
        self.powershell_app_package_path_entry.bind(
            "<KeyRelease>", lambda _: self._update_install_via_powershell_state()
        )

        # Application Package Path Select Button
        self.powershell_app_package_path_select_button = customtkinter.CTkButton(
            self.install_via_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_powershell_app_package_path
        )
        self.powershell_app_package_path_select_button.grid(row=1, column=3, sticky="w", padx=(0, 10), pady=5)

        # Dependencies
        self.powershell_dependencies_checkbox = customtkinter.CTkCheckBox(
            self.install_via_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.installer.dependencies"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._toggle_powershell_dependencies_state
        )
        self.powershell_dependencies_checkbox.grid(row=2, column=0, sticky="w", padx=(10, 0), pady=5)

        # Dependencies Paths Entry
        self.powershell_dependencies_paths_entry = customtkinter.CTkEntry(
            self.install_via_powershell_current_user_options_frame,
            placeholder_text=self.app_translator.translate("pages.installer.dependencies_paths_placeholder"),
            font=customtkinter.CTkFont(family=self.font_family),
            width=650
        )
        self.powershell_dependencies_paths_entry.grid(row=2, column=1, sticky="ew", padx=(0, 10), pady=5, columnspan=2)

        # Dependencies Paths Select Button
        self.powershell_dependencies_paths_select_button = customtkinter.CTkButton(
            self.install_via_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.common.browse"),
            font=customtkinter.CTkFont(family=self.font_family),
            command=self._select_powershell_dependencies_paths,
            state="disabled"
        )
        self.powershell_dependencies_paths_select_button.grid(row=2, column=3, sticky="w", padx=(0, 10), pady=5)

        # Apply Initial Toggle States
        self._toggle_powershell_app_package_state()
        self._toggle_powershell_dependencies_state()
        self._update_install_via_powershell_state()

        # --- Reinstall via Windows PowerShell ---
        reinstall_via_powershell_frame = self._create_group_frame()
        reinstall_via_powershell_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.reinstall_via_powershell_card = self._create_actions_card(
            parent=reinstall_via_powershell_frame,
            title=self.app_translator.translate("pages.installer.reinstall_via_powershell"),
            description=self.app_translator.translate("pages.installer.reinstall_via_powershell_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_reinstall_via_powershell,
            state="normal"
        )

        self._create_separator(reinstall_via_powershell_frame)

        # - Reinstall via Windows PowerShell Options -
        self.reinstall_via_powershell_options_frame = customtkinter.CTkScrollableFrame(
            reinstall_via_powershell_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=42
        )
        self.reinstall_via_powershell_options_frame.pack(fill="x", padx=10, pady=5)

        self.reinstall_user_scope_var = tkinter.StringVar(value="current_user")

        # All Users
        self.reinstall_all_users_radiobutton = customtkinter.CTkRadioButton(
            self.reinstall_via_powershell_options_frame,
            text=self.app_translator.translate("pages.installer.all_users"),
            variable=self.reinstall_user_scope_var,
            value="all_users",
            command=self._toggle_reinstall_user_scope_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.reinstall_all_users_radiobutton.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Current User
        self.reinstall_current_user_radiobutton = customtkinter.CTkRadioButton(
            self.reinstall_via_powershell_options_frame,
            text=self.app_translator.translate("pages.installer.current_user"),
            variable=self.reinstall_user_scope_var,
            value="current_user",
            command=self._toggle_reinstall_user_scope_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.reinstall_current_user_radiobutton.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.reinstall_action_var = tkinter.StringVar(value="reset")

        # Reinstall
        self.reinstall_reinstall_radiobutton = customtkinter.CTkRadioButton(
            self.reinstall_via_powershell_options_frame,
            text=self.app_translator.translate("pages.installer.reinstall"),
            variable=self.reinstall_action_var,
            value="reinstall",
            command=self._toggle_reinstall_force_quit_state,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.reinstall_reinstall_radiobutton.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Force Quit
        self.reinstall_force_quit_var = tkinter.BooleanVar(value=False)
        self.reinstall_force_quit_checkbox = customtkinter.CTkCheckBox(
            self.reinstall_via_powershell_options_frame,
            text=self.app_translator.translate("pages.installer.force_quit"),
            variable=self.reinstall_force_quit_var,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.reinstall_force_quit_checkbox.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        CTkToolTip(self.reinstall_force_quit_checkbox,
                   self.app_translator.translate("pages.installer.force_quit_tooltip"),
                   font=(self.font_family, 12))

        # Reset
        self.reinstall_reset_radiobutton = customtkinter.CTkRadioButton(
            self.reinstall_via_powershell_options_frame,
            text=self.app_translator.translate("pages.installer.reset"),
            variable=self.reinstall_action_var,
            value="reset",
            command=self._toggle_reinstall_force_quit_state,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.reinstall_reset_radiobutton.grid(row=0, column=4, sticky="w", padx=10, pady=5)

        # Apply Initial Toggle States
        self._toggle_reinstall_user_scope_state()
        self._toggle_reinstall_force_quit_state()
        self._update_reinstall_via_powershell_state()
        # === End of Offline Install Section ===


    # ~~~ Features Functions ~~~
    # ~ Install via Microsoft Store ~
    @staticmethod
    def _update_install_via_msstore_state():
        return "normal"

    def _run_install_via_msstore(self):
        self.install_via_msstore_card.configure(state="disabled")
        self.update_idletasks()

        worker = InstallViaMicrosoftStore(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            open_method=self.open_msstore_var.get()
        )

        self._run_operation(
            worker.execute,
            "pages.installer.install_via_msstore",
            on_completion=lambda: self.install_via_msstore_card.configure(
                state=self._update_install_via_msstore_state()
            )
        )
    # ~ End of Install via Microsoft Store ~

    # ~ Install Microsoft EdgeWebView2 Runtime ~
    def _run_install_webview2(self):
        self.install_webview2_card.configure(state="disabled")
        self.update_idletasks()

        worker = InstallMicrosoftEdgeWebView2Runtime(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            installer_type=self.install_webview2_installer_var.get(),
            silent_install=bool(self.silent_install_checkbox.get())
        )

        self._run_operation(
            worker.execute,
            "pages.installer.install_webview2",
            on_completion=lambda: self.install_webview2_card.configure(state="normal")
        )
    # ~ End of Install Microsoft EdgeWebView2 Runtime ~

    # ~ Install via DISM ~
    def _set_entry_group_state(self, enabled, entry, button=None):
        if button is not None:
            button.configure(state="normal" if enabled else "disabled")
        if enabled:
            entry.configure(state="normal")
            entry.unbind("<Button-1>")
        else:
            entry.configure(state="normal")
            entry.bind("<Button-1>", self._block_entry_event, add="+")

    @staticmethod
    def _set_entry_text(entry, text):
        entry.delete(0, tkinter.END)
        entry.insert(0, text)

    def _toggle_offline_image_state(self):
        enabled = self.install_image_var.get() == "offline_image"
        self._set_entry_group_state(enabled, self.offline_image_path_entry,
                                     self.offline_image_path_select_button)
        self._update_install_via_dism_state()

    def _select_offline_image_path(self):
        folder_path = tkinter.filedialog.askdirectory(
            title=self.app_translator.translate("pages.installer.select_offline_image_path")
        )
        if folder_path:
            self._set_entry_text(self.offline_image_path_entry, folder_path)
        self._update_install_via_dism_state()

    def _select_app_package_path(self):
        file_path = tkinter.filedialog.askopenfilename(
            title=self.app_translator.translate("pages.installer.select_app_package_path"),
            filetypes=[
                (self.app_translator.translate("pages.installer.app_package"),
                 "*.appx;*.appxbundle;*.msix;*.msixbundle"),
                (self.app_translator.translate("pages.common.all_files"), "*.*")
            ]
        )
        if file_path:
            self._set_entry_text(self.app_package_path_entry, file_path)
        self._update_install_via_dism_state()

    def _select_license_path(self):
        file_path = tkinter.filedialog.askopenfilename(
            title=self.app_translator.translate("pages.installer.select_license_path"),
            filetypes=[
                (self.app_translator.translate("pages.installer.license"), "*.xml"),
                (self.app_translator.translate("pages.common.all_files"), "*.*")
            ]
        )
        if file_path:
            self._set_entry_text(self.license_path_entry, file_path)

    def _select_dependencies_paths(self):
        file_paths = tkinter.filedialog.askopenfilenames(
            title=self.app_translator.translate("pages.installer.select_dependencies_paths"),
            filetypes=[
                (self.app_translator.translate("pages.installer.dependencies"), "*.appx;*.msix"),
                (self.app_translator.translate("pages.common.all_files"), "*.*")
            ]
        )
        if file_paths:
            self._set_entry_text(self.dependencies_paths_entry, " | ".join(file_paths))

    def _toggle_app_package_state(self):
        enabled = self.app_package_var.get()
        self._set_entry_group_state(enabled, self.app_package_path_entry,
                                     self.app_package_path_select_button)
        self._update_install_via_dism_state()

    def _toggle_license_state(self):
        enabled = self.license_checkbox.get()
        self._set_entry_group_state(enabled, self.license_path_entry,
                                     self.license_path_select_button)

    def _toggle_dependencies_state(self):
        enabled = self.dependencies_checkbox.get()
        self._set_entry_group_state(enabled, self.dependencies_paths_entry,
                                     self.dependencies_paths_select_button)

    @staticmethod
    def _block_entry_event(_):
        return "break"

    def _update_install_via_dism_state(self):
        if not AdvancedStartup.is_administrator():
            self.install_via_dism_card.configure(state="disabled")
            return
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["Dism.exe"],
                                                                   suppress_complete_log=True):
            self.logger.warning("Dism.exe is not available. Disabling 'Install via DISM' option.")
            self.install_via_dism_card.configure(state="disabled")
            return
        if self.install_image_var.get() == "offline_image" and not self.offline_image_path_entry.get().strip():
            self.install_via_dism_card.configure(state="disabled")
            return
        if not self.app_package_var.get() or not self.app_package_path_entry.get().strip():
            self.install_via_dism_card.configure(state="disabled")
            return
        self.install_via_dism_card.configure(state="normal")
    
    def _run_install_via_dism(self):
        self.install_via_dism_card.configure(state="disabled")
        self.update_idletasks()

        worker = InstallViaDISM(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            image_type=self.install_image_var.get(),
            offline_image_path=self.offline_image_path_entry.get() if self.install_image_var.get() == "offline_image" else "",
            app_package_path=self.app_package_path_entry.get(),
            license_path=self.license_path_entry.get() if self.license_checkbox.get() else "",
            dependencies_paths=self.dependencies_paths_entry.get() if self.dependencies_checkbox.get() else ""
        )

        self._run_operation(
            worker.execute,
            "pages.installer.install_via_dism",
            on_completion=lambda: self._update_install_via_dism_state()
        )
    # ~ End of Install via DISM ~

    # ~ Install via Windows PowerShell for Current User ~
    def _toggle_powershell_app_package_state(self):
        enabled = self.powershell_app_package_var.get()
        self._set_entry_group_state(enabled, self.powershell_app_package_path_entry,
                                     self.powershell_app_package_path_select_button)
        self._update_install_via_powershell_state()

    def _toggle_powershell_dependencies_state(self):
        enabled = self.powershell_dependencies_checkbox.get()
        self._set_entry_group_state(enabled, self.powershell_dependencies_paths_entry,
                                     self.powershell_dependencies_paths_select_button)

    def _select_powershell_app_package_path(self):
        file_path = tkinter.filedialog.askopenfilename(
            title=self.app_translator.translate("pages.installer.select_app_package_path"),
            filetypes=[
                (self.app_translator.translate("pages.installer.app_package"),
                 "*.appx;*.appxbundle;*.msix;*.msixbundle"),
                (self.app_translator.translate("pages.common.all_files"), "*.*")
            ]
        )
        if file_path:
            self._set_entry_text(self.powershell_app_package_path_entry, file_path)
        self._update_install_via_powershell_state()

    def _select_powershell_dependencies_paths(self):
        file_paths = tkinter.filedialog.askopenfilenames(
            title=self.app_translator.translate("pages.installer.select_dependencies_paths"),
            filetypes=[
                (self.app_translator.translate("pages.installer.dependencies"), "*.appx;*.msix"),
                (self.app_translator.translate("pages.common.all_files"), "*.*")
            ]
        )
        if file_paths:
            self._set_entry_text(self.powershell_dependencies_paths_entry, " | ".join(file_paths))

    def _update_install_via_powershell_state(self):
        if not AdvancedStartup.is_administrator():
            self.install_via_powershell_current_user_card.configure(state="disabled")
            return
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"],
                                                                   suppress_complete_log=True):
            self.logger.warning(
                "powershell.exe is not available. Disabling 'Install via Windows PowerShell (Current User)' option.")
            self.install_via_powershell_current_user_card.configure(state="disabled")
            return
        if (not self.powershell_app_package_var.get()
                or not self.powershell_app_package_path_entry.get().strip()):
            self.install_via_powershell_current_user_card.configure(state="disabled")
            return
        self.install_via_powershell_current_user_card.configure(state="normal")

    def _run_install_via_powershell(self):
        self.install_via_powershell_current_user_card.configure(state="disabled")
        self.update_idletasks()

        worker = InstallViaPowerShellForCurrentUser(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            force_quit=self.powershell_force_quit_var.get(),
            app_package_path=self.powershell_app_package_path_entry.get(),
            dependencies_paths=self.powershell_dependencies_paths_entry.get()
            if self.powershell_dependencies_checkbox.get() else ""
        )

        self._run_operation(
            worker.execute,
            "pages.installer.install_via_powershell_current_user",
            on_completion=lambda: self._update_install_via_powershell_state()
        )
    # ~ End of Install via Windows PowerShell for Current User ~

    # ~ Reinstall via Windows PowerShell ~
    def _toggle_reinstall_user_scope_state(self):
        if self.reinstall_user_scope_var.get() == "all_users":
            self.reinstall_reset_radiobutton.configure(state="disabled")
            self.reinstall_action_var.set("reinstall")
        else:
            self.reinstall_reset_radiobutton.configure(state="normal")
        self._toggle_reinstall_force_quit_state()

    def _toggle_reinstall_force_quit_state(self):
        if self.reinstall_action_var.get() == "reinstall":
            self.reinstall_force_quit_checkbox.configure(state="normal")
        else:
            self.reinstall_force_quit_var.set(False)
            self.reinstall_force_quit_checkbox.configure(state="disabled")

    def _update_reinstall_via_powershell_state(self):
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"],
                                                                   suppress_complete_log=True):
            self.logger.warning(
                "powershell.exe is not available. Disabling 'Reinstall via Windows PowerShell' option.")
            self.reinstall_via_powershell_card.configure(state="disabled")
            return
        self.reinstall_via_powershell_card.configure(state="normal")

    def _run_reinstall_via_powershell(self):
        self.reinstall_via_powershell_card.configure(state="disabled")
        self.update_idletasks()

        worker = ReinstallViaPowerShell(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            action=self.reinstall_action_var.get(),
            user_scope=self.reinstall_user_scope_var.get(),
            force_quit=self.reinstall_force_quit_var.get()
        )

        self._run_operation(
            worker.execute,
            "pages.installer.reinstall_via_powershell",
            on_completion=lambda: self.reinstall_via_powershell_card.configure(state="normal")
        )
    # ~ End of Reinstall via Windows PowerShell ~
