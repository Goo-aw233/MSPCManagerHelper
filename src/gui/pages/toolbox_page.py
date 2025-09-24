import webbrowser

import customtkinter

from ..modules.program_settings import ProgramSettings


class ToolboxPageFrame(customtkinter.CTkScrollableFrame):
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
            text=self.translator.translate("toolbox_page"),
            font=(self.font_family, 20, "bold"),
            anchor="center"
        )
        self.title_label.grid(row=current_row, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.title_label.bind("<Configure>", lambda event: self.title_label.configure(
            wraplength=self.title_label.winfo_width() - 20))
        current_row += 1

        """ Program Update Frame """
        self.program_update_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.program_update_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.program_update_frame.grid_columnconfigure(0, weight=1)

        self.program_update_label_title = customtkinter.CTkLabel(self.program_update_frame,
                                                                 text=self.translator.translate("program_update"),
                                                                 font=(self.font_family, 16, "bold"))
        self.program_update_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.get_mspcmanagerhelper_github_button = customtkinter.CTkButton(
            self.program_update_frame,
            text=self.translator.translate("get_mspcmanagerhelper_from_github"),
            font=(self.font_family, 12),
            command=lambda: webbrowser.open_new_tab("https://github.com/Goo-aw233/MSPCManagerHelper/releases")
        )
        self.get_mspcmanagerhelper_github_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.get_mspcmanagerhelper_onedrive_button = customtkinter.CTkButton(
            self.program_update_frame,
            text=self.translator.translate("get_mspcmanagerhelper_from_onedrive"),
            font=(self.font_family, 12),
            command=lambda: webbrowser.open_new_tab("https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA")
        )
        self.get_mspcmanagerhelper_onedrive_button.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        current_row += 1

        """ Microsoft PC Manager Update Frame """
        self.ms_pc_manager_update_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.ms_pc_manager_update_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.ms_pc_manager_update_frame.grid_columnconfigure(0, weight=1)

        self.ms_pc_manager_update_label_title = customtkinter.CTkLabel(
            self.ms_pc_manager_update_frame,
            text=self.translator.translate("microsoft_pc_manager_update"),
            font=(self.font_family, 16, "bold")
        )
        self.ms_pc_manager_update_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.get_ms_pc_manager_licaoz_button = customtkinter.CTkButton(
            self.ms_pc_manager_update_frame,
            text=self.translator.translate("get_microsoft_pc_manager_from_licaoz_azure_blob"),
            font=(self.font_family, 12),
            command=lambda: webbrowser.open_new_tab("https://kaoz.uk/PCManagerOFL")
        )
        self.get_ms_pc_manager_licaoz_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.get_ms_pc_manager_onedrive_button = customtkinter.CTkButton(
            self.ms_pc_manager_update_frame,
            text=self.translator.translate("get_microsoft_pc_manager_from_onedrive"),
            font=(self.font_family, 12),
            command=lambda: webbrowser.open_new_tab(
                "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EoscJOQ9taJFtx9LZLPiBM0BEmVm7wsLuJOuHnwmo9EQ5w")
        )
        self.get_ms_pc_manager_onedrive_button.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        current_row += 1

        """ Runtime Download Frame """
        self.runtime_download_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width=1)
        self.runtime_download_frame.grid(row=current_row, column=0, padx=20, pady=10, sticky="ew")
        self.runtime_download_frame.grid_columnconfigure(0, weight=1)

        self.runtime_download_label_title = customtkinter.CTkLabel(
            self.runtime_download_frame,
            text=self.translator.translate("runtime_download"),
            font=(self.font_family, 16, "bold")
        )
        self.runtime_download_label_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.get_microsoft_edge_webview2_button = customtkinter.CTkButton(
            self.runtime_download_frame,
            text=self.translator.translate("get_microsoft_edge_webview2_from_microsoft_edge_developer"),
            font=(self.font_family, 12),
            command=self._open_microsoft_edge_webview2_download_link
        )
        self.get_microsoft_edge_webview2_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.get_windows_app_runtime_button = customtkinter.CTkButton(
            self.runtime_download_frame,
            text=self.translator.translate("get_windows_app_runtime_from_microsoft_learn"),
            font=(self.font_family, 12),
            command=self._open_windows_app_runtime_download_link
        )
        self.get_windows_app_runtime_button.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        current_row += 1

    @staticmethod
    def _open_microsoft_edge_webview2_download_link():
        base_url = "https://developer.microsoft.com/microsoft-edge/webview2"
        if ProgramSettings.is_support_developer_enabled():
            url_to_open = base_url + ProgramSettings.microsoft_student_ambassadors_cid
        else:
            url_to_open = base_url
        webbrowser.open_new_tab(url_to_open)

    @staticmethod
    def _open_windows_app_runtime_download_link():
        base_url = "https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive"
        if ProgramSettings.is_support_developer_enabled():
            url_to_open = base_url + ProgramSettings.microsoft_student_ambassadors_cid
        else:
            url_to_open = base_url
        webbrowser.open_new_tab(url_to_open)
