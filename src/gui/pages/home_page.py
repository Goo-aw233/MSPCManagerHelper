import ctypes
import customtkinter
import os
import subprocess
import sys
import threading
from tkinter import messagebox
from ..modules import AdvancedStartup, CheckSystemRequirements, GetMicrosoftPCManagerVersionNumber, ProgramSettings


class HomePageFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font_family=None, translator=None, change_language_callback=None, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, *args, **kwargs)
        self.font_family = font_family
        self.translator = translator
        self.change_language_callback = change_language_callback

        # 配置网格权重
        self.grid_columnconfigure(0, weight=1)
        # 初始化主框架的行计数器
        current_row = 0

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.translator.translate("home_page"),
            font=(self.font_family, 20, "bold")
        )
        self.title_label.grid(row=current_row, column=0, pady=(20, 10), sticky="ew")
        self.title_label.bind("<Configure>", lambda event: self.title_label.configure(
            wraplength=self.title_label.winfo_width() - 20))
        current_row += 1

        # Welcome Message Frame
        self.welcome_message_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.welcome_message_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.welcome_message_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        current_row_in_welcome_message_frame = 0
        self.welcome_title_label = customtkinter.CTkLabel(
            self.welcome_message_frame,
            text=self.translator.translate("introduction"),
            font=(self.font_family, 16, "bold")
        )
        self.welcome_title_label.grid(row=current_row_in_welcome_message_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.welcome_title_label.bind("<Configure>", lambda event: self.welcome_title_label.configure(
            wraplength=self.welcome_message_frame.winfo_width() - 20))
        current_row_in_welcome_message_frame += 1

        # Welcome Message
        self.welcome_label = customtkinter.CTkLabel(
            self.welcome_message_frame,
            text=self.translator.translate("welcome_message"),
            font=(self.font_family, 12)
        )
        self.welcome_label.grid(row=current_row_in_welcome_message_frame, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.welcome_label.bind("<Configure>", lambda event: self.welcome_label.configure(
            wraplength=self.welcome_message_frame.winfo_width() - 20))
        current_row_in_welcome_message_frame += 1

        # Microsoft PC Manager Information Frame
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.info_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        current_row_in_info_frame = 0
        self.info_title_label = customtkinter.CTkLabel(
            self.info_frame,
            text=self.translator.translate("microsoft_pc_manager_information"),
            font=(self.font_family, 16, "bold")
        )
        self.info_title_label.grid(row=current_row_in_info_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.info_title_label.bind("<Configure>", lambda event: self.info_title_label.configure(
            wraplength=self.info_frame.winfo_width() - 20))
        current_row_in_info_frame += 1

        # Microsoft PC Manager Version Number
        version_number = GetMicrosoftPCManagerVersionNumber().get_microsoft_pc_manager_version_number()
        if version_number:  # Successfully Read the Version Number
            version_text = (f"{self.translator.translate('current_microsoft_pc_manager_version_number')}: "
                            f"{version_number}")
            self.microsoft_pc_manager_version_label = customtkinter.CTkLabel(
                self.info_frame,
                text=version_text,
                font=(self.font_family, 12)
            )
            self.microsoft_pc_manager_version_label.grid(row=current_row_in_info_frame, column=0, padx=10,
                                                         pady=5, sticky="ew")
            self.microsoft_pc_manager_version_label.bind("<Configure>", lambda
                event: self.microsoft_pc_manager_version_label.configure(
                wraplength=self.info_frame.winfo_width() - 20))
            current_row_in_info_frame += 1

            # Start Microsoft PC Manager Button
            self.start_microsoft_pc_manager_button = customtkinter.CTkButton(
                self.info_frame,
                text=self.translator.translate("start_microsoft_pc_manager"),
                font=(self.font_family, 12),
                command=self._start_microsoft_pc_manager
            )
            self.start_microsoft_pc_manager_button.grid(row=current_row_in_info_frame, column=0, padx=20,
                                                        pady=(5, 10), sticky="ew")
            current_row_in_info_frame += 1
        else:  # Failed to Read the Version Number
            version_text = self.translator.translate('failure_to_read_microsoft_pc_manager_version_number')
            self.microsoft_pc_manager_version_label = customtkinter.CTkLabel(
                self.info_frame,
                text=version_text,
                font=(self.font_family, 12)
            )
            self.microsoft_pc_manager_version_label.grid(row=current_row_in_info_frame, column=0, padx=10,
                                                         pady=5, sticky="ew")
            self.microsoft_pc_manager_version_label.bind("<Configure>", lambda
                event: self.microsoft_pc_manager_version_label.configure(
                wraplength=self.info_frame.winfo_width() - 20))
            current_row_in_info_frame += 1

        # Microsoft PC Manager Beta Version Number
        beta_version_number = GetMicrosoftPCManagerVersionNumber().get_microsoft_pc_manager_beta_version_number()
        if beta_version_number:  # If beta_version_number is None, Nothing is Displayed
            beta_version_text = (f"{self.translator.translate('current_microsoft_pc_manager_beta_version_number')}: "
                                 f"{beta_version_number}")
            self.microsoft_pc_manager_beta_version_label = customtkinter.CTkLabel(
                self.info_frame,
                text=beta_version_text,
                font=(self.font_family, 12)
            )
            self.microsoft_pc_manager_beta_version_label.grid(row=current_row_in_info_frame, column=0,
                                                              padx=10, pady=5, sticky="ew")
            self.microsoft_pc_manager_beta_version_label.bind("<Configure>", lambda
                event: self.microsoft_pc_manager_beta_version_label.configure(
                wraplength=self.info_frame.winfo_width() - 20))
            current_row_in_info_frame += 1

            # Start Microsoft PC Manager Beta Button
            self.start_microsoft_pc_manager_beta_button = customtkinter.CTkButton(
                self.info_frame, fg_color="transparent", border_width=2,
                text_color=("gray10", "#DCE4EE"),
                text=self.translator.translate("start_microsoft_pc_manager_beta"),
                font=(self.font_family, 12),
                command=self._start_microsoft_pc_manager_beta
            )
            self.start_microsoft_pc_manager_beta_button.grid(row=current_row_in_info_frame, column=0,
                                                             padx=20, pady=(5, 10), sticky="ew")
            current_row_in_info_frame += 1

        # Check System Requirements Frame
        self.check_system_requirements_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.check_system_requirements_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.check_system_requirements_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        current_row_in_check_system_req_frame = 0
        self.check_system_requirements_title_label = customtkinter.CTkLabel(
            self.check_system_requirements_frame,
            text=self.translator.translate("system_requirements_check"),
            font=(self.font_family, 16, "bold")
        )
        self.check_system_requirements_title_label.grid(row=current_row_in_check_system_req_frame, column=0, padx=10, pady=(10, 5), sticky="w")
        self.check_system_requirements_title_label.bind("<Configure>", lambda event: self.check_system_requirements_title_label.configure(
            wraplength=self.check_system_requirements_frame.winfo_width() - 20))
        current_row_in_check_system_req_frame += 1

        # Check System Minimum Requirements
        system_requirements_status = CheckSystemRequirements().check_system_minimum_requirements()
        if system_requirements_status is True:
            requirements_text = self.translator.translate("meet_minimum_system_version_requirements")
        elif system_requirements_status is False:
            requirements_text = self.translator.translate("failure_to_meet_minimum_system_version_requirements")
        else:
            requirements_text = self.translator.translate("system_requirement_checks_cannot_be_completed_at_this_time")

        self.system_requirements_status_label = customtkinter.CTkLabel(
            self.check_system_requirements_frame,
            text=requirements_text,
            font=(self.font_family, 12)
        )
        self.system_requirements_status_label.grid(row=current_row_in_check_system_req_frame, column=0,
                                                   padx=10, pady=5, sticky="ew")
        self.system_requirements_status_label.bind("<Configure>", lambda
            event: self.system_requirements_status_label.configure(
            wraplength=self.check_system_requirements_frame.winfo_width() - 20))
        current_row_in_check_system_req_frame += 1

        # Check Windows Version
        windows_version = CheckSystemRequirements.get_windows_installation_information()

        if windows_version:
            self.windows_version_label = customtkinter.CTkLabel(
                self.check_system_requirements_frame,
                text=windows_version,
                font=(self.font_family, 12)
            )
            self.windows_version_label.grid(row=current_row_in_check_system_req_frame, column=0,
                                            padx=10,
                                            pady=5, sticky="ew")
            self.windows_version_label.bind("<Configure>", lambda
                event: self.windows_version_label.configure(
                wraplength=self.check_system_requirements_frame.winfo_width() - 20))
            current_row_in_check_system_req_frame += 1

        # Check Windows Server Levels
        windows_server_levels_status = CheckSystemRequirements().check_windows_server_levels()
        if windows_server_levels_status is True:
            windows_server_core_levels_prompt = self.translator.translate("windows_server_installation_type_is_core")
            self.windows_server_levels_status_label = customtkinter.CTkLabel(
                self.check_system_requirements_frame,
                text=windows_server_core_levels_prompt,
                font=(self.font_family, 12)
            )
            self.windows_server_levels_status_label.grid(row=current_row_in_check_system_req_frame, column=0,
                                                         padx=10,
                                                         pady=5, sticky="ew")
            self.windows_server_levels_status_label.bind("<Configure>", lambda
                event: self.windows_server_levels_status_label.configure(
                wraplength=self.check_system_requirements_frame.winfo_width() - 20))
            current_row_in_check_system_req_frame += 1

        # Check Admin Approval Mode
        admin_approval_status = CheckSystemRequirements().check_admin_approval_mode()
        if admin_approval_status is True:
            admin_approval_text = self.translator.translate("administrator_protection_is_enabled")
            self.admin_approval_status_label = customtkinter.CTkLabel(
                self.check_system_requirements_frame,
                text=admin_approval_text,
                font=(self.font_family, 12)
            )
            self.admin_approval_status_label.grid(row=current_row_in_check_system_req_frame, column=0, padx=10,
                                                  pady=5, sticky="ew")
            self.admin_approval_status_label.bind("<Configure>", lambda
                event: self.admin_approval_status_label.configure(
                wraplength=self.check_system_requirements_frame.winfo_width() - 20))
            current_row_in_check_system_req_frame += 1

        # Program Settings Frame
        self.program_settings_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.program_settings_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.program_settings_frame.grid_columnconfigure(1, weight=1)
        current_row += 1

        current_row_in_program_settings_frame = 0
        self.program_settings_title_label = customtkinter.CTkLabel(
            self.program_settings_frame,
            text=self.translator.translate("settings"),
            font=(self.font_family, 16, "bold")
        )
        self.program_settings_title_label.grid(row=current_row_in_program_settings_frame, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        self.program_settings_title_label.bind("<Configure>", lambda event: self.program_settings_title_label.configure(
            wraplength=self.program_settings_frame.winfo_width() - 20))
        current_row_in_program_settings_frame += 1

        # Run as Administrator Button
        self.run_as_administrator_button = customtkinter.CTkButton(
            self.program_settings_frame,
            text=self.translator.translate("run_as_administrator"),
            font=(self.font_family, 12),
            command=self._restart_as_administrator
        )
        self.run_as_administrator_button.grid(row=current_row_in_program_settings_frame, column=0, columnspan=2,
                                              padx=20, pady=(5, 5), sticky="ew")
        if AdvancedStartup.is_administrator():
            self.run_as_administrator_button.configure(state="disabled")
        current_row_in_program_settings_frame += 1

        # Language Selection OptionMenu
        self.language_selection_label = customtkinter.CTkLabel(self.program_settings_frame,
                                                               text=self.translator.translate("current_language"),
                                                               font=(self.font_family, 12)
                                                               )
        self.language_selection_label.grid(row=current_row_in_program_settings_frame, column=0, padx=(20, 5),
                                           pady=(5, 5), sticky="w")

        # 从翻译值动态构建语言菜单
        # 1. 定义语言代码到其翻译键的映射
        self.language_code_to_key_map = {
            "en-us": "lang_en-us",
            "zh-cn": "lang_zh-cn",
            "zh-tw": "lang_zh-tw"
        }

        # 2. 创建一个从翻译后的显示名称到语言代码的新映射，用于回调
        self.language_display_map = {
            self.translator.translate(key): code for code, key in self.language_code_to_key_map.items()
        }

        # 3. 获取当前语言的正确显示名称，用于设置默认值
        current_language_translation_key = self.language_code_to_key_map.get(self.translator.locale, "lang_en-us")
        current_language_display = self.translator.translate(current_language_translation_key)

        # 4. 创建 OptionMenu，值为翻译后的语言列表
        self.language_optionmenu = customtkinter.CTkOptionMenu(self.program_settings_frame,
                                                                    values=list(self.language_display_map.keys()),
                                                                    font=(self.font_family, 12),
                                                                    dropdown_font=(self.font_family, 12),
                                                                    command=self._change_language_event)
        self.language_optionmenu.set(current_language_display)
        self.language_optionmenu.grid(row=current_row_in_program_settings_frame, column=1, padx=(5, 20),
                                            pady=(5, 5), sticky="ew")
        current_row_in_program_settings_frame += 1

        # Appearance Mode OptionMenu
        self.appearance_mode_label = customtkinter.CTkLabel(self.program_settings_frame,
                                                            text=self.translator.translate("appearance_mode"),
                                                            font=(self.font_family, 12)
                                                            )
        self.appearance_mode_label.grid(row=current_row_in_program_settings_frame, column=0, padx=(20, 5),
                                        pady=(5, 5), sticky="w")

        # Define English to translated string mapping for Appearance Modes.
        self.appearance_mode_translations = {
            "Light": self.translator.translate("light_theme"),
            "Dark": self.translator.translate("dark_theme"),
            "System": self.translator.translate("follow_windows_theme")
        }

        # Values to display in the OptionMenu (translated).
        appearance_display_values = [
            self.appearance_mode_translations["Light"],
            self.appearance_mode_translations["Dark"],
            self.appearance_mode_translations["System"]
        ]

        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.program_settings_frame,
                                                                     values=appearance_display_values,
                                                                     font=(self.font_family, 12),
                                                                     dropdown_font=(self.font_family, 12),
                                                                     command=self._change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=current_row_in_program_settings_frame, column=1, padx=(5, 20),
                                              pady=(5, 5), sticky="ew")

        # Set default value based on current Appearance Mode.
        current_appearance_mode = customtkinter.get_appearance_mode()  # Returns "Light", "Dark", or "System"

        if current_appearance_mode == "Light":
            self.appearance_mode_optionmenu.set(self.appearance_mode_translations["Light"])
        elif current_appearance_mode == "Dark":
            self.appearance_mode_optionmenu.set(self.appearance_mode_translations["Dark"])
        else:  # System or other unexpected values.
            self.appearance_mode_optionmenu.set(self.appearance_mode_translations["System"])
        current_row_in_program_settings_frame += 1

        # Support Developer CheckBox
        self.support_developer_checkbox = customtkinter.CTkCheckBox(
            self.program_settings_frame,
            text=self.translator.translate("support_developer"),
            font=(self.font_family, 12),
            command=ProgramSettings.toggle_support_developer
        )
        if ProgramSettings.is_support_developer_enabled():
            self.support_developer_checkbox.select()
        else:
            self.support_developer_checkbox.deselect()
        self.support_developer_checkbox.grid(row=current_row_in_program_settings_frame, column=0, columnspan=2,
                                             padx=20,
                                             pady=(5, 10), sticky="w")
        current_row_in_program_settings_frame += 1

        # Compatibility Mode CheckBox
        self.compatibility_mode_checkbox = customtkinter.CTkCheckBox(
            self.program_settings_frame,
            text=self.translator.translate("compatibility_mode"),
            font=(self.font_family, 12),
            command=ProgramSettings.toggle_compatibility_mode
        )
        self.compatibility_mode_checkbox.grid(row=current_row_in_program_settings_frame, column=0, columnspan=2,
                                              padx=20, pady=(0, 10), sticky="w")

    def _change_language_event(self, new_language_display: str):
        # 使用 self.language_display_map 来查找对应的语言代码
        new_language_code = self.language_display_map.get(new_language_display)
        if new_language_code and self.change_language_callback:
            self.change_language_callback(new_language_code)

    def _change_appearance_mode_event(self, new_appearance_mode_translated: str):
        # Find the English key corresponding to the translated value.
        appearance_mode_to_set = "System"  # Default to "System"
        for appearance_mode_key, translated_value in self.appearance_mode_translations.items():
            if translated_value == new_appearance_mode_translated:
                appearance_mode_to_set = appearance_mode_key
                break
        customtkinter.set_appearance_mode(appearance_mode_to_set)

    def _restart_as_administrator(self):
        if not AdvancedStartup.is_administrator():
            """
            Construct the path to main.py in the program root directory.
            __file__ is ".../src/gui/pages/home_page.py".
            Program root is three levels up from os.path.dirname(__file__).
            """
            main_py_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "main.py")
            )

            """
            Prepare parameters: script path + original arguments (e.g., /DevMode).
            Ensure paths/args with spaces are quoted for ShellExecuteW.
            """
            formatted_original_args = [
                f'"{arg}"' if " " in arg else arg for arg in sys.argv[1:]
            ]

            """
            Construct the argument string for ShellExecuteW:
            "{main.py_script_path}" "arg1" "arg2_with_space" ...
            The main.py path itself also needs to be enclosed in double quotes to prevent spaces in the path.
            """
            params_list = [f'"{main_py_path}"'] + formatted_original_args
            params_str = " ".join(params_list)

            if not AdvancedStartup.run_as_administrator(params_str):
                failure_to_run_as_administrator_error_code = ctypes.get_last_error()
                failure_to_run_as_administrator_error_message = ctypes.FormatError(
                    failure_to_run_as_administrator_error_code).strip()
                messagebox.showerror(
                    self.translator.translate("error"),
                    f"{self.translator.translate('failure_to_run_as_administrator')}\n"
                    f"{self.translator.translate('error_code')}: {failure_to_run_as_administrator_error_code}\n"
                    f"{self.translator.translate('error_message')}: {failure_to_run_as_administrator_error_message}"
                )

    def _start_microsoft_pc_manager(self):
        self.start_microsoft_pc_manager_button.configure(state="disabled")

        def run_start_microsoft_pc_manager_command():
            try:
                start_microsoft_pc_manager_command = ["cmd.exe", "/C", "start",
                                                      "shell:AppsFolder\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe!App"
                                                      ]
                subprocess.run(start_microsoft_pc_manager_command, creationflags=subprocess.CREATE_NO_WINDOW)
            finally:
                # Ensure that UI components are updated in the main thread.
                self.master.after(0, lambda: self.start_microsoft_pc_manager_button.configure(state="normal"))

        threading.Thread(target=run_start_microsoft_pc_manager_command).start()

    def _start_microsoft_pc_manager_beta(self):
        self.start_microsoft_pc_manager_beta_button.configure(state="disabled")

        def run_start_microsoft_pc_manager_beta_command():
            try:
                start_microsoft_pc_manager_beta_command = ["cmd.exe", "/C", "start", "Start Microsoft PC Manager",
                                                           "%ProgramFiles%\\Microsoft PC Manager\\MSPCManager.exe"]
                subprocess.run(start_microsoft_pc_manager_beta_command, creationflags=subprocess.CREATE_NO_WINDOW)
            finally:
                # Ensure that UI components are updated in the main thread.
                self.master.after(0, lambda: self.start_microsoft_pc_manager_beta_button.configure(state="normal"))

        threading.Thread(target=run_start_microsoft_pc_manager_beta_command).start()
