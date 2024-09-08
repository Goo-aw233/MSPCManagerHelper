import os
import subprocess
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from checkSystemRequirements import check_system_requirements
from getVersionNumber import get_current_windows_version
from installationFeature import InstallationFeature
from mainFeature import MainFeature
from runAsAdministrator import Administrator
from translator import Translator
from otherFeature import OtherFeature
from uninstallationFeature import UninstallationFeature

class MSPCManagerHelper(tk.Tk):
    def __init__(self):
        super().__init__()
        if Administrator.is_admin():
            self.title("MSPCManagerHelper Preview v2498 - we11C (Administrator)")
        else:
            self.title("MSPCManagerHelper Preview v2498 - we11C")
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(bg="white")

        # 初始化功能
        self.translator = Translator('en-us')
        self.main_feature = MainFeature(self.translator)
        self.installation_feature = InstallationFeature(self.translator)
        self.uninstallation_feature = UninstallationFeature(self.translator)
        self.other_feature = OtherFeature(self.translator)
        self.create_widgets()
        self.result_queue = queue.Queue()
        self.cancelled = False
        self.current_process = None
        self.current_pid = None

        # 设置默认字体样式
        self.default_font_style = ("Segoe UI", 10)
        self.set_font_style()  # 设置字体样式

    # 创建窗口部件
    def create_widgets(self):
        # 语言选择组合框
        self.language_combobox = ttk.Combobox(self, values=[self.translator.translate("lang_en-us"),
                                                            self.translator.translate("lang_zh-cn"),
                                                            self.translator.translate("lang_zh-tw")],
                                              state="readonly")
        self.language_combobox.current(0)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)
        self.language_combobox.place(x=35, y=80, width=180, height=25)

        # 检测版本的 TextBlock 和刷新按钮
        version_frame = tk.Frame(self, bg="white")
        version_frame.place(x=35, y=110)

        # 版本号
        self.version_label = tk.Label(version_frame, text=self.translator.translate("current_pcm_version"), bg="white")
        self.version_label.pack(side="left", padx=(0, 10))

        # 刷新按钮
        self.refresh_button = tk.Button(version_frame, text=self.translator.translate("refresh"), command=self.refresh_version, width=10, height=1)
        self.refresh_button.pack(side="left")

        # 系统要求检测
        self.system_requirement_label = tk.Label(self, text=self.translator.translate("system_requirements_checking"), bg="white", wraplength=400, padx=0, pady=10)
        self.system_requirement_label.place(x=35, y=150)

        # 提示信息
        self.hint_label = tk.Label(self, text=self.translator.translate("notice_select_option"), bg="white")
        self.hint_label.place(x=35, y=205)

        # 第一个组合框
        self.main_combobox = ttk.Combobox(self, values=[self.translator.translate("select_option"),
                                                        self.translator.translate("main_project"),
                                                        self.translator.translate("install_project"),
                                                        self.translator.translate("uninstall_project"),
                                                        self.translator.translate("other_project")],
                                          state="readonly")
        self.main_combobox.current(0)
        self.main_combobox.bind("<<ComboboxSelected>>", self.update_feature_combobox)
        self.main_combobox.place(x=35, y=260, width=380, height=25)

        # 第二个组合框
        self.feature_combobox = ttk.Combobox(self, state="readonly")
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
        if Administrator.is_admin():
            self.run_as_administrator_button.config(state="disabled")

        # 结果输出框
        self.result_textbox = tk.Text(self, wrap="word", state="disabled", bg="lightgray")
        self.result_textbox.place(x=435, y=80, width=400, height=310)

        # 初始检测版本号和系统要求
        self.refresh_version()
        self.check_system_requirements()

        # 创建 result_textbox 右键菜单
        self.create_result_textbox_context_menu()
        self.update_result_textbox_context_menu()  # 确保调用 update_result_textbox_context_menu 方法
        self.result_textbox.bind("<Button-3>", self.show_result_textbox_context_menu)

    # 更新右键菜单中的“复制”选项标签文本
    def update_result_textbox_context_menu(self):
        self.context_menu.entryconfig(0, label=self.translator.translate("main_copy"))

    # 创建 result_textbox 右键菜单具体项目
    def create_result_textbox_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label=self.translator.translate("main_copy"), command=self.result_textbox_copy_to_clipboard)

    # 复制结果到剪贴板
    def result_textbox_copy_to_clipboard(self):
        try:
            selected_text = self.result_textbox.selection_get()
        except tk.TclError:
            selected_text = self.result_textbox.get("1.0", tk.END)

        self.clipboard_clear()
        self.clipboard_append(selected_text)

    # 显示右键菜单
    def show_result_textbox_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    # 以管理员身份运行
    def run_as_administrator(self):
        params = __file__
        Administrator.run_as_admin(params)

    # 更改语言
    def change_language(self, event):
        selected_language = self.language_combobox.get()
        if selected_language == self.translator.translate("lang_en-us"):
            self.translator = Translator('en-us')
        elif selected_language == self.translator.translate("lang_zh-cn"):
            self.translator = Translator('zh-cn')
        elif selected_language == self.translator.translate("lang_zh-tw"):
            self.translator = Translator('zh-tw')
        self.main_feature = MainFeature(self.translator)  # 更新 MainFeature 语言实例
        self.installation_feature = InstallationFeature(self.translator)  # 更新 InstallationFeature 语言实例
        self.uninstallation_feature = UninstallationFeature(self.translator)  # 更新 UninstallationFeature 语言实例
        self.other_feature = OtherFeature(self.translator)  # 更新 OtherFeature 语言实例
        self.update_texts()
        self.refresh_version()
        self.check_system_requirements()
        self.set_font_style()  # 设置字体样式

    # 更新文本
    def update_texts(self):
        self.version_label.config(text=self.translator.translate("current_pcm_version"))
        self.refresh_button.config(text=self.translator.translate("refresh"))
        self.update_result_textbox_context_menu()  # 更新右键菜单的文本
        self.system_requirement_label.config(text=self.translator.translate("system_requirements_checking"))
        self.hint_label.config(text=self.translator.translate("notice_select_option"))
        self.execute_button.config(text=self.translator.translate("main_execute_button"))
        self.cancel_button.config(text=self.translator.translate("main_cancel_button"))
        self.run_as_administrator_button.config(text=self.translator.translate("run_as_administrator"))  # 更新以管理员身份运行按钮的文本
        self.main_combobox.config(values=[self.translator.translate("select_option"),
                                          self.translator.translate("main_project"),
                                          self.translator.translate("install_project"),
                                          self.translator.translate("uninstall_project"),
                                          self.translator.translate("other_project")])
        self.main_combobox.current(0)
        self.update_feature_combobox(None)

    # 更新功能组合框
    def update_feature_combobox(self, event):
        selection = self.main_combobox.get()
        options = {
            self.translator.translate("main_project"): [self.translator.translate("repair_pc_manager"),
                                                        self.translator.translate("get_pc_manager_logs")],
            self.translator.translate("install_project"): [self.translator.translate("download_from_winget"),
                                                           self.translator.translate("download_from_store"),
                                                           self.translator.translate("install_for_all_users"),
                                                           self.translator.translate("install_for_current_user")],
            self.translator.translate("uninstall_project"): [self.translator.translate("uninstall_for_all_users"),
                                                             self.translator.translate("uninstall_for_current_user"),
                                                             self.translator.translate("uninstall_beta")],
            self.translator.translate("other_project"): [self.translator.translate("view_installed_antivirus"),
                                                         self.translator.translate("developer_options"),
                                                         self.translator.translate("repair_edge_wv2_setup"),
                                                         self.translator.translate("pc_manager_faq"),
                                                         self.translator.translate("install_wv2_runtime"),
                                                         # self.translator.translate("join_preview_program"),
                                                         self.translator.translate("restart_pc_manager_service"),
                                                         self.translator.translate("switch_region_to_cn")]
        }

        # 获取当前选择的语言
        current_language = self.language_combobox.get()

        # 需要隐藏的选项
        hidden_options = [self.translator.translate("pc_manager_faq"),
                          # self.translator.translate("join_preview_program"),
                          self.translator.translate("switch_region_to_cn")]

        # 如果当前语言是 en-us 或 zh-tw 或其它语言，隐藏特定选项
        if current_language in [self.translator.translate("lang_en-us"),
                                self.translator.translate("lang_zh-tw")]:
            for key in options:
                options[key] = [option for option in options[key] if option not in hidden_options]

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
            self.result_textbox.config(state="normal")
            self.result_textbox.delete("1.0", tk.END)  # 清空 TextBox 的内容
            feature = self.feature_combobox.get()
            executing_message = f"{self.translator.translate('main_executing')} {feature} {self.translator.translate('main_operation')}"
            self.result_textbox.insert(tk.END, executing_message + "\n")
            self.result_textbox.config(state="disabled")

            def run_feature():
                result = ""
                # MainFeature
                if feature == self.translator.translate("repair_pc_manager"):
                    result = self.main_feature.repair_pc_manager()
                elif feature == self.translator.translate("get_pc_manager_logs"):
                    result = self.main_feature.get_pc_manager_logs()

                # InstallationFeature
                elif feature == self.translator.translate("download_from_winget"):
                    result = self.installation_feature.download_from_winget()
                elif feature == self.translator.translate("download_from_store"):
                    result = self.installation_feature.download_from_store()
                elif feature == self.translator.translate("install_for_all_users"):
                    result = self.installation_feature.install_for_all_users()
                elif feature == self.translator.translate("install_for_current_user"):
                    result = self.installation_feature.install_for_current_user()

                # UninstallationFeature
                elif feature == self.translator.translate("uninstall_for_all_users"):
                    result = self.uninstallation_feature.uninstall_for_all_users()
                elif feature == self.translator.translate("uninstall_for_current_user"):
                    result = self.uninstallation_feature.uninstall_for_current_user()
                elif feature == self.translator.translate("uninstall_beta"):
                    result = self.uninstallation_feature.uninstall_beta()

                # OtherFeature
                elif feature == self.translator.translate("view_installed_antivirus"):
                    result = self.other_feature.view_installed_antivirus()
                elif feature == self.translator.translate("developer_options"):
                    result = self.other_feature.developer_options()
                elif feature == self.translator.translate("repair_edge_wv2_setup"):
                    result = self.other_feature.repair_edge_wv2_setup()
                elif feature == self.translator.translate("pc_manager_faq"):
                    result = self.other_feature.pc_manager_faq()
                elif feature == self.translator.translate("install_wv2_runtime"):
                    result = self.other_feature.install_wv2_runtime(self)
                # elif feature == self.translator.translate("join_preview_program"):
                #     result = self.other_feature.join_preview_program()
                elif feature == self.translator.translate("restart_pc_manager_service"):
                    result = self.other_feature.restart_pc_manager_service()
                elif feature == self.translator.translate("switch_region_to_cn"):
                    result = self.other_feature.switch_region_to_cn()
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
        version = get_current_windows_version()
        if version:
            self.version_label.config(text=f"{self.translator.translate('current_pcm_version')}{version}")
        else:
            self.version_label.config(text=self.translator.translate("cannot_read_pcm_version"))

    # 检测系统要求
    def check_system_requirements(self):
        system_status = check_system_requirements(self.translator.locale)
        self.system_requirement_label.config(text=system_status)

if __name__ == "__main__":
    app = MSPCManagerHelper()
    app.mainloop()