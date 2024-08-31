import tkinter as tk
from tkinter import ttk, messagebox
from getVersionNumber import detect_version
from checkSystemRequirements import check_system_requirements
from Translator import Translator
from otherFeature import OtherFeature

class MSPCManagerHelper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MSPCManagerHelper Preview v24831 - we11A")
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(bg="white")

        self.translator = Translator('en-us')
        self.other_feature = OtherFeature(self.translator)
        self.create_widgets()

    # 创建窗口部件
    def create_widgets(self):
        # 语言选择组合框
        self.language_combobox = ttk.Combobox(self, values=["English (United States)", "中文 (简体)", "中文 (繁體)"], state="readonly")
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
        self.refresh_button = tk.Button(version_frame, text=self.translator.translate("refresh"), command=self.refresh_version, width=10, height=1, font=("Segoe UI", 10))
        self.refresh_button.pack(side="left")

        # 系统要求检测
        self.system_requirement_label = tk.Label(self, text=self.translator.translate("system_requirements_checking"), bg="white", wraplength=400, padx=0, pady=10)
        self.system_requirement_label.place(x=35, y=150)

        # 提示信息
        self.hint_label = tk.Label(self, text=self.translator.translate("notice_select_option"), bg="white")
        self.hint_label.place(x=35, y=210)

        # 第一个组合框
        self.main_combobox = ttk.Combobox(self, values=[self.translator.translate("select_option"), self.translator.translate("main_project"), self.translator.translate("install_project"), self.translator.translate("uninstall_project"), self.translator.translate("other_project")], state="readonly")
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

        # 结果输出框
        self.result_textbox = tk.Text(self, wrap="word", state="disabled", bg="lightgray")
        self.result_textbox.place(x=435, y=80, width=400, height=310)

        # 初始检测版本号和系统要求
        self.refresh_version()
        self.check_system_requirements()

        # 创建右键菜单
        self.create_result_textbox_context_menu()
        self.update_result_textbox_context_menu()  # 确保调用 update_result_textbox_context_menu 方法
        self.result_textbox.bind("<Button-3>", self.show_result_textbox_context_menu)

    # 设置字体样式
    def update_result_textbox_context_menu(self):
        self.context_menu.entryconfig(0, label=self.translator.translate("main_copy"))

    # 创建右键菜单
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

    # 更改语言
    def change_language(self, event):
        selected_language = self.language_combobox.get()
        if selected_language == "English (United States)":
            self.translator = Translator('en-us')
        elif selected_language == "中文 (简体)":
            self.translator = Translator('zh-cn')
        elif selected_language == "中文 (繁體)":
            self.translator = Translator('zh-tw')
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
        self.main_combobox.config(values=[self.translator.translate("select_option"), self.translator.translate("main_project"), self.translator.translate("install_project"), self.translator.translate("uninstall_project"), self.translator.translate("other_project")])
        self.main_combobox.current(0)
        self.update_feature_combobox(None)

    # 更新功能组合框
    def update_feature_combobox(self, event):
        selection = self.main_combobox.get()
        options = {
            self.translator.translate("main_project"): [self.translator.translate("repair_pc_manager"), self.translator.translate("get_pc_manager_logs")],
            self.translator.translate("install_project"): [self.translator.translate("download_from_winget"), self.translator.translate("download_from_store"), self.translator.translate("install_for_all_users"), self.translator.translate("install_for_current_user")],
            self.translator.translate("uninstall_project"): [self.translator.translate("uninstall_for_all_users"), self.translator.translate("uninstall_for_current_user"), self.translator.translate("uninstall_beta")],
            self.translator.translate("other_project"): [self.translator.translate("view_installed_antivirus"), self.translator.translate("developer_options"), self.translator.translate("repair_edge_wv2_setup"), self.translator.translate("pc_manager_faq"), self.translator.translate("install_wv2_runtime"), self.translator.translate("join_preview_program"), self.translator.translate("restart_pc_manager_service"), self.translator.translate("switch_region_to_china")]
        }
        self.feature_combobox['values'] = options.get(selection, [])
        self.feature_combobox.set("")

    # 执行功能
    def execute_feature(self):
        if self.main_combobox.get() == self.translator.translate("select_option") or not self.feature_combobox.get():
            messagebox.showwarning(self.translator.translate("warning"), self.translator.translate("select_function"))
        else:
            self.result_textbox.config(state="normal")
            self.result_textbox.delete("1.0", tk.END)  # 清空 TextBox 的内容
            feature = self.feature_combobox.get()
            executing_message = f"{self.translator.translate('main_executing')} {feature} {self.translator.translate('main_operation')}"
            self.result_textbox.insert(tk.END, executing_message + "\n")
            result = ""
            # mainFeature.py 中的语言功能调用
            # installationFeature.py 中的语言功能调用
            # uninstallationFeature.py 中的语言功能调用
            # otherFeature.py 中的语言功能调用
            if feature == self.translator.translate("view_installed_antivirus"):
                result = self.other_feature.view_installed_antivirus()
            elif feature == self.translator.translate("developer_options"):
                result = self.other_feature.developer_options()
            elif feature == self.translator.translate("repair_edge_wv2_setup"):
                result = self.other_feature.repair_edge_wv2_setup()
            elif feature == self.translator.translate("pc_manager_faq"):
                result = self.other_feature.pc_manager_faq()
            # 其他功能的调用可以在这里继续添加
            self.result_textbox.insert(tk.END, result)
            # self.result_textbox.insert(tk.END, f"{self.translator.translate('task_completed')}\n")
            self.result_textbox.config(state="disabled")
            self.cancel_button.config(state="normal")

    # 取消功能
    def cancel_feature(self):
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, f"{self.translator.translate('user_cancelled')}\n")
        self.result_textbox.config(state="disabled")
        self.cancel_button.config(state="disabled")

    # 设置字体样式
    def set_font_style(self):
        font_styles = {
            "English (United States)": ("Segoe UI", 10),
            "中文 (简体)": ("微软雅黑", 10),
            "中文 (繁體)": ("微软雅黑", 10),
            # 在这里添加更多语言及其对应的字体样式
        }

        selected_language = self.language_combobox.get()
        font_style = font_styles.get(selected_language, ("Segoe UI", 10))  # 如果未找到语言，默认使用 Segoe UI

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
        version = detect_version()
        if version:
            self.version_label.config(text=f"{self.translator.translate('current_pcm_version')}{version}")
        else:
            self.version_label.config(text=self.translator.translate("cannot_read_version"))

    # 检测系统要求
    def check_system_requirements(self):
        system_status = check_system_requirements(self.translator.locale)
        self.system_requirement_label.config(text=system_status)

if __name__ == "__main__":
    app = MSPCManagerHelper()
    app.mainloop()