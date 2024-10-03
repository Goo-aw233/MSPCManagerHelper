import tkinter as tk
import webbrowser

class TopMenu:
    def __init__(self, parent, translator, version):
        self.top_menu_update = None
        self.top_menu_properties = None
        self.top_menu = None
        self.parent = parent
        self.translator = translator
        self.version = version
        self.create_menu()

    def create_menu(self):
        self.top_menu = tk.Menu(self.parent)
        self.top_menu_properties = tk.Menu(self.top_menu, tearoff=0)
        self.top_menu_update = tk.Menu(self.top_menu, tearoff=0)

        self.top_menu.add_cascade(label=self.translator.translate("top_menu_update"), menu=self.top_menu_update)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_GitHub"), command=TopMenuUpdate.open_github_update)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_OneDrive"), command=TopMenuUpdate.open_onedrive_update)
        self.top_menu_update.add_separator()
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_LiCaoZ_Azure_Blob_PC_Manager"), command=TopMenuUpdate.open_LiCaoZ_Azure_Blob_application_package)
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_OneDrive_PC_Manager"), command=TopMenuUpdate.open_OneDrive_application_package)
        self.top_menu_update.add_separator()
        self.top_menu_update.add_command(label=self.translator.translate("top_menu_update_WindowsAppRuntime"), command=TopMenuUpdate.open_WindowsAppRuntime_download)

        self.top_menu.add_cascade(label=self.translator.translate("top_menu_properties"), menu=self.top_menu_properties)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_about"), command=self.properties_about)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_help"), command=TopMenuProperties.open_help)
        self.top_menu_properties.add_command(label=self.translator.translate("top_menu_properties_official_site"), command=TopMenuProperties.open_official_site)

    def properties_about(self):
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
        webbrowser.open("https://www.microsoft.com/download/details.aspx?id=105892")

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
                      f"\n{self.translator.translate('translation_author')}: {self.translator.translate('localization_translators')}")
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
