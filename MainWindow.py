import tkinter as tk
from tkinter import ttk, messagebox
from getVersionNumber import detect_version
from checkSystemRequirements import check_system_requirements
from Translator import Translator

class MSPCManagerHelper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MSPCManagerHelper Preview v24816 - we11A")
        self.geometry("854x480")
        self.resizable(False, False)
        self.configure(bg="white")

        self.translator = Translator('en-us')
        self.create_widgets()

    def create_widgets(self):
        # 语言选择组合框
        self.language_combobox = ttk.Combobox(self, values=["English (United States)", "中文 (简体)", "中文 (繁體)"], state="readonly")
        self.language_combobox.current(0)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)
        self.language_combobox.place(x=55, y=80, width=200, height=25)

        # 检测版本的 TextBlock 和刷新按钮
        version_frame = tk.Frame(self, bg="white")
        version_frame.place(x=55, y=110)

        self.version_label = tk.Label(version_frame, text=self.translator.translate("current_version"), bg="white")
        self.version_label.pack(side="left", padx=(0, 10))

        self.refresh_button = tk.Button(version_frame, text=self.translator.translate("refresh"), command=self.refresh_version, width=5, height=1, font=("Arial", 10))
        self.refresh_button.pack(side="left")

        # 系统要求检测
        self.system_requirement_label = tk.Label(self, text=self.translator.translate("system_requirements_checking"), bg="white", wraplength=400, padx=0, pady=10)
        self.system_requirement_label.place(x=55, y=140)

        # 提示信息
        self.hint_label = tk.Label(self, text=self.translator.translate("notice_select_option"), bg="white")
        self.hint_label.place(x=55, y=210)

        # 第一个组合框
        self.main_combobox = ttk.Combobox(self, values=[self.translator.translate("select_option"), self.translator.translate("main_project"), self.translator.translate("install_project"), self.translator.translate("uninstall_project"), self.translator.translate("other_project")], state="readonly")
        self.main_combobox.current(0)
        self.main_combobox.bind("<<ComboboxSelected>>", self.update_feature_combobox)
        self.main_combobox.place(x=55, y=260, width=300, height=25)

        # 第二个组合框
        self.feature_combobox = ttk.Combobox(self, state="readonly")
        self.feature_combobox.place(x=55, y=310, width=300, height=25)

        # 执行按钮
        self.execute_button = tk.Button(self, text=self.translator.translate("execute"), command=self.execute_feature, width=10, height=1)
        self.execute_button.place(x=55, y=360)

        # 取消按钮
        self.cancel_button = tk.Button(self, text=self.translator.translate("cancel"), command=self.cancel_feature, state="disabled", width=10, height=1)
        self.cancel_button.place(x=165, y=360)

        # 结果输出框
        self.result_textbox = tk.Text(self, wrap="word", height=20, width=50, state="disabled")
        self.result_textbox.place(x=460, y=80)

        # 初始检测版本号和系统要求
        self.refresh_version()
        self.check_system_requirements()

    def change_language(self, event):
        selected_language = self.language_combobox.get()
        if selected_language == "English (United States)":
            self.translator = Translator('en-us')
        elif selected_language == "中文 (简体)":
            self.translator = Translator('zh-cn')
        elif selected_language == "中文 (繁體)":
            self.translator = Translator('zh-tw')
        self.update_texts()
        self.refresh_version()
        self.check_system_requirements()

    def update_texts(self):
        self.version_label.config(text=self.translator.translate("current_version"))
        self.refresh_button.config(text=self.translator.translate("refresh"))
        self.system_requirement_label.config(text=self.translator.translate("system_requirements_checking"))
        self.hint_label.config(text=self.translator.translate("notice_select_option"))
        self.execute_button.config(text=self.translator.translate("execute"))
        self.cancel_button.config(text=self.translator.translate("cancel"))
        self.main_combobox.config(values=[self.translator.translate("select_option"), self.translator.translate("main_project"), self.translator.translate("install_project"), self.translator.translate("uninstall_project"), self.translator.translate("other_project")])
        self.main_combobox.current(0)
        self.update_feature_combobox(None)

    def update_feature_combobox(self, event):
        selection = self.main_combobox.get()
        options = {
            self.translator.translate("main_project"): [self.translator.translate("fix_pc_manager"), self.translator.translate("get_pc_manager_logs")],
            self.translator.translate("install_project"): [self.translator.translate("download_from_winget"), self.translator.translate("download_from_store"), self.translator.translate("install_for_all_users"), self.translator.translate("install_for_current_user")],
            self.translator.translate("uninstall_project"): [self.translator.translate("uninstall_for_all_users"), self.translator.translate("uninstall_for_current_user"), self.translator.translate("uninstall_beta")],
            self.translator.translate("other_project"): [self.translator.translate("view_installed_antivirus"), self.translator.translate("developer_options"), self.translator.translate("fix_edge_runtime"), self.translator.translate("pc_manager_faq"), self.translator.translate("install_edge_runtime"), self.translator.translate("join_preview_program"), self.translator.translate("restart_pc_manager_service"), self.translator.translate("switch_region_to_china")]
        }
        self.feature_combobox['values'] = options.get(selection, [])
        self.feature_combobox.set("")

    def execute_feature(self):
        if self.main_combobox.get() == self.translator.translate("select_option") or not self.feature_combobox.get():
            messagebox.showwarning(self.translator.translate("warning"), self.translator.translate("select_function"))
        else:
            self.result_textbox.config(state="normal")
            self.result_textbox.delete("1.0", tk.END)  # 清空 TextBox 的内容
            self.result_textbox.insert(tk.END,
                                       f"{self.translator.translate('executing')} {self.feature_combobox.get()} {self.translator.translate('operation')}\n")
            self.result_textbox.config(state="disabled")
            self.cancel_button.config(state="normal")

    def cancel_feature(self):
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, f"{self.translator.translate('user_cancelled')}\n")
        self.result_textbox.config(state="disabled")
        self.cancel_button.config(state="disabled")

    def refresh_version(self):
        version = detect_version()
        if version:
            self.version_label.config(text=f"{self.translator.translate('current_version')}{version}")
        else:
            self.version_label.config(text=self.translator.translate("cannot_read_version"))

    def check_system_requirements(self):
        system_status = check_system_requirements(self.translator.locale)
        self.system_requirement_label.config(text=system_status)

if __name__ == "__main__":
    app = MSPCManagerHelper()
    app.mainloop()
