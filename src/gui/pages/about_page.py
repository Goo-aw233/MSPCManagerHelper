import subprocess
import threading
import webbrowser
from tkinter import messagebox

import customtkinter

from .. import __program_name__, __program_version__
from ..modules import CheckSystemRequirements


class AboutPageFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, font_family=None, translator=None, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, *args, **kwargs)
        self.font_family = font_family
        self.translator = translator

        # 配置网格权重
        self.grid_columnconfigure(0, weight=1)
        # 初始化主框架的行计数器
        current_row = 0

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text=self.translator.translate("about_page"),
            font=(self.font_family, 20, "bold")
        )
        self.title_label.grid(row=current_row, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.title_label.bind("<Configure>", lambda event: self.title_label.configure(
            wraplength=self.title_label.winfo_width() - 20))
        current_row += 1

        # Program Information Frame
        self.program_info_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.program_info_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.program_info_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.program_info_label_title = customtkinter.CTkLabel(self.program_info_frame,
                                                               text=self.translator.translate("program_information"),
                                                               font=(self.font_family, 16, "bold"))
        self.program_info_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.program_info_content_label = customtkinter.CTkLabel(self.program_info_frame, justify="left")
        translated_program_info_content_1 = f'{self.translator.translate("program_name")}: {__program_name__}'
        translated_program_info_content_2 = f'{self.translator.translate("program_version")}: {__program_version__}'
        combined_program_info = (f"{translated_program_info_content_1}\n"
                                 f"{translated_program_info_content_2}")
        self.program_info_content_label.configure(text=combined_program_info, font=(self.font_family, 12),
                                                  anchor="center")
        self.program_info_content_label.bind("<Configure>", lambda event: self.program_info_content_label.configure(
            wraplength=self.program_info_frame.winfo_width() - 20))
        self.program_info_content_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Contributors Frame
        self.contributors_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.contributors_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.contributors_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.contributors_label_title = customtkinter.CTkLabel(self.contributors_frame,
                                                               text=self.translator.translate("contributors"),
                                                               font=(self.font_family, 16, "bold"))
        self.contributors_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.contributors_name_label = customtkinter.CTkLabel(self.contributors_frame, justify="left")
        translated_contributors_name = self.translator.translate("contributors_name")
        self.contributors_name_label.configure(text=translated_contributors_name, font=(self.font_family, 12),
                                               anchor="center")
        self.contributors_name_label.bind("<Configure>", lambda event: self.contributors_name_label.configure(
            wraplength=self.contributors_frame.winfo_width() - 20))
        self.contributors_name_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Translators Frame
        self.translators_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.translators_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.translators_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.translators_label_title = customtkinter.CTkLabel(self.translators_frame,
                                                              text=self.translator.translate("translators"),
                                                              font=(self.font_family, 16, "bold"))
        self.translators_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.translators_name_label = customtkinter.CTkLabel(self.translators_frame, justify="left")
        translated_translators_name = self.translator.translate("translators_name")
        self.translators_name_label.configure(text=translated_translators_name, font=(self.font_family, 12),
                                              anchor="center")
        self.translators_name_label.bind("<Configure>", lambda event: self.translators_name_label.configure(
            wraplength=self.translators_frame.winfo_width() - 20))
        self.translators_name_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Terms of Use Frame
        self.terms_of_use_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.terms_of_use_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.terms_of_use_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.terms_of_use_label_title = customtkinter.CTkLabel(self.terms_of_use_frame,
                                                               text=self.translator.translate("terms_of_use"),
                                                               font=(self.font_family, 16, "bold"))
        self.terms_of_use_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.terms_of_use_content_label = customtkinter.CTkTextbox(
            self.terms_of_use_frame,
            wrap="word",
            fg_color="transparent",
            border_width=0,
            height=200,
            font=(self.font_family, 12)
        )
        translated_terms_of_use_content = self.translator.translate("terms_of_use_content")
        self.terms_of_use_content_label.insert("1.0", translated_terms_of_use_content)
        self.terms_of_use_content_label.configure(state="disabled")
        self.terms_of_use_content_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Privacy Policy Frame
        self.privacy_policy_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.privacy_policy_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.privacy_policy_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.privacy_policy_label_title = customtkinter.CTkLabel(self.privacy_policy_frame,
                                                                 text=self.translator.translate("privacy_policy"),
                                                                 font=(self.font_family, 16, "bold"))
        self.privacy_policy_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.privacy_policy_content_label = customtkinter.CTkTextbox(
            self.privacy_policy_frame,
            wrap="word",
            fg_color="transparent",
            border_width=0,
            height=100,
            font=(self.font_family, 12)
        )
        translated_privacy_policy_content = self.translator.translate("privacy_policy_content")
        self.privacy_policy_content_label.insert("1.0", translated_privacy_policy_content)
        self.privacy_policy_content_label.configure(state="disabled")
        self.privacy_policy_content_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Privacy Settings Button
        self.privacy_settings_button = customtkinter.CTkButton(
            self.privacy_policy_frame,
            text=self.translator.translate("privacy_settings"),
            font=(self.font_family, 12),
            command=self._open_privacy_settings_window
        )
        self.privacy_settings_button.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        if CheckSystemRequirements.check_windows_server_levels():
            self.privacy_settings_button.configure(state="disabled")

        # Help Frame
        self.help_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.help_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.help_frame.grid_columnconfigure(0, weight=1)
        current_row += 1

        self.help_label_title = customtkinter.CTkLabel(self.help_frame,
                                                       text=self.translator.translate("help"),
                                                       font=(self.font_family, 16, "bold"))
        self.help_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Repository URL Button
        self.repository_url_button = customtkinter.CTkButton(self.help_frame,
                                                             text=self.translator.translate("repository_url"),
                                                             font=(self.font_family, 12),
                                                             command=lambda: webbrowser.open_new_tab(
                                                                 "https://github.com/Goo-aw233/MSPCManagerHelper"))
        self.repository_url_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Get Help Button
        self.get_help_button = customtkinter.CTkButton(self.help_frame,
                                                       text=self.translator.translate("get_help"),
                                                       font=(self.font_family, 12),
                                                       command=lambda: webbrowser.open_new_tab(
                                                           "https://mspcmanager.github.io/mspcm-docs"))
        self.get_help_button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Official Website Button
        self.official_website_button = customtkinter.CTkButton(self.help_frame,
                                                               text=self.translator.translate("official_website"),
                                                               font=(self.font_family, 12),
                                                               command=lambda: webbrowser.open_new_tab(
                                                                   "https://pcmanager.microsoft.com"))
        self.official_website_button.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Contact Us Button
        self.contact_us_button = customtkinter.CTkButton(self.help_frame,
                                                         text=self.translator.translate("contact_us"),
                                                         font=(self.font_family, 12),
                                                         command=self._open_the_official_website_for_more_contact)
        self.contact_us_button.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")

    def _open_the_official_website_for_more_contact(self):
        messagebox.showinfo(
            self.translator.translate("info"),
            self.translator.translate("get_more_contact_from_official_website")
        )
        webbrowser.open_new_tab("https://pcmanager.microsoft.com")

    def _open_privacy_settings_window(self):
        self.privacy_settings_button.configure(state="disabled")

        def open_privacy_settings_window_command():
            try:
                subprocess.run(["cmd.exe", "/C", "start", "ms-settings:privacy"], check=True,
                               creationflags=subprocess.CREATE_NO_WINDOW)
            finally:
                # Ensure that UI components are updated in the main thread.
                self.master.after(0, lambda: self.privacy_settings_button.configure(state="normal"))

        threading.Thread(target=open_privacy_settings_window_command).start()
