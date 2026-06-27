import tkinter

import customtkinter
from CTkToolTip import CTkToolTip

from core import (
    AdvancedStartup,
    OptionalChecks
)
from gui.components import (
    BaseWidgets,
)
from modules.uninstaller import (
    UninstallBeta,
    UninstallViaDISMForAllUsers,
    UninstallViaPowerShellForAllUsers,
    UninstallViaPowerShellForCurrentUser
)
from .base_page_frame import BaseFuncPageFrame


class UninstallerPage(BaseFuncPageFrame, BaseWidgets):
    def __init__(self, parent, app_translator, font_family):
        super().__init__(
            parent=parent,
            app_translator=app_translator,
            font_family=font_family,
            page_title_key="pages.navigation.uninstaller",
            events_textbox_wrap="none"
        )

        # === Uninstall Stable ===
        self._create_section_label(self.app_translator.translate("pages.uninstaller.uninstall_stable"))

        # --- Uninstall via DISM for All Users ---
        uninstall_via_dism_for_all_users_frame = self._create_group_frame()
        uninstall_via_dism_for_all_users_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.uninstall_via_dism_all_users_card = self._create_actions_card(
            parent=uninstall_via_dism_for_all_users_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_dism_all_users"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_dism_all_users_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_dism_all_users,
            state=self._update_uninstall_via_dism_all_users_state()
        )

        self._create_separator(uninstall_via_dism_for_all_users_frame)

        # - Uninstall Options -
        self.uninstall_options_frame = customtkinter.CTkScrollableFrame(
            uninstall_via_dism_for_all_users_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.uninstall_options_frame.pack(fill="x", padx=10, pady=5)

        self.uninstall_image_var = tkinter.StringVar(value="online_image")

        # Online Image
        self.radiobutton_online_image = customtkinter.CTkRadioButton(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.common.online_image"),
            variable=self.uninstall_image_var,
            value="online_image",
            command=self._on_uninstall_image_change,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.radiobutton_online_image.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Offline Image
        self.radiobutton_offline_image = customtkinter.CTkRadioButton(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.common.offline_image"),
            variable=self.uninstall_image_var,
            value="offline_image",
            command=self._on_uninstall_image_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.radiobutton_offline_image.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        CTkToolTip(self.radiobutton_offline_image,
                   self.app_translator.translate("pages.common.offline_image_description"), font=(self.font_family, 12))

        # Basic Cleanup
        self.checkbox_basic_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._on_basic_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_basic_cleanup.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Advanced Cleanup
        self.checkbox_advanced_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_cleanup"),
            command=self._on_advanced_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_advanced_cleanup.grid(row=0, column=3, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.checkbox_basic_select_all = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.checkbox_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._on_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.checkbox_basic_registries = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._on_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.checkbox_basic_cache_files = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._on_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Advanced Select All
        self.checkbox_advanced_select_all = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_advanced_select_all,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_advanced_select_all.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Advanced App Package Data
        self.checkbox_advanced_app_package_data = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_app_package_data"),
            command=self._on_advanced_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_advanced_app_package_data.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Advanced Registries
        self.checkbox_advanced_registries = customtkinter.CTkCheckBox(
            self.uninstall_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_registries"),
            command=self._on_advanced_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_advanced_registries.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.basic_option_checkboxes = [
            self.checkbox_basic_config_cache_dirs,
            self.checkbox_basic_registries,
            self.checkbox_basic_cache_files
        ]
        self.advanced_option_checkboxes = [
            self.checkbox_advanced_app_package_data,
            self.checkbox_advanced_registries
        ]

        self._update_cleanup_options_state()

        # --- Uninstall via Windows PowerShell for All Users ---
        uninstall_via_powershell_for_all_users_frame = self._create_group_frame()
        uninstall_via_powershell_for_all_users_frame.pack_configure(pady=(0, 5)) # Add a 9-Pixel Spacing Below
        self.uninstall_via_powershell_all_users_card = self._create_actions_card(
            parent=uninstall_via_powershell_for_all_users_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_powershell_all_users"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_powershell_all_users_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_powershell_all_users,
            state=self._update_uninstall_via_powershell_all_users_state()
        )

        self._create_separator(uninstall_via_powershell_for_all_users_frame)

        # - Uninstall Options -
        self.uninstall_powershell_options_frame = customtkinter.CTkScrollableFrame(
            uninstall_via_powershell_for_all_users_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=112
        )
        self.uninstall_powershell_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.checkbox_powershell_basic_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._on_powershell_basic_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_powershell_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Advanced Cleanup
        self.checkbox_powershell_advanced_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_cleanup"),
            command=self._on_powershell_advanced_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_advanced_cleanup.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.checkbox_powershell_basic_select_all = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_powershell_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.checkbox_powershell_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._on_powershell_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.checkbox_powershell_basic_registries = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._on_powershell_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.checkbox_powershell_basic_cache_files = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._on_powershell_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Advanced Select All
        self.checkbox_powershell_advanced_select_all = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_advanced_select_all,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_advanced_select_all.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Advanced App Package Data
        self.checkbox_powershell_advanced_app_package_data = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_app_package_data"),
            command=self._on_powershell_advanced_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_advanced_app_package_data.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Advanced Registries
        self.checkbox_powershell_advanced_registries = customtkinter.CTkCheckBox(
            self.uninstall_powershell_options_frame,
            text=self.app_translator.translate("pages.uninstaller.advanced_registries"),
            command=self._on_powershell_advanced_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_advanced_registries.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.powershell_basic_option_checkboxes = [
            self.checkbox_powershell_basic_config_cache_dirs,
            self.checkbox_powershell_basic_registries,
            self.checkbox_powershell_basic_cache_files
        ]
        self.powershell_advanced_option_checkboxes = [
            self.checkbox_powershell_advanced_app_package_data,
            self.checkbox_powershell_advanced_registries
        ]

        self._update_powershell_cleanup_options_state()

        # --- Uninstall via Windows PowerShell for Current User ---
        uninstall_via_powershell_for_current_user_frame = self._create_group_frame()
        self.uninstall_via_powershell_current_user_card = self._create_actions_card(
            parent=uninstall_via_powershell_for_current_user_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_via_powershell_current_user"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_via_powershell_current_user_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_via_powershell_current_user,
            state=self._update_uninstall_via_powershell_current_user_state()
        )

        self._create_separator(uninstall_via_powershell_for_current_user_frame)

        # - Uninstall Options -
        self.uninstall_powershell_current_user_options_frame = customtkinter.CTkScrollableFrame(
            uninstall_via_powershell_for_current_user_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.uninstall_powershell_current_user_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.checkbox_powershell_current_user_basic_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._on_powershell_current_user_basic_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_powershell_current_user_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.checkbox_powershell_current_user_basic_select_all = customtkinter.CTkCheckBox(
            self.uninstall_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_powershell_current_user_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_powershell_current_user_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.checkbox_powershell_current_user_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.uninstall_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._on_powershell_current_user_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_current_user_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.checkbox_powershell_current_user_basic_registries = customtkinter.CTkCheckBox(
            self.uninstall_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._on_powershell_current_user_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_current_user_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.checkbox_powershell_current_user_basic_cache_files = customtkinter.CTkCheckBox(
            self.uninstall_powershell_current_user_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._on_powershell_current_user_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_powershell_current_user_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.powershell_current_user_basic_option_checkboxes = [
            self.checkbox_powershell_current_user_basic_config_cache_dirs,
            self.checkbox_powershell_current_user_basic_registries,
            self.checkbox_powershell_current_user_basic_cache_files
        ]

        self._update_powershell_current_user_cleanup_options_state()

        # === End of Uninstall Stable ===

        # === Uninstall Beta ===
        self._create_section_label(self.app_translator.translate("pages.uninstaller.uninstall_beta"))

        # --- Uninstall Beta ---
        uninstall_beta_frame = self._create_group_frame()
        self.uninstall_beta_card = self._create_actions_card(
            parent=uninstall_beta_frame,
            title=self.app_translator.translate("pages.uninstaller.uninstall_beta"),
            description=self.app_translator.translate("pages.uninstaller.uninstall_beta_desc"),
            widget_constructor=customtkinter.CTkButton,
            text=self.app_translator.translate("pages.common.execute"),
            command=self._run_uninstall_beta,
            state=self._update_uninstall_beta_state()
        )

        self._create_separator(uninstall_beta_frame)

        # - Uninstall Options -
        self.uninstall_beta_options_frame = customtkinter.CTkScrollableFrame(
            uninstall_beta_frame,
            orientation="horizontal",
            fg_color="transparent",
            height=77
        )
        self.uninstall_beta_options_frame.pack(fill="x", padx=10, pady=5)

        # Basic Cleanup
        self.checkbox_beta_basic_cleanup = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cleanup"),
            command=self._on_beta_basic_cleanup_toggle,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_beta_basic_cleanup.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Basic Select All
        self.checkbox_beta_basic_select_all = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.common.select_all"),
            command=self._toggle_beta_basic_select_all,
            font=customtkinter.CTkFont(family=self.font_family, weight="bold")
        )
        self.checkbox_beta_basic_select_all.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Basic Config & Cache Dirs
        self.checkbox_beta_basic_config_cache_dirs = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_config_cache_dirs"),
            command=self._on_beta_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_beta_basic_config_cache_dirs.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Basic Registries
        self.checkbox_beta_basic_registries = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_registries"),
            command=self._on_beta_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_beta_basic_registries.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Basic Cache Files
        self.checkbox_beta_basic_cache_files = customtkinter.CTkCheckBox(
            self.uninstall_beta_options_frame,
            text=self.app_translator.translate("pages.uninstaller.basic_cache_files"),
            command=self._on_beta_basic_option_change,
            font=customtkinter.CTkFont(family=self.font_family)
        )
        self.checkbox_beta_basic_cache_files.grid(row=1, column=3, sticky="w", padx=10, pady=5)

        # Store checkboxes in lists for easier management.
        self.beta_basic_option_checkboxes = [
            self.checkbox_beta_basic_config_cache_dirs,
            self.checkbox_beta_basic_registries,
            self.checkbox_beta_basic_cache_files
        ]

        self._update_beta_cleanup_options_state()

        # === End of Uninstall Beta ===

    # ~~~ Features Functions ~~~
    # ~ Uninstall via DISM for All Users ~
    def _update_uninstall_via_dism_all_users_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["Dism.exe", "powershell.exe"]):
            state = "disabled"
            self.logger.warning("Dism.exe or PowerShell is not available. Disabling 'Uninstall via DISM (All Users)' option.")
        return state

    def _update_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.basic_option_checkboxes):
            self.checkbox_basic_select_all.select()
        else:
            self.checkbox_basic_select_all.deselect()

    def _update_advanced_select_all_state(self):
        if all(cb.get() == 1 for cb in self.advanced_option_checkboxes):
            self.checkbox_advanced_select_all.select()
        else:
            self.checkbox_advanced_select_all.deselect()

    def _set_basic_row_enabled(self, enabled):
        if enabled:
            self.checkbox_basic_select_all.configure(state="normal")
            for cb in self.basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_basic_select_all.deselect()
            self.checkbox_basic_select_all.configure(state="disabled")
            for cb in self.basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _set_advanced_row_enabled(self, enabled):
        if enabled:
            self.checkbox_advanced_select_all.configure(state="normal")
            for cb in self.advanced_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_advanced_select_all.deselect()
            self.checkbox_advanced_select_all.configure(state="disabled")
            for cb in self.advanced_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _update_cleanup_options_state(self):
        if self.uninstall_image_var.get() == "offline_image":
            self.checkbox_basic_cleanup.deselect()
            self.checkbox_basic_cleanup.configure(state="disabled")
            self.checkbox_advanced_cleanup.deselect()
            self.checkbox_advanced_cleanup.configure(state="disabled")
            self._set_basic_row_enabled(False)
            self._set_advanced_row_enabled(False)
            return

        self.checkbox_basic_cleanup.configure(state="normal")
        self.checkbox_advanced_cleanup.configure(state="normal")

        self._set_basic_row_enabled(self.checkbox_basic_cleanup.get() == 1)
        self._set_advanced_row_enabled(self.checkbox_advanced_cleanup.get() == 1)

    def _on_basic_cleanup_toggle(self):
        self._update_cleanup_options_state()

    def _on_advanced_cleanup_toggle(self):
        self._update_cleanup_options_state()

    def _on_uninstall_image_change(self):
        self._update_cleanup_options_state()

    def _toggle_basic_select_all(self):
        state = self.checkbox_basic_select_all.get()
        for cb in self.basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_basic_select_all_state()

    def _toggle_advanced_select_all(self):
        state = self.checkbox_advanced_select_all.get()
        for cb in self.advanced_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_advanced_select_all_state()

    def _on_basic_option_change(self):
        self._update_basic_select_all_state()

    def _on_advanced_option_change(self):
        self._update_advanced_select_all_state()

    def _run_uninstall_via_dism_all_users(self):
        self.uninstall_via_dism_all_users_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.checkbox_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.checkbox_basic_registries.get() == 1,
            "basic_cache_files": self.checkbox_basic_cache_files.get() == 1,
            "advanced_app_package_data": self.checkbox_advanced_app_package_data.get() == 1,
            "advanced_registries": self.checkbox_advanced_registries.get() == 1
        }

        uninstaller = UninstallViaDISMForAllUsers(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            image_type=self.uninstall_image_var.get(),
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            uninstaller.execute,
            "pages.uninstaller.uninstall_via_dism_all_users",
            on_completion=lambda: self.uninstall_via_dism_all_users_card.configure(
                state=self._update_uninstall_via_dism_all_users_state()
            )
        )
    # ~ End of Uninstall via DISM for All Users ~

    # ~ Uninstall via Windows PowerShell for All Users ~
    def _update_uninstall_via_powershell_all_users_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"]):
            state = "disabled"
            self.logger.warning("Windows PowerShell is not available. Disabling 'Uninstall via Windows PowerShell (All Users)' option.")
        return state

    def _update_powershell_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_basic_option_checkboxes):
            self.checkbox_powershell_basic_select_all.select()
        else:
            self.checkbox_powershell_basic_select_all.deselect()

    def _update_powershell_advanced_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_advanced_option_checkboxes):
            self.checkbox_powershell_advanced_select_all.select()
        else:
            self.checkbox_powershell_advanced_select_all.deselect()

    def _set_powershell_basic_row_enabled(self, enabled):
        if enabled:
            self.checkbox_powershell_basic_select_all.configure(state="normal")
            for cb in self.powershell_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_powershell_basic_select_all.deselect()
            self.checkbox_powershell_basic_select_all.configure(state="disabled")
            for cb in self.powershell_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _set_powershell_advanced_row_enabled(self, enabled):
        if enabled:
            self.checkbox_powershell_advanced_select_all.configure(state="normal")
            for cb in self.powershell_advanced_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_powershell_advanced_select_all.deselect()
            self.checkbox_powershell_advanced_select_all.configure(state="disabled")
            for cb in self.powershell_advanced_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _update_powershell_cleanup_options_state(self):
        self.checkbox_powershell_basic_cleanup.configure(state="normal")
        self.checkbox_powershell_advanced_cleanup.configure(state="normal")

        self._set_powershell_basic_row_enabled(self.checkbox_powershell_basic_cleanup.get() == 1)
        self._set_powershell_advanced_row_enabled(self.checkbox_powershell_advanced_cleanup.get() == 1)

    def _on_powershell_basic_cleanup_toggle(self):
        self._update_powershell_cleanup_options_state()

    def _on_powershell_advanced_cleanup_toggle(self):
        self._update_powershell_cleanup_options_state()

    def _toggle_powershell_basic_select_all(self):
        state = self.checkbox_powershell_basic_select_all.get()
        for cb in self.powershell_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_powershell_basic_select_all_state()

    def _toggle_powershell_advanced_select_all(self):
        state = self.checkbox_powershell_advanced_select_all.get()
        for cb in self.powershell_advanced_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_powershell_advanced_select_all_state()

    def _on_powershell_basic_option_change(self):
        self._update_powershell_basic_select_all_state()

    def _on_powershell_advanced_option_change(self):
        self._update_powershell_advanced_select_all_state()

    def _run_uninstall_via_powershell_all_users(self):
        self.uninstall_via_powershell_all_users_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.checkbox_powershell_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.checkbox_powershell_basic_registries.get() == 1,
            "basic_cache_files": self.checkbox_powershell_basic_cache_files.get() == 1,
            "advanced_app_package_data": self.checkbox_powershell_advanced_app_package_data.get() == 1,
            "advanced_registries": self.checkbox_powershell_advanced_registries.get() == 1
        }

        uninstaller = UninstallViaPowerShellForAllUsers(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            uninstaller.execute,
            "pages.uninstaller.uninstall_via_powershell_all_users",
            on_completion=lambda: self.uninstall_via_powershell_all_users_card.configure(
                state=self._update_uninstall_via_powershell_all_users_state()
            )
        )
    # ~ End of Uninstall via Windows PowerShell for All Users ~

    # ~ Uninstall via Windows PowerShell for Current User ~
    def _update_uninstall_via_powershell_current_user_state(self):
        state = "normal" if AdvancedStartup.is_administrator() else "disabled"
        if not OptionalChecks.check_windows_utilities_availability(target_utility=["powershell.exe"]):
            state = "disabled"
            self.logger.warning("Windows PowerShell is not available. Disabling 'Uninstall via Windows PowerShell (Current User)' option.")
        return state

    def _update_powershell_current_user_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.powershell_current_user_basic_option_checkboxes):
            self.checkbox_powershell_current_user_basic_select_all.select()
        else:
            self.checkbox_powershell_current_user_basic_select_all.deselect()

    def _set_powershell_current_user_basic_row_enabled(self, enabled):
        if enabled:
            self.checkbox_powershell_current_user_basic_select_all.configure(state="normal")
            for cb in self.powershell_current_user_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_powershell_current_user_basic_select_all.deselect()
            self.checkbox_powershell_current_user_basic_select_all.configure(state="disabled")
            for cb in self.powershell_current_user_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _update_powershell_current_user_cleanup_options_state(self):
        self.checkbox_powershell_current_user_basic_cleanup.configure(state="normal")
        self._set_powershell_current_user_basic_row_enabled(self.checkbox_powershell_current_user_basic_cleanup.get() == 1)

    def _on_powershell_current_user_basic_cleanup_toggle(self):
        self._update_powershell_current_user_cleanup_options_state()

    def _toggle_powershell_current_user_basic_select_all(self):
        state = self.checkbox_powershell_current_user_basic_select_all.get()
        for cb in self.powershell_current_user_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_powershell_current_user_basic_select_all_state()

    def _on_powershell_current_user_basic_option_change(self):
        self._update_powershell_current_user_basic_select_all_state()

    def _run_uninstall_via_powershell_current_user(self):
        self.uninstall_via_powershell_current_user_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.checkbox_powershell_current_user_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.checkbox_powershell_current_user_basic_registries.get() == 1,
            "basic_cache_files": self.checkbox_powershell_current_user_basic_cache_files.get() == 1
        }

        uninstaller = UninstallViaPowerShellForCurrentUser(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            uninstaller.execute,
            "pages.uninstaller.uninstall_via_powershell_current_user",
            on_completion=lambda: self.uninstall_via_powershell_current_user_card.configure(
                state=self._update_uninstall_via_powershell_current_user_state()
            )
        )
    # ~ End of Uninstall via Windows PowerShell for Current User ~

    # ~ Uninstall Beta ~
    @staticmethod
    def _update_uninstall_beta_state():
        return "normal" if AdvancedStartup.is_administrator() else "disabled"

    def _update_beta_basic_select_all_state(self):
        if all(cb.get() == 1 for cb in self.beta_basic_option_checkboxes):
            self.checkbox_beta_basic_select_all.select()
        else:
            self.checkbox_beta_basic_select_all.deselect()

    def _set_beta_basic_row_enabled(self, enabled):
        if enabled:
            self.checkbox_beta_basic_select_all.configure(state="normal")
            for cb in self.beta_basic_option_checkboxes:
                cb.configure(state="normal")
        else:
            self.checkbox_beta_basic_select_all.deselect()
            self.checkbox_beta_basic_select_all.configure(state="disabled")
            for cb in self.beta_basic_option_checkboxes:
                cb.deselect()
                cb.configure(state="disabled")

    def _update_beta_cleanup_options_state(self):
        self.checkbox_beta_basic_cleanup.configure(state="normal")
        self._set_beta_basic_row_enabled(self.checkbox_beta_basic_cleanup.get() == 1)

    def _on_beta_basic_cleanup_toggle(self):
        self._update_beta_cleanup_options_state()

    def _toggle_beta_basic_select_all(self):
        state = self.checkbox_beta_basic_select_all.get()
        for cb in self.beta_basic_option_checkboxes:
            if state:
                cb.select()
            else:
                cb.deselect()
        self._update_beta_basic_select_all_state()

    def _on_beta_basic_option_change(self):
        self._update_beta_basic_select_all_state()

    def _run_uninstall_beta(self):
        self.uninstall_beta_card.configure(state="disabled")
        self.update_idletasks()

        selected_cleanup_options = {
            "basic_config_cache_dirs": self.checkbox_beta_basic_config_cache_dirs.get() == 1,
            "basic_registries": self.checkbox_beta_basic_registries.get() == 1,
            "basic_cache_files": self.checkbox_beta_basic_cache_files.get() == 1
        }

        uninstaller = UninstallBeta(
            logger=self.logger,
            app_translator=self.app_translator,
            log_callback=self.events_textbox.log_to_events,
            selected_cleanup_options=selected_cleanup_options
        )

        self._run_operation(
            uninstaller.execute,
            "pages.uninstaller.uninstall_beta",
            on_completion=lambda: self.uninstall_beta_card.configure(
                state=self._update_uninstall_beta_state()
            )
        )
    # ~ End of Uninstall Beta ~
