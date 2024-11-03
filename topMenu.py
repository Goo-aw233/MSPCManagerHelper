import os
import textwrap
import tkinter as tk
import webbrowser
from tkinter import ttk

class TopMenu:
    def __init__(self, parent, translator, version):
        self.top_menu_update = None
        self.top_menu_term_of_use_and_privacy = None
        self.top_menu_properties = None
        self.top_menu = None
        self.parent = parent
        self.translator = translator
        self.version = version
        self.create_menu()

    def create_menu(self):
        self.top_menu = tk.Menu(self.parent)
        self.top_menu_properties = tk.Menu(self.top_menu, tearoff=0)
        self.top_menu_term_of_use_and_privacy = tk.Menu(self.top_menu, tearoff=0)
        self.top_menu_update = tk.Menu(self.top_menu, tearoff=0)

        self.top_menu.add_cascade(label=self.translator.translate("top_menu_update"), menu=self.top_menu_update)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_GitHub"), command=TopMenuUpdate.open_github_update)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_OneDrive"), command=TopMenuUpdate.open_onedrive_update)
        self.top_menu_update.add_separator()
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_LiCaoZ_Azure_Blob_PC_Manager"), command=TopMenuUpdate.open_LiCaoZ_Azure_Blob_application_package)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_OneDrive_PC_Manager"), command=TopMenuUpdate.open_OneDrive_application_package)
        self.top_menu_update.add_separator()
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_WindowsAppRuntime"), command=TopMenuUpdate.open_WindowsAppRuntime_download)

        self.top_menu.add_cascade(label=self.translator.translate("top_menu_term_of_use_and_privacy"), menu=self.top_menu_term_of_use_and_privacy)
        self.top_menu_term_of_use_and_privacy.add_command(label=self.translator.translate("top_menu_term_of_use"), command=self.top_menu_term_of_use)
        self.top_menu_term_of_use_and_privacy.add_command(label=self.translator.translate("top_menu_privacy"), command=self.top_menu_privacy)

        self.top_menu.add_cascade(label=self.translator.translate("top_menu_properties"), menu=self.top_menu_properties)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_about"), command=self.top_menu_properties_about)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_help"), command=TopMenuProperties.open_help)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_official_site"), command=TopMenuProperties.open_official_site)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_more_contact"), command=lambda: TopMenuProperties.open_more_contact(self.translator))

    def top_menu_term_of_use(self):
        TopMenuTermOfUse(self.parent, self.translator).show_term_of_use_window()

    def top_menu_privacy(self):
        TopMenuTermOfUse(self.parent, self.translator).show_privacy_window()

    def top_menu_properties_about(self):
        TopMenuProperties(self.parent, self.translator, self.version)

class TopMenuUpdate:
    @staticmethod
    def open_github_update():
        webbrowser.open("https://github.com/Goo-aw233/MSPCManagerHelper/releases")

    @staticmethod
    def open_onedrive_update():
        webbrowser.open("https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA")
    @staticmethod
    def open_LiCaoZ_Azure_Blob_application_package():
        webbrowser.open("https://lcz.ink/PCMOFL")

    @staticmethod
    def open_OneDrive_application_package():
        webbrowser.open("https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EoscJOQ9taJFtx9LZLPiBM0BEmVm7wsLuJOuHnwmo9EQ5w")

    @staticmethod
    def open_WindowsAppRuntime_download():
        webbrowser.open("https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive?wt.mc_id=studentamb_265231#windows-app-sdk-15")

