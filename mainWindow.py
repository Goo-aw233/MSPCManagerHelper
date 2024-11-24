import ctypes
import locale
import os
import queue
import subprocess
import threading
import tkinter as tk
from advancedStartup import AdvancedStartup
from checkSystemRequirements import check_system_requirements
from getVersionNumber import GetPCManagerVersion
from installationFeature import InstallationFeature
from mainFeature import MainFeature
from otherFeature import OtherFeature
from tkinter import filedialog, messagebox, ttk
from topMenu import TopMenu
from translator import Translator
from uninstallationFeature import UninstallationFeature

class MSPCManagerHelper(tk.Tk):
    def __init__(self):
        super().__init__()
        main_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'MSPCManagerHelper-256.ico')
        self.iconbitmap(main_icon_path)
        self.MSPCManagerHelper_Version = "Beta v0.2.0.3"
        title = f"MSPCManagerHelper {self.MSPCManagerHelper_Version}"
        if AdvancedStartup.is_admin():
            title += " (Administrator)"
        if AdvancedStartup.is_devmode():
            title += " - DevMode"
        if AdvancedStartup.is_debugdevmode():
            title += " - DebugDevMode"
        self.set_dpi_awareness()  # 设置 DPI 感知
        self.title(title)
        window_width, window_height = 854, 480  # 窗口大小
        center_x, center_y = self.winfo_screenwidth() // 2 - window_width // 2, self.winfo_screenheight() // 2 - window_height // 2 # 计算窗口位置
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")  # 设置窗口位置
        self.resizable(False, False)    # 禁止调整窗口大小
        self.configure(bg="white")

        # 初始化功能
        self.translator = Translator('en-us')
        locale_str = locale.getlocale()[0]
        if locale_str.startswith("English"):
            self.translator = Translator('en-us')
        elif locale_str.startswith("Chinese (Simplified)"):
            self.translator = Translator('zh-cn')
        elif locale_str.startswith("Chinese (Traditional)"):
            self.translator = Translator('zh-tw')
        self.main_feature = MainFeature(self.translator)
        self.installation_feature = InstallationFeature(self.translator)
        self.uninstallation_feature = UninstallationFeature(self.translator)
        self.other_feature = OtherFeature(self.translator)
        self.create_widgets()
        self.result_queue = queue.Queue()
        self.cancelled = False
        self.current_process = None
        self.current_pid = None
        self.top_menu = None
        self.bind_all("<Alt_L>", self.toggle_top_menu)
        self.bind("<Button-1>", self.hide_top_menu)

        # 设置默认字体样式
        self.default_font_style = ("Segoe UI", 10)
        self.set_font_style()  # 设置字体样式

    # 设置 DPI 感知
    def set_dpi_awareness(self):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            messagebox.showerror(self.translator.translate("failed_to_set_dpi_awareness"), f"{str(e)}")

    # 创建窗口部件
    def create_widgets(self):
        # 语言选择组合框
        self.language_list = [self.translator.translate("lang_en-us"),
                    self.translator.translate("lang_zh-cn"),
                    self.translator.translate("lang_zh-tw"),
                    self.translator.translate("lang_custom")]
        translators = [Translator(i) for i in ['en-us', 'zh-cn', 'zh-tw']]
        self.languages = dict(zip(self.language_list, translators))
        self.language_combobox = ttk.Combobox(self, values=self.language_list,
                                              state="readonly", height=6)
        self.language_combobox.current(0)
        locale_str = locale.getlocale()[0]
        if locale_str.startswith("English"):
            self.language_combobox.current(0)
        elif locale_str.startswith("Chinese (Simplified)"):
            self.language_combobox.current(1)
        elif locale_str.startswith("Chinese (Traditional)"):
            self.language_combobox.current(2)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)
        self.language_combobox.place(x=35, y=80, width=180, height=25)

        # 检测版本的 TextBlock 和刷新按钮
        version_frame = tk.Frame(self, bg="white")
        version_frame.place(x=35, y=110)

        # 检查 Windows 版本号
        self.version_label = tk.Label(version_frame, text=self.translator.translate("current_pc_manager_version"), bg="white")
        self.version_label.pack(side="left", padx=(0, 10))

        # 刷新按钮
        self.refresh_button = tk.Button(version_frame, text=self.translator.translate("refresh"), command=self.refresh_version, width=10, height=1)
        self.refresh_button.pack(side="left")

        # 系统要求检测
        self.system_requirement_label = tk.Label(self, text=self.translator.translate("system_requirements_checking"), bg="white", wraplength=400, padx=0, pady=10)
        self.system_requirement_label.place(x=35, y=145)

        # 提示信息
        self.hint_label = tk.Label(self, text=self.translator.translate("notice_select_option"), bg="white")
        self.hint_label.place(x=35, y=210)

        # 第一个组合框
        self.main_combobox = ttk.Combobox(self, values=[self.translator.translate("select_option"),
                                                        self.translator.translate("main_project"),
                                                        self.translator.translate("install_project"),
                                                        self.translator.translate("uninstall_project"),
                                                        self.translator.translate("other_project")],
                                          state="readonly", height=8)  # 设置展开后的最大高度为 8
        self.main_combobox.current(0)
        self.main_combobox.bind("<<ComboboxSelected>>", self.update_feature_combobox)
        self.main_combobox.place(x=35, y=260, width=380, height=25)

        # 第二个组合框
        self.feature_combobox = ttk.Combobox(self, state="readonly", height=6)  # 设置展开后的最大高度为 6
        self.feature_combobox.place(x=35, y=310, width=380, height=25)

        # 执行按钮
        self.execute_button = tk.Button(self, text=self.translator.translate("main_execute_button"), command=self.execute_feature, width=10, height=1)
        self.execute_button.place(x=35, y=360)

        # 取消按钮
        self.cancel_button = tk.Button(self, text=self.translator.translate("main_cancel_button"), command=self.cancel_feature, state="disabled", width=10, height=1)
        self.cancel_button.place(x=145, y=360)

        # 以管理员身份运行按钮
        self.run_as_administrator_button = tk.Button(self, text=self.translator.translate("run_as_administrator"), command=self.run_as_administrator, width=20, height=1)
        self.run_as_administrator_button.place(x=255, y=360)
        if AdvancedStartup.is_admin():
            self.run_as_administrator_button.config(state="disabled")

        # 结果输出框 result_textbox
        self.result_textbox = tk.Text(self, wrap="word", state="disabled", bg="lightgray")
        self.result_textbox.place(x=435, y=80, width=400, height=310)
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.result_textbox.yview)
        # 将滚动条与 result_textbox 关联
        self.result_textbox.config(yscrollcommand=scrollbar.set)
        # 放置滚动条
        scrollbar.place(x=835, y=80, height=310)

        # 输出所有功能的信息到 result_textbox
        self.main_feature.result_textbox = self.result_textbox
        self.installation_feature.result_textbox = self.result_textbox
        self.uninstallation_feature.result_textbox = self.result_textbox
        self.other_feature.result_textbox = self.result_textbox
        self.textbox(self.translator.translate('see_term_of_use_and_privacy'))
        self.textbox(self.translator.translate('tips_open_top_menu'))
        self.textbox(self.translator.translate('tips_run_as_dev_mode'))

        # 初始检测版本号和系统要求
        self.refresh_version()
        self.check_system_requirements()

        # 创建 result_textbox 的右键菜单
        self.create_result_textbox_context_menu()
        self.result_textbox.bind("<Button-3>", self.show_result_textbox_context_menu)

    # 创建 result_textbox 右键菜单具体项目
    def create_result_textbox_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label=self.translator.translate("main_copy"), command=self.result_textbox_copy_to_clipboard)
        self.context_menu.add_command(label=self.translator.translate("main_clear"), command=self.clear_result_textbox)

    # 复制结果到剪贴板
    def result_textbox_copy_to_clipboard(self):
        try:
            selected_text = self.result_textbox.selection_get()
        except tk.TclError:
            selected_text = self.result_textbox.get("1.0", tk.END)

        self.clipboard_clear()
        self.clipboard_append(selected_text)

    # 清空 result_textbox 输出框
    def clear_result_textbox(self):
        self.result_textbox.config(state="normal")
        self.result_textbox.delete("1.0", tk.END)
        self.result_textbox.config(state="disabled")

    # 输出文本到 result_textbox
    def textbox(self, message):
        message = str(message)
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disable")
        self.result_textbox.update_idletasks()  # 刷新界面

    # 显示右键菜单
    def show_result_textbox_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    # 以管理员身份运行
    def run_as_administrator(self):
        params = __file__
        AdvancedStartup.run_as_admin(params)

    # 更改语言
    def change_language(self, event):
        selected_language = self.language_combobox.get()
        Load_Languages = self.translator.translate("lang_custom")
        add_language = False

        # 选择语言
        if selected_language in self.languages:
            self.translator = self.languages[selected_language]
        elif selected_language == Load_Languages:
            language_file_path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")])
            if language_file_path:
                add_language = True
                self.translator.load_translations(language_file_path)
                current_language = self.translator.translate("current_language")
                self.languages[self.translator.translate(current_language)] = self.translator

        # 更新语言选择组合框
        self.language_list = list(self.languages.keys()) + [self.translator.translate("lang_custom")]
        self.language_combobox.config(values=(self.language_list))
        if add_language:
            self.language_combobox.current(len(self.language_list)-2)
        else:
            current_language = self.translator.translate("current_language")
            current_language_index = self.language_list.index(self.translator.translate(current_language))

            self.language_combobox.current(current_language_index)
        self.language_combobox.update()

        self.main_feature = MainFeature(self.translator, self.result_textbox)  # 更新 MainFeature 语言实例
        self.installation_feature = InstallationFeature(self.translator, self.result_textbox)  # 更新 InstallationFeature 语言实例
        self.uninstallation_feature = UninstallationFeature(self.translator, self.result_textbox)  # 更新 UninstallationFeature 语言实例
        self.other_feature = OtherFeature(self.translator, self.result_textbox)  # 更新 OtherFeature 语言实例
        self.update_texts()
        self.refresh_version()
        self.check_system_requirements()
        self.set_font_style()  # 设置字体样式
        self.clear_result_textbox()
        # 重新输出指定协议与隐私
        self.textbox(self.translator.translate('see_term_of_use_and_privacy'))
        self.textbox(self.translator.translate('tips_open_top_menu'))
        self.textbox(self.translator.translate('tips_run_as_dev_mode'))

    # 更新文本
    def update_texts(self):
        self.version_label.config(text=self.translator.translate("current_pc_manager_version"))
        self.refresh_button.config(text=self.translator.translate("refresh"))
        self.system_requirement_label.config(text=self.translator.translate("system_requirements_checking"))
        self.hint_label.config(text=self.translator.translate("notice_select_option"))
        self.execute_button.config(text=self.translator.translate("main_execute_button"))
        self.cancel_button.config(text=self.translator.translate("main_cancel_button"))
        self.run_as_administrator_button.config(text=self.translator.translate("run_as_administrator"))  # 更新以管理员身份运行按钮的文本
        self.main_combobox.config(values=[self.translator.translate("select_option"),
                                          self.translator.translate("main_project"),
                                          self.translator.translate("install_project"),
                                          self.translator.translate("uninstall_project"),
                                          self.translator.translate("other_project"),
                                          ])
        self.main_combobox.current(0)
        self.update_feature_combobox(None)

        # 更新右键菜单的文本
        self.context_menu.entryconfig(0, label=self.translator.translate("main_copy"))  # 更新复制命令文本
        self.context_menu.entryconfig(1, label=self.translator.translate("main_clear"))  # 更新清除命令文本

    # 更新功能组合框内容
    def update_feature_combobox(self, event):
        selection = self.main_combobox.get()
        options = {
            self.translator.translate("main_project"): [self.translator.translate("repair_pc_manager"),
                                                        self.translator.translate("get_pc_manager_logs")],
            self.translator.translate("install_project"): [self.translator.translate("download_from_winget"),
                                                           self.translator.translate("download_from_msstore"),
                                                           self.translator.translate("install_for_all_users"),
                                                           self.translator.translate("install_for_current_user"),
                                                           self.translator.translate("reinstall_pc_manager"),
                                                           self.translator.translate("update_from_application_package"),
                                                           self.translator.translate("install_wv2_runtime")],
            self.translator.translate("uninstall_project"): [self.translator.translate("uninstall_for_all_users_in_dism"),
                                                             self.translator.translate("uninstall_for_all_users"),
                                                             self.translator.translate("uninstall_for_current_user"),
                                                             self.translator.translate("uninstall_pc_manager_beta")],
            self.translator.translate("other_project"): [self.translator.translate("view_installed_antivirus"),
                                                         self.translator.translate("developer_options"),
                                                         self.translator.translate("repair_edge_wv2_setup"),
                                                         self.translator.translate("pc_manager_docs"),
                                                         self.translator.translate("restart_pc_manager_service"),
                                                         self.translator.translate("switch_pc_manager_region"),
                                                         self.translator.translate("compute_files_hash"),
                                                         self.translator.translate("get_msedge_webview2_version")]
        }

        # 根据参数显示或隐藏选项
        if AdvancedStartup.is_devmode():
            options[self.translator.translate("install_project")].insert(5, self.translator.translate("install_from_appxmanifest"))
        if AdvancedStartup.is_debugdevmode():
            options[self.translator.translate("main_project")].append(self.translator.translate("debug_dev_mode"))  # 插入到末尾
            options[self.translator.translate("install_project")].insert(5, self.translator.translate("install_from_appxmanifest")) # 插入到第 5 个位置（从 0 开始）

        # 获取当前选择的语言
        # current_language = self.language_combobox.get()

        # 根据语言隐藏特定选项
        # language_hidden_options = [self.translator.translate("pc_manager_docs")]

        # 如果当前语言是 en-us 或 zh-tw 或其它语言，隐藏特定选项
        # if current_language in [self.translator.translate("lang_en-us"),
        #                         self.translator.translate("lang_zh-tw")]:
        #     for key in options:
        #         options[key] = [option for option in options[key] if option not in language_hidden_options]

        # 更新功能组合框的值
        self.feature_combobox['values'] = options.get(selection, [])
        self.feature_combobox.set("")

    # 执行功能
    def execute_feature(self):
        if self.main_combobox.get() == self.translator.translate("select_option") or not self.feature_combobox.get():
            messagebox.showwarning(self.translator.translate("warning"),
                                   self.translator.translate("select_function"))
        else:
            self.execute_button.config(state="disabled")
            self.cancel_button.config(state="normal")
            self.clear_result_textbox()  # 清空 TextBox 的内容
            main_feature_name = self.feature_combobox.get()
            executing_message = self.translator.translate('main_executing_operation').format(main_feature_name=main_feature_name)
            executing_message += '\n' + self.translator.translate('excessive_waiting_time')
            self.textbox(executing_message)

            def run_feature():
                result = ""
                # MainFeature
                if main_feature_name == self.translator.translate("repair_pc_manager"):
                    result = self.main_feature.repair_pc_manager()
                elif main_feature_name == self.translator.translate("get_pc_manager_logs"):
                    result = self.main_feature.get_pc_manager_logs()
                elif main_feature_name == self.translator.translate("debug_dev_mode"):
                    result = self.main_feature.debug_dev_mode()

                # InstallationFeature
                elif main_feature_name == self.translator.translate("download_from_winget"):
                    result = self.installation_feature.download_from_winget()
                elif main_feature_name == self.translator.translate("download_from_msstore"):
                    result = self.installation_feature.download_from_msstore()
                elif main_feature_name == self.translator.translate("install_for_all_users"):
                    result = self.installation_feature.install_for_all_users()
                elif main_feature_name == self.translator.translate("install_for_current_user"):
                    result = self.installation_feature.install_for_current_user()
                elif main_feature_name == self.translator.translate("reinstall_pc_manager"):
                    result = self.installation_feature.reinstall_pc_manager()
                elif main_feature_name == self.translator.translate("update_from_application_package"):
                    result = self.installation_feature.update_from_application_package()
                elif main_feature_name == self.translator.translate("install_from_appxmanifest"):
                    result = self.installation_feature.install_from_appxmanifest()
                elif main_feature_name == self.translator.translate("install_wv2_runtime"):
                    result = self.installation_feature.install_wv2_runtime(self)

                # UninstallationFeature
                elif main_feature_name == self.translator.translate("uninstall_for_all_users_in_dism"):
                    result = self.uninstallation_feature.uninstall_for_all_users_in_dism()
                elif main_feature_name == self.translator.translate("uninstall_for_all_users"):
                    result = self.uninstallation_feature.uninstall_for_all_users()
                elif main_feature_name == self.translator.translate("uninstall_for_current_user"):
                    result = self.uninstallation_feature.uninstall_for_current_user()
                elif main_feature_name == self.translator.translate("uninstall_pc_manager_beta"):
                    result = self.uninstallation_feature.uninstall_pc_manager_beta()

                # OtherFeature
                elif main_feature_name == self.translator.translate("view_installed_antivirus"):
                    result = self.other_feature.view_installed_antivirus()
                elif main_feature_name == self.translator.translate("developer_options"):
                    result = self.other_feature.developer_options()
                elif main_feature_name == self.translator.translate("repair_edge_wv2_setup"):
                    result = self.other_feature.repair_edge_wv2_setup()
                elif main_feature_name == self.translator.translate("pc_manager_docs"):
                    result = self.other_feature.pc_manager_docs()
                # elif main_feature_name == self.translator.translate("join_preview_program"):
                #     result = self.other_feature.join_preview_program()
                elif main_feature_name == self.translator.translate("restart_pc_manager_service"):
                    result = self.other_feature.restart_pc_manager_service()
                elif main_feature_name == self.translator.translate("switch_pc_manager_region"):
                    result = self.other_feature.switch_pc_manager_region()
                elif main_feature_name == self.translator.translate("compute_files_hash"):
                    result = self.other_feature.compute_files_hash()
                elif main_feature_name == self.translator.translate("get_msedge_webview2_version"):
                    result = self.other_feature.get_msedge_webview2_version()

                self.result_queue.put(result)
            threading.Thread(target=run_feature).start()
            self.after(100, self.process_queue)

    # 处理队列中的结果
    def process_queue(self):
        try:
            result = self.result_queue.get_nowait()
            self.result_textbox.config(state="normal")
            self.result_textbox.insert(tk.END, result)
            self.result_textbox.config(state="disabled")
            self.execute_button.config(state="normal")
            self.cancel_button.config(state="disabled")
        except queue.Empty:
            self.after(100, self.process_queue)

    # 获取进程 PID
    def get_pid(self):
        pid = []
        # 使用 tasklist.exe 获取所有进程信息并按行分割输出
        for line in os.popen('tasklist.exe').read().splitlines():
            if 'MicrosoftEdgeWebView2Setup.exe' in line or 'MicrosoftEdgeUpdate.exe' in line:
                # 分割行并提取 PID
                split = line.split()
                if 'Console' in split:
                    pid.append(split[1])  # PID 通常是第二个元素
        return pid

    # 结束进程
    def kill_process_by_pid(self):
        tf = True
        while tf:  # 循环 taskkill.exe，直到指定进程被 taskkill.exe 关闭
            for i in self.get_pid():
                subprocess.run(['taskkill.exe', '/PID', i, '/F'], creationflags=subprocess.CREATE_NO_WINDOW)
                tf = False

    # 取消功能
    def cancel_feature(self):
        self.cancelled = True
        self.execute_button.config(state="disabled")
        self.cancel_button.config(state="disabled")

        def kill_process_thread():
            self.kill_process_by_pid()  # 结束指定进程
            self.after(0, lambda: self.execute_button.config(state="normal"))

        threading.Thread(target=kill_process_thread).start()

    # 设置字体样式
    def set_font_style(self):
        default_font_style = ("Segoe UI", 10)
        font_styles = {
            "lang_en-us": default_font_style,
            "lang_zh-cn": ("微软雅黑", 10),
            "lang_zh-tw": ("微軟正黑體", 10),
            # 在这里添加更多语言及其对应的字体样式
        }

        selected_language = self.language_combobox.get()
        language_key = None

        if selected_language == self.translator.translate("lang_en-us"):
            language_key = "lang_en-us"
        elif selected_language == self.translator.translate("lang_zh-cn"):
            language_key = "lang_zh-cn"
        elif selected_language == self.translator.translate("lang_zh-tw"):
            language_key = "lang_zh-tw"

        font_style = font_styles.get(language_key, default_font_style)  # 如果未找到语言，默认使用 Segoe UI

        self.version_label.config(font=font_style)
        self.refresh_button.config(font=font_style)
        self.system_requirement_label.config(font=font_style)
        self.hint_label.config(font=font_style)
        self.execute_button.config(font=font_style)
        self.cancel_button.config(font=font_style)
        self.main_combobox.config(font=font_style)
        self.feature_combobox.config(font=font_style)
        self.result_textbox.config(font=font_style)
        # 重新设置 result_textbox 的大小
        self.result_textbox.place(x=435, y=80, width=400, height=310)

    # 刷新版本号
    def refresh_version(self):
        version, beta_version = GetPCManagerVersion().refresh_version()
        if version:
            self.version_label.config(text=f"{self.translator.translate('current_pc_manager_version')}: {version}")
            if beta_version:
                # 清除并重新输入 pc_manager_beta_installed 的内容
                self.result_textbox.config(state="normal")
                self.result_textbox.delete("1.0", tk.END)
                self.result_textbox.insert(tk.END, f"{self.translator.translate('pc_manager_beta_installed')}: {beta_version}\n")
        elif beta_version:
            self.version_label.config(text=f"{self.translator.translate('current_pc_manager_beta_version')}: {beta_version}")
        else:
            self.version_label.config(text=self.translator.translate("cannot_read_pc_manager_version"))

    # 检测系统要求
    def check_system_requirements(self):
        system_status = check_system_requirements(self.translator.locale)
        self.system_requirement_label.config(text=system_status)

    # 显示顶部菜单
    def toggle_top_menu(self, event):
        if self.top_menu is None:
            self.top_menu = TopMenu(self, self.translator, self.MSPCManagerHelper_Version)
            self.config(menu=self.top_menu.top_menu)
        else:
            self.config(menu=tk.Menu(self))  # 使用空的 tk.Menu 实例
            self.top_menu = None

    def hide_top_menu(self, event):
        if self.top_menu is not None:
            self.config(menu=tk.Menu(self))  # 使用空的 tk.Menu 实例
            self.top_menu = None

    def show_top_menu(self, event):
        self.top_menu = TopMenu(self, self.translator, self.MSPCManagerHelper_Version)
        self.config(menu=self.top_menu.top_menu)

if __name__ == "__main__":
    app = MSPCManagerHelper()
    app.mainloop()
