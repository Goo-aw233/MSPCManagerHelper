import customtkinter
import locale
import tkinter.font
from tkinter import messagebox
from windows_toasts import Toast, WindowsToaster
from . import __program_name__, __program_version__
from .modules import (AdvancedStartup, CheckSystemRequirements, GetProgramResources)
from .navigation import NavigationFrame
from .translator import Translator
from .pages import (
    HomePageFrame, MaintenancePageFrame, InstallationFeaturesPageFrame,
    UninstallationFeaturesPageFrame, UtilsPageFrame, ToolboxPageFrame, AboutPageFrame
)


class MSPCManagerHelperMainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._set_language()
        self._check_system_requirements()
        self._init_ui()

    def _configure_window(self):
        # Set the Window Title
        program_title_str = f"{__program_name__} {__program_version__}"
        if AdvancedStartup.is_administrator():
            program_title_str += " (Administrator)"
        if AdvancedStartup.is_devmode():
            program_title_str += " - DevMode"
        self.title(program_title_str)
        # Set Font Family
        self.font_family = tkinter.font.nametofont("TkDefaultFont").actual()["family"]
        # Set Window Size
        self._adjust_window_size(default_width=984, default_height=661)
        # Set Window Icon
        program_icon_path = GetProgramResources.get_program_icon()
        if program_icon_path:
            self.iconbitmap(program_icon_path)

    def _set_language(self, language=None):
        if language is None:
            language_map = {
                ('en_',): 'en-us',
                ('zh_CN', 'zh_Hans', 'zh_Hans_HK', 'zh_Hans_MO', 'zh_Hans_SG', 'zh_SG'): 'zh-cn',
                ('zh_Hant', 'zh_Hant_HK', 'zh_Hant_MO', 'zh_Hant_TW', 'zh_HK', 'zh_MO', 'zh_TW'): 'zh-tw'
            }
            locale_str = locale.getdefaultlocale()[0]
            default_language = 'en-us'
            language = default_language
            for prefixes, trans_locale in language_map.items():
                if any(locale_str.startswith(prefix) for prefix in prefixes):
                    language = trans_locale
                    break
        self.language = language
        self.translator = Translator(self.language)

    def _check_system_requirements(self):
        if CheckSystemRequirements.check_admin_approval_mode():
            messagebox.showwarning(
                self.translator.translate("warning"),
                self.translator.translate("administrator_protection_is_enabled")
            )
        if CheckSystemRequirements.check_windows_server_levels():
            messagebox.showwarning(
                self.translator.translate("warning"),
                self.translator.translate("windows_server_installation_type_is_core")
            )
        if not AdvancedStartup.is_administrator():
            toaster = WindowsToaster(self.translator.translate("mspcmanagerhelper"))
            toast_notification = Toast()
            toast_notification.text_fields = [
                self.translator.translate("administrator_required"),
                self.translator.translate("program_is_not_running_as_administrator")
            ]
            toaster.show_toast(toast_notification)

    def _init_ui(self):
        # 清除旧的 widgets
        for widget in self.winfo_children():
            widget.destroy()

        # 设置主窗口的 grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=40)

        # 创建各页面 Frame
        self.frames = {
            "home_page": HomePageFrame(self, font_family=self.font_family, translator=self.translator, change_language_callback=self.change_language),
            "maintenance_page": MaintenancePageFrame(self, font_family=self.font_family, translator=self.translator),
            "installation_features_page": InstallationFeaturesPageFrame(self, font_family=self.font_family, translator=self.translator),
            "uninstallation_features_page": UninstallationFeaturesPageFrame(self, font_family=self.font_family, translator=self.translator),
            "utils_page": UtilsPageFrame(self, font_family=self.font_family, translator=self.translator),
            "toolbox_page": ToolboxPageFrame(self, font_family=self.font_family, translator=self.translator),
            "about_page": AboutPageFrame(self, font_family=self.font_family, translator=self.translator),
        }
        for frame in self.frames.values():
            frame.grid(row=0, column=1, sticky="nsew")
            frame.grid_remove()

        # 创建导航栏，传入 font_family 和 translator
        self.navigation_frame = NavigationFrame(
            self,
            self._on_page_change,
            font_family=self.font_family,
            translator=self.translator
        )
        self.navigation_frame.grid(row=0, column=0, sticky="nsw")

        # 默认显示首页
        self.navigation_frame.select_page("home_page")

    def change_language(self, new_language_code: str):
        self._set_language(new_language_code)
        self._init_ui()

    def _on_page_change(self, page_name):
        self._show_page(page_name)

    def _show_page(self, page_name):
        for name, frame in self.frames.items():
            if name == page_name:
                frame.grid()
            else:
                frame.grid_remove()

    def _adjust_window_size(self, default_width, default_height, offset_ratio=0.05):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        min_offset = int(min(screen_width, screen_height) * offset_ratio)
        width = min(default_width, screen_width - min_offset)
        height = min(default_height, screen_height - min_offset)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