class TopMenuTermOfUse:
    def __init__(self, parent, translator):
        self.parent = parent
        self.translator = translator

    def show_term_of_use_window(self):
        term_of_use_window = tk.Toplevel(self.parent)
        term_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'MSPCManagerHelper-256.ico')
        term_of_use_window.iconbitmap(term_icon_path)
        term_of_use_window.title(self.translator.translate("top_menu_term_of_use"))
        term_of_use_window.geometry("400x300")
        term_of_use_window.resizable(False, False)  # 禁止调整窗口大小
        term_of_use_window.transient(self.parent)  # 设置窗口为模态
        term_of_use_window.grab_set()

        # 使窗口在程序窗口的位置居中显示
        term_of_use_window.update_idletasks()
        window_width = term_of_use_window.winfo_width()
        window_height = term_of_use_window.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        position_top = parent_y + (parent_height // 2) - (window_height // 2)
        position_right = parent_x + (parent_width // 2) - (window_width // 2)
        term_of_use_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        term_of_use_text = self.translator.translate("TermOfUse_context")

        # 创建滚动条
        scrollbar = ttk.Scrollbar(term_of_use_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本框
        text_widget = tk.Text(term_of_use_window, wrap="word", yscrollcommand=scrollbar.set)
        text_widget.insert(tk.END, term_of_use_text)
        text_widget.config(state=tk.DISABLED)  # 禁止编辑
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        # 配置滚动条
        scrollbar.config(command=text_widget.yview)

        term_of_use_window.protocol("WM_DELETE_WINDOW", term_of_use_window.destroy)

    def show_privacy_window(self):
        privacy_window = tk.Toplevel(self.parent)
        privacy_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'MSPCManagerHelper-256.ico')
        privacy_window.iconbitmap(privacy_icon_path)
        privacy_window.title(self.translator.translate("top_menu_privacy"))
        privacy_window.geometry("400x300")
        privacy_window.resizable(False, False)  # 禁止调整窗口大小
        privacy_window.transient(self.parent)  # 设置窗口为模态
        privacy_window.grab_set()

        # 使窗口在程序窗口的位置居中显示
        privacy_window.update_idletasks()
        window_width = privacy_window.winfo_width()
        window_height = privacy_window.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        position_top = parent_y + (parent_height // 2) - (window_height // 2)
        position_right = parent_x + (parent_width // 2) - (window_width // 2)
        privacy_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        privacy_text = self.translator.translate("Privacy_context")

        # 创建滚动条
        scrollbar = ttk.Scrollbar(privacy_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本框
        text_widget = tk.Text(privacy_window, wrap="word", yscrollcommand=scrollbar.set)
        text_widget.insert(tk.END, privacy_text)
        text_widget.config(state=tk.DISABLED)  # 禁止编辑
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        # 配置滚动条
        scrollbar.config(command=text_widget.yview)

        privacy_window.protocol("WM_DELETE_WINDOW", privacy_window.destroy)

class TopMenuProperties:
    def __init__(self, parent, translator, version):
        self.parent = parent
        self.translator = translator
        self.version = version
        self.show_properties_properties_about_window()

    def show_properties_properties_about_window(self):
        properties_about_window = tk.Toplevel(self.parent)
        properties_about_window.title(self.translator.translate("top_menu_properties_about"))
        properties_about_window.geometry("300x150")
        properties_about_window.resizable(False, False) # 禁止调整窗口大小
        properties_about_window.transient(self.parent)  # 设置窗口为模态
        properties_about_window.grab_set()

        # 使窗口在程序窗口的位置居中显示
        properties_about_window.update_idletasks()
        window_width = properties_about_window.winfo_width()
        window_height = properties_about_window.winfo_height()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        position_top = parent_y + (parent_height // 2) - (window_height // 2)
        position_right = parent_x + (parent_width // 2) - (window_width // 2)
        properties_about_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        label_text = (f"MSPCManagerHelper"
                      f"\n{self.version}"
                      f"\n{self.translator.translate('translation_author')}: {self.translator.translate('localization_translators_name')}"
                      f"\n{self.translator.translate('project_contributors')}: {textwrap.fill(self.translator.translate('project_contributors_name'), width=30)}"
                      )
        label = tk.Label(properties_about_window, text=label_text, justify="center")
        label.pack(expand=True)

        properties_about_window.protocol("WM_DELETE_WINDOW", properties_about_window.destroy)

        # 绑定 ESC 键关闭窗口
        properties_about_window.bind("<Escape>", lambda event: properties_about_window.destroy())

    @staticmethod
    def open_help():
        webbrowser.open("https://github.com/Goo-aw233/MSPCManagerHelper/wiki")

    @staticmethod
    def open_official_site():
        webbrowser.open("https://pcmanager.microsoft.com")

    @staticmethod
    def open_more_contact(translator):
        if translator.locale == "zh-cn":
            webbrowser.open("https://forms.office.com/r/7YhjaEEmKc")
        else:
            webbrowser.open("https://forms.office.com/r/EPcrKfUbjK")