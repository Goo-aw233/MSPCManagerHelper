import ctypes
import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from tkinter import BooleanVar, messagebox, ttk

from core.advanced_startup import AdvancedStartup
from core.check_system_requirements import CheckSystemRequirements
from core.get_microsoft_pc_manager_version_number import GetMicrosoftPCManagerVersionNumber
from core.program_logger import ProgramLogger
from core.program_settings import ProgramSettings
from gui.widgets.scrollable_frame import ScrollableFrame


class HomePage(ttk.Frame):
    def __init__(self, parent, translator, font_family):
        super().__init__(parent)
        self.translator = translator
        self.font_family = font_family
        self.logger = ProgramLogger.get_logger()

        self.create_widgets()
        self.logger.info("Home Page initialized.")

    def create_widgets(self):
        # Configure style for LabelFrame's label.
        style = ttk.Style(self)
        style.configure("TLabelframe.Label", font=(self.font_family, 10, "bold"))

        # Use the theme background so the canvas matches the rest of UI.
        frame_bg = style.lookup("TFrame", "background") or self.cget("background")
        # text_fg = style.lookup("TLabel", "foreground") or "#000000"

        # Page-level Scrollable Frame (Shared Component)
        scrollable = ScrollableFrame(self, bg=frame_bg)
        scrollable.pack(fill="both", expand=True)
        content_frame = scrollable.content_frame

        # Home Page Title
        title_label = ttk.Label(content_frame, text=self.translator.translate("home_page"),
                                font=(self.font_family, 16, "bold"))
        title_label.pack(pady=10)

        # ======================= Introduction Frame Section =======================
        # Introduction Frame
        introduction_frame = ttk.LabelFrame(
            content_frame,
            text=self.translator.translate("introduction"),
            padding=10
        )
        introduction_frame.pack(fill="x", padx=10, pady=5)

        # Introduction Text Label
        intro_text = self.translator.translate("home_page_introduction")
        intro_label = ttk.Label(
            introduction_frame,
            text=intro_text,
            font=(self.font_family, 10),
            justify="left"
        )
        intro_label.pack(anchor="w", fill="x", padx=(8, 6))

        def _update_intro_wrap(e):
            wrap = max(30, e.width - 20)
            intro_label.config(wraplength=wrap)
        introduction_frame.bind("<Configure>", _update_intro_wrap)
        # ======================= End of Introduction Frame Section =======================

        # ======================= Microsoft PC Manager Version Information Frame Section =======================
        # Microsoft PC Manager Version Information Frame
        mspcm_version_frame = ttk.LabelFrame(
            content_frame,
            text=self.translator.translate("microsoft_pc_manager_version_infomation"),
            padding=10
        )
        mspcm_version_frame.pack(fill="x", padx=10, pady=5)

        # --- Row: Microsoft PC Manager Version Text Label ---
        show_mspcm_version_frame = ttk.Frame(mspcm_version_frame)
        show_mspcm_version_frame.pack(anchor="w", fill="x")
        show_mspcm_version_frame.grid_columnconfigure(0, weight=1)

        version_label = ttk.Label(
            show_mspcm_version_frame,
            text="",
            font=(self.font_family, 10),
            justify="left"
        )
        version_label.grid(row=0, column=0, sticky="we", padx=(8, 6))

        # --- Row: Action Buttons ---
        action_buttons_frame = ttk.Frame(mspcm_version_frame)
        action_buttons_frame.pack(anchor="w", fill="x", pady=(5, 0))

        start_mspcm_button = ttk.Button(action_buttons_frame, text=self.translator.translate("start_microsoft_pc_manager"), style="Accent.TButton")
        start_mspcm_beta_button = ttk.Button(action_buttons_frame, text=self.translator.translate("start_microsoft_pc_manager_beta"))

        def _on_start_mspcm_click():
            registered_class = "shell:AppsFolder\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe!App"

            try:
                os.startfile(registered_class)
                self.logger.info(f"Successfully Started Microsoft PC Manager Via os.startfile: {registered_class}")
            except Exception as e_os:
                self.logger.warning(f"Failed to start via os.startfile: {e_os}. Trying CMD fallback...")
                try:
                    subprocess.run(["cmd.exe", "/C", "start", "Start Microsoft PC Manager", f"{registered_class}"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    self.logger.info(f"Successfully Started Microsoft PC Manager Via CMD: {registered_class}")
                except Exception as e_cmd:
                    self.logger.warning(f"Failed to start Microsoft PC Manager via CMD: {e_cmd}. Trying Windows PowerShell fallback...")
                    try:
                        subprocess.run(
                            ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{registered_class}'"],
                            check=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        self.logger.info(f"Successfully Started Microsoft PC Manager Via Windows PowerShell: {registered_class}")
                    except Exception as e_windows_powershell:
                        self.logger.warning(f"Failed to start Microsoft PC Manager via Windows PowerShell: {e_windows_powershell}. Trying webbrowser fallback...")
                        try:
                            webbrowser.open(registered_class)
                            self.logger.info(f"Successfully Started Microsoft PC Manager Via webbrowser: {registered_class}")
                        except Exception as e_webbrowser:
                            self.logger.error(f"Failed to start Microsoft PC Manager. Error: {e_webbrowser}")

        def _on_start_mspcm_beta_click():
            registered_class_beta = "shell:AppsFolder\\Microsoft.AutoGenerated.{CDBC7B0D-6A70-5A10-4C8A-4B161DDC42A7}"
            beta_exe_path = Path(os.environ["ProgramFiles"]) / "Microsoft PC Manager" / "MSPCManager.exe"

            try:
                os.startfile(registered_class_beta)
                self.logger.info(f"Successfully Started Microsoft PC Manager Public Beta Via os.startfile: {registered_class_beta}")
            except Exception as e_os:
                self.logger.warning(f"Failed to start via os.startfile: {e_os}. Trying CMD fallback...")
                try:
                    subprocess.run(["cmd.exe", "/C", "start", "Start Microsoft PC Manager Public Beta", f"{registered_class_beta}"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    self.logger.info(f"Successfully Started Microsoft PC Manager Public Beta Via CMD: {registered_class_beta}")
                except Exception as e_cmd:
                    self.logger.warning(f"Failed to start Microsoft PC Manager Public Beta via CMD: {e_cmd}. Trying Windows PowerShell fallback...")
                    try:
                        subprocess.run(
                            ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{registered_class_beta}'"],
                            check=True,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        self.logger.info(f"Successfully Started Microsoft PC Manager Public Beta Via Windows PowerShell: {registered_class_beta}")
                    except Exception as e_windows_powershell:
                        self.logger.warning(f"Failed to start Microsoft PC Manager Public Beta via Windows PowerShell: {e_windows_powershell}. Trying webbrowser fallback...")
                        try:
                            webbrowser.open(registered_class_beta)
                            self.logger.info(f"Successfully Started Microsoft PC Manager Public Beta Via webbrowser: {registered_class_beta}")
                        except Exception as e_webbrowser:
                            self.logger.error(f"Failed to start Microsoft PC Manager Public Beta. Error: {e_webbrowser}")

        start_mspcm_button = ttk.Button(
            action_buttons_frame,
            text=self.translator.translate("start_microsoft_pc_manager"),
            command=_on_start_mspcm_click,
            style="Accent.TButton"
        )
        start_mspcm_beta_button = ttk.Button(
            action_buttons_frame,
            text=self.translator.translate("start_microsoft_pc_manager_beta"),
            command=_on_start_mspcm_beta_click
        )

        def _update_mspcm_version_info():
            version_number = GetMicrosoftPCManagerVersionNumber().get_microsoft_pc_manager_version_number()
            beta_version_number = GetMicrosoftPCManagerVersionNumber().get_microsoft_pc_manager_beta_version_number()

            # Reset Buttons and Frame
            start_mspcm_button.pack_forget()
            start_mspcm_beta_button.pack_forget()
            action_buttons_frame.pack_forget()  # Hide the button container to eliminate empty space.

            # Release & Beta Version
            if version_number and beta_version_number:
                version_text = (f"{self.translator.translate('current_microsoft_pc_manager_version_number')}: {version_number}\n"
                                f"{self.translator.translate('current_microsoft_pc_manager_beta_version_number')}: {beta_version_number}")
                self.logger.info(f"Microsoft PC Manager Version: {version_number}, Public Beta Version: {beta_version_number}")
                
                action_buttons_frame.pack(anchor="w", fill="x", pady=(5, 0))    # Display button container.
                start_mspcm_button.pack(side="left", padx=(8, 5))
                start_mspcm_beta_button.pack(side="left", padx=(0, 8))

            # Release Version
            elif version_number:
                version_text = f"{self.translator.translate('current_microsoft_pc_manager_version_number')}: {version_number}"
                self.logger.info(f"Microsoft PC Manager Version: {version_number}")
                
                action_buttons_frame.pack(anchor="w", fill="x", pady=(5, 0))    # Display button container.
                start_mspcm_button.pack(side="left", padx=(8, 8))

            # Beta Version
            elif beta_version_number:
                version_text = f"{self.translator.translate('current_microsoft_pc_manager_beta_version_number')}: {beta_version_number}"
                self.logger.info(f"Microsoft PC Manager Public Beta Version: {beta_version_number}")
                
                action_buttons_frame.pack(anchor="w", fill="x", pady=(5, 0))    # Display button container.
                start_mspcm_beta_button.pack(side="left", padx=(8, 8))

            # Failed to Get Any Version
            else:
                version_text = self.translator.translate("failed_to_get_microsoft_pc_manager_version_number")
            version_label.config(text=version_text)

        # Initial update of version info.
        _update_mspcm_version_info()

        def _on_refresh_button_click():
            _update_mspcm_version_info()
            self.logger.info("Microsoft PC Manager Version has been refreshed.")

        # Refresh Button
        refresh_button = ttk.Button(
            show_mspcm_version_frame,
            text=self.translator.translate("refresh"),
            command=_on_refresh_button_click
        )
        refresh_button.grid(row=0, column=1, padx=(0, 8))

        def _update_version_wrap(e):
            # Subtract extra space for the button (approx 100px).
            wrap = max(20, e.width - 120)
            version_label.config(wraplength=wrap)
        show_mspcm_version_frame.bind("<Configure>", _update_version_wrap)
        # ======================= End of Microsoft PC Manager Version Information Frame Section =======================

        # ======================= Check System Requirements Frame Section =======================
        # Check System Requirements Frame
        check_system_requirements_frame = ttk.LabelFrame(
            content_frame,
            text=self.translator.translate("check_system_requirements"),
            padding=10
        )
        check_system_requirements_frame.pack(fill="x", padx=10, pady=5)

        # --- Row: Compatibility Check Label ---
        is_compatible = CheckSystemRequirements.check_system_minimum_requirements()
        if is_compatible:
            compatibility_check_text = self.translator.translate("current_system_meet_system_requirements")
            self.logger.info("The current system meets the minimum system requirements for Microsoft PC Manager.")
        else:
            compatibility_check_text = self.translator.translate("current_system_not_meet_system_requirements")
            self.logger.warning("The current system does not meet the minimum system requirements for Microsoft PC Manager.")

        compatibility_check_label = ttk.Label(
            check_system_requirements_frame,
            text=compatibility_check_text,
            font=(self.font_family, 10),
            justify="left"
        )
        compatibility_check_label.pack(anchor="w", padx=5, pady=5)

        # --- Row: Check Windows Server Levels Label ---
        is_server_core = CheckSystemRequirements.check_windows_server_levels()
        server_level_label = None
        if is_server_core:
            server_level_text = self.translator.translate("windows_server_installation_type_is_core")
            server_level_label = ttk.Label(
                check_system_requirements_frame,
                text=server_level_text,
                font=(self.font_family, 10),
                justify="left"
            )
            server_level_label.pack(anchor="w", padx=5, pady=5)

        # --- Row: Check Admin Approval Mode Label ---
        is_admin_approval_mode = CheckSystemRequirements.check_admin_approval_mode()
        admin_approval_mode_label = None
        if is_admin_approval_mode:
            admin_approval_mode_label = ttk.Label(
                check_system_requirements_frame,
                text=self.translator.translate("administrator_protection_is_enabled"),
                font=(self.font_family, 10),
                justify="left"
            )
            admin_approval_mode_label.pack(anchor="w", padx=5, pady=5)

        # --- Row: Windows Installation Information Label ---
        windows_installation_info = CheckSystemRequirements.get_windows_installation_information()
        if windows_installation_info:
            windows_info_frame = ttk.Frame(check_system_requirements_frame)
            windows_info_frame.pack(fill="x", padx=5, pady=5)
            windows_info_frame.grid_columnconfigure(0, weight=1)

            windows_installation_info_label = ttk.Label(
                windows_info_frame,
                text=f"{self.translator.translate('windows_installation_information')}:\n{windows_installation_info}",
                font=(self.font_family, 10),
                justify="left"
            )
            windows_installation_info_label.grid(row=0, column=0, sticky="we")

            def _on_about_windows_click():
                about_windows_uri = "ms-settings:about"
                try:
                    os.startfile(about_windows_uri)
                    self.logger.info(f"Successfully opened {about_windows_uri} via os.startfile.")
                except Exception as e_os:
                    self.logger.warning(f"Failed to open {about_windows_uri} via os.startfile: {e_os}. Trying CMD fallback...")
                    try:
                        subprocess.run(["cmd.exe", "/C", "start", "About Windows", about_windows_uri], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        self.logger.info(f"Successfully opened {about_windows_uri} via CMD.")
                    except Exception as e_cmd:
                        self.logger.warning(f"Failed to open {about_windows_uri} via CMD: {e_cmd}. Trying Windows PowerShell fallback...")
                        try:
                            subprocess.run(
                                ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{about_windows_uri}'"],
                                check=True,
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                            self.logger.info(f"Successfully opened {about_windows_uri} via Windows PowerShell.")
                        except Exception as e_windows_powershell:
                            self.logger.warning(f"Failed to open {about_windows_uri} via Windows PowerShell: {e_windows_powershell}. Trying webbrowser fallback...")
                            try:
                                webbrowser.open(about_windows_uri)
                                self.logger.info(f"Successfully opened {about_windows_uri} via webbrowser.")
                            except Exception as e_webbrowser:
                                self.logger.error(f"Failed to open {about_windows_uri}. Error: {e_webbrowser}")

            about_windows_button = ttk.Button(
                windows_info_frame,
                text=self.translator.translate("about_windows_in_mssettings"),
                command=_on_about_windows_click
            )
            about_windows_button.grid(row=0, column=1, padx=(10, 0))

            def _update_windows_info_wrap(e):
                wrap = max(20, e.width - 120)
                windows_installation_info_label.config(wraplength=wrap)
            windows_info_frame.bind("<Configure>", _update_windows_info_wrap)

        def _update_requirements_wrap(e):
            wrap = max(30, e.width - 20)
            compatibility_check_label.config(wraplength=wrap)
            if server_level_label:
                server_level_label.config(wraplength=wrap)
            if admin_approval_mode_label:
                admin_approval_mode_label.config(wraplength=wrap)
        check_system_requirements_frame.bind("<Configure>", _update_requirements_wrap)
        # ======================= End of Check System Requirements Frame Section =======================

        # ======================= Program Settings Frame Section =======================
        # Program Settings Frame
        program_settings_frame = ttk.LabelFrame(
            content_frame,
            text=self.translator.translate("program_settings"),
            padding=10
        )
        program_settings_frame.pack(fill="x", padx=10, pady=5)

        # --- Row: Run as Administrator ---
        run_as_admin_frame = ttk.Frame(program_settings_frame)
        run_as_admin_frame.pack(fill="x", padx=5, pady=5)
        run_as_admin_frame.grid_columnconfigure(0, weight=1)

        run_as_admin_desc_label = ttk.Label(
            run_as_admin_frame,
            text=self.translator.translate("run_as_administrator_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        run_as_admin_desc_label.grid(row=0, column=0, sticky="w")

        def _restart_as_administrator():
            if AdvancedStartup.is_administrator():
                self.logger.info("Already running as administrator, no action taken.")
                return

            # Determine the original launch path (exe/script).
            boot_file_path = str(Path(sys.argv[0]).resolve())
            self.logger.debug(f"Determined Boot File Path: {boot_file_path}")

            original_args = AdvancedStartup.get_runtime_arguments()
            params_list = [f'"{boot_file_path}"'] + [f'"{arg}"' if " " in arg else arg for arg in original_args]

            formatted_original_args = [
                f'"{arg}"' if " " in arg else arg for arg in original_args
            ]

            params_list = [f'"{boot_file_path}"'] + formatted_original_args
            params_str = " ".join(params_list)
            self.logger.info(f"Attempting to restart as administrator. Executable: {boot_file_path}; Params: {params_str}")

            try:
                result = AdvancedStartup.run_as_administrator(params_str)
                if not result:
                    failed_code = ctypes.get_last_error()
                    failed_msg = ctypes.FormatError(failed_code).strip()
                    self.logger.error(
                        f"Failed to request elevation (ShellExecute returned failure). "
                        f"ErrorCode={failed_code}; Message={failed_msg}"
                    )
                    messagebox.showerror(
                        self.translator.translate("error"),
                        f"{self.translator.translate('failed_to_run_as_administrator')}\n"
                        f"{self.translator.translate('error_code')}: {failed_code}\n"
                        f"{self.translator.translate('error_message')}: {failed_msg}"
                    )
                else:
                    self.logger.info("Elevation request succeeded (process elevated or ShellExecute triggered).")
            except Exception as e:
                self.logger.exception("Exception while attempting to restart as administrator.")
                failed_code = ctypes.get_last_error()
                failed_msg = ctypes.FormatError(failed_code).strip()
                messagebox.showerror(
                    self.translator.translate("error"),
                    f"{self.translator.translate('failed_to_run_as_administrator')}\n"
                    f"{self.translator.translate('error_code')}: {failed_code}\n"
                    f"{self.translator.translate('error_message')}: {failed_msg}"
                )

        is_admin = AdvancedStartup.is_administrator()

        run_as_admin_button = ttk.Button(
            run_as_admin_frame,
            text=self.translator.translate("run_as_administrator"),
            style="Accent.TButton",
            command=_restart_as_administrator,
            state="disabled" if is_admin else "normal"
        )
        run_as_admin_button.grid(row=0, column=1, sticky="e", padx=(10, 0))

        def _update_run_as_admin_desc_wrap(e):
            try:
                button_width = run_as_admin_button.winfo_width() or run_as_admin_button.winfo_reqwidth()
            except Exception:
                button_width = 120
            padding = 30
            wrap = max(30, e.width - button_width - padding)
            run_as_admin_desc_label.config(wraplength=wrap)

        run_as_admin_frame.bind("<Configure>", _update_run_as_admin_desc_wrap)

        # --- Row: Switch Program Language ---

        # --- Row: Switch Program Theme ---

        # --- Row: Support Developer ---
        support_developer_frame = ttk.Frame(program_settings_frame)
        support_developer_frame.pack(fill="x", padx=5, pady=5)

        support_developer_desc_label = ttk.Label(
            support_developer_frame,
            text=self.translator.translate("support_developer_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        support_developer_desc_label.grid(row=0, column=0, sticky="w")

        # Support Developer
        self.support_developer_var = BooleanVar(value=ProgramSettings.is_support_developer_enabled())

        def _on_toggle_support_developer():
            try:
                new_state = self.support_developer_var.get()
                ProgramSettings.set_support_developer_enabled(new_state)
                self.logger.info(f"Support Developer Setting Set to: {new_state}")
            except Exception as e:
                self.logger.exception(f"Failed to Set Support Developer: {e}")

        style.configure("Big.TCheckbutton", font=(self.font_family, 10))
        support_developer_checkbutton = ttk.Checkbutton(
            support_developer_frame,
            text=self.translator.translate("support_developer"),
            variable=self.support_developer_var,
            style="Big.TCheckbutton",
            command=_on_toggle_support_developer
        )
        support_developer_checkbutton.grid(row=0, column=1, sticky="e", padx=(10, 0))
        support_developer_frame.grid_columnconfigure(0, weight=1)

        def _update_support_developer_desc_wrap(e):
            try:
                checkbox_width = support_developer_checkbutton.winfo_width() or support_developer_checkbutton.winfo_reqwidth()
            except Exception:
                checkbox_width = 120
            padding = 30
            wrap = max(30, e.width - checkbox_width - padding)
            support_developer_desc_label.config(wraplength=wrap)

        support_developer_frame.bind("<Configure>", _update_support_developer_desc_wrap)

        # --- Row: Compatibility Mode ---
        compatibility_mode_frame = ttk.Frame(program_settings_frame)
        compatibility_mode_frame.pack(fill="x", padx=5, pady=5)

        compatibility_mode_desc_label = ttk.Label(
            compatibility_mode_frame,
            text=self.translator.translate("compatibility_mode_description"),
            font=(self.font_family, 10),
            justify="left"
        )
        compatibility_mode_desc_label.grid(row=0, column=0, sticky="w")

        # Compatibility Mode
        self.compatibility_mode_var = BooleanVar(value=ProgramSettings.is_compatibility_mode_enabled())

        def _on_toggle_compatibility_mode():
            try:
                new_state = self.compatibility_mode_var.get()
                ProgramSettings.set_compatibility_mode_enabled(new_state)
                self.logger.info(f"Compatibility Mode Setting Set to: {new_state}")
            except Exception as e:
                self.logger.exception(f"Failed to Set Compatibility Mode: {e}")

        style.configure("Big.TCheckbutton", font=(self.font_family, 10))
        compatibility_mode_checkbutton = ttk.Checkbutton(
            compatibility_mode_frame,
            text=self.translator.translate("compatibility_mode"),
            variable=self.compatibility_mode_var,
            style="Big.TCheckbutton",
            command=_on_toggle_compatibility_mode
        )
        compatibility_mode_checkbutton.grid(row=0, column=1, sticky="e", padx=(10, 0))
        compatibility_mode_frame.grid_columnconfigure(0, weight=1)

        def _update_compatibility_mode_desc_wrap(e):
            try:
                checkbox_width = compatibility_mode_checkbutton.winfo_width() or compatibility_mode_checkbutton.winfo_reqwidth()
            except Exception:
                checkbox_width = 120
            padding = 30
            wrap = max(30, e.width - checkbox_width - padding)
            compatibility_mode_desc_label.config(wraplength=wrap)

        compatibility_mode_frame.bind("<Configure>", _update_compatibility_mode_desc_wrap)
        # ======================= End of Program Settings Frame Section =======================
