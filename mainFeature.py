import os
import shutil
import subprocess
import winreg
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
import sys

class MainFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox

    def textbox(self, message):
        message = str(message)
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disable")
        self.result_textbox.update_idletasks()  # 刷新界面

    def repair_pc_manager(self):
        return self.translator.translate("feature_unavailable")

    def get_pc_manager_logs(self):
        # 获取进程 PID
        def get_pid(processes: list):
            pids = []
            result = os.popen('tasklist.exe').read()
            for process in processes:
                process = process[:25]
                if process in result:
                    for line in result.split(process)[1:]:
                        pids.append((process, line.split()[0]))
            return pids

        try:
            # 设置路径变量
            date_str = datetime.now().strftime(datetime.now().isoformat().replace(":", "."))
            logs_destination = os.path.join(os.getenv('UserProfile'), 'Desktop', 'Microsoft PC Manager Logs', date_str)
            app_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Store', 'Common')
            setup_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Store', 'Setup')
            exe_setup_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Setup')
            logs_zip_archive = os.path.join(os.getenv('UserProfile'), 'Desktop')

            # 创建目标目录
            os.makedirs(logs_destination, exist_ok=True)
            os.makedirs(os.path.join(logs_destination, 'Common'), exist_ok=True)

            # 复制使用日志
            try:
                for file_name in os.listdir(app_logs_source):
                    if file_name.endswith('.log'):
                        full_file_name = os.path.join(app_logs_source, file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, os.path.join(logs_destination, 'Common'))
                self.textbox(self.translator.translate("retrieve_pc_manager_app_logs_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_app_logs_error") + f": {str(e)}")

            # 复制安装日志
            try:
                shutil.copytree(setup_logs_source, os.path.join(logs_destination, 'Setup'), dirs_exist_ok=True)
                self.textbox(self.translator.translate("retrieve_pc_manager_setup_logs_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_setup_logs_error") + f": {str(e)}")

            # 复制 EXE 安装日志
            try:
                shutil.copytree(exe_setup_logs_source, os.path.join(logs_destination, 'Windows Master Setup'),
                                dirs_exist_ok=True)
                self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_error") + f": {str(e)}")

            # 复制 Application.evtx
            try:
                system_root = os.getenv('SystemRoot')
                application_evtx_source = os.path.join(system_root, 'System32', 'winevt', 'Logs', 'Application.evtx')
                shutil.copy(application_evtx_source, logs_destination)
                self.textbox(self.translator.translate("retrieve_pc_manager_evtx_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_evtx_error") + f": {str(e)}")

            # 弹出提示框询问用户是否选择获取 Dumps
            response_for_dumps = messagebox.askyesnocancel(
                self.translator.translate("ask_to_retrieve_pc_manager_dumps_notice"),
                self.translator.translate("ask_to_retrieve_pc_manager_dumps")
            )

            if response_for_dumps:
                # 读取注册表值并使用 procdump
                dumps_destination = os.path.join(logs_destination, 'Dumps')
                os.makedirs(dumps_destination, exist_ok=True)
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                        processor_architecture = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]

                    # 根据处理器架构设定 procdump 变量
                    if processor_architecture == "AMD64":
                        if hasattr(sys, '_MEIPASS'):
                            procdump_path = os.path.join(sys._MEIPASS, "tools", "procdump", "procdump64.exe")
                        else:
                            procdump_path = os.path.join("tools", "procdump", "procdump64.exe")
                    elif processor_architecture == "ARM64":
                        if hasattr(sys, '_MEIPASS'):
                             procdump_path = os.path.join(sys._MEIPASS, "tools", "procdump", "procdump64a.exe")
                        else:
                            procdump_path = os.path.join("tools", "procdump", "procdump64a.exe")
                    else:
                        self.textbox(self.translator.translate("no_match_procdump_version"))
                        return "\n.join(messages)"

                    # 输出许可协议
                    self.textbox(self.translator.translate("procdump_agreement"))

                    # 获取进程 PID 并生成转储文件
                    processes = ["MSPCManager.exe", "MSPCManagerService.exe", "Microsoft.WIC.PCWndManager.Plugin.exe",
                                 "MSPCWndManager.exe"]
                    pids = get_pid(processes)
                    for process, pid in pids:
                        self.textbox('\n' + self.translator.translate("retrieving_progress_name") + f": {process}")

                        dump_file = os.path.join(dumps_destination, f"{process}_{date_str}.dmp")
                        try:
                            result = subprocess.run([procdump_path, "-ma", pid, dump_file], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            self.textbox('\n'.join(result.stdout.split('\n')[5:-2]))
                            self.textbox(self.translator.translate("retrieve_pc_manager_dumps_success") + f": {dump_file}")
                        except subprocess.CalledProcessError as e:
                            self.textbox(self.translator.translate("retrieve_pc_manager_dumps_error") + f": {str(e)}")

                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_logs_error") + f": {str(e)}")

            # 获取计算机信息并保存到 ComputerInfo.txt
            try:
                computer_info_path = os.path.join(logs_destination, 'ComputerInfo.txt')
                with open(computer_info_path, 'w', encoding='utf-8') as file:
                    result = subprocess.run(['powershell', '-Command',
                                             'Get-ComputerInfo | Select-Object CsName, WindowsVersion, OSDisplayVersion, WindowsBuildLabEx, OsArchitecture, WindowsEditionId, OsLanguage, BiosManufacturer, BiosVersion, CsManufacturer, CsModel, CsTotalPhysicalMemory, CsSystemType, TimeZone, OsLocale, OsUILanguage'],
                                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    file.write(result.stdout)
                self.textbox(self.translator.translate("retrieve_computer_info_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_computer_info_error") + f": {str(e)}")

            # 压缩日志文件夹
            self.textbox("\n" + self.translator.translate("compressing_pc_manager_logs"))
            zip_file_name = f"{self.translator.translate('pc_manager_logs_zip_archive')}_{date_str}"
            zip_file_path = os.path.join(logs_zip_archive, zip_file_name)
            shutil.make_archive(zip_file_path, 'zip', logs_destination)
            self.textbox(self.translator.translate("path_to_pc_manager_logs_zip_archive") + f": {zip_file_path}.zip")
            messagebox.showwarning(self.translator.translate("warning"),
                                   self.translator.translate("do_not_share_log_files_with_untrusted_users"))
            self.textbox("\n" + self.translator.translate("do_not_share_log_files_with_untrusted_users"))
            messages = self.translator.translate("retrieve_pc_manager_logs_and_dumps_success")

        except Exception as e:
            messages = self.translator.translate("retrieve_pc_manager_logs_error") + f": {str(e)}"

        return messages

    def debug_dev_mode(self):
        try:
            messages = self.translator.translate("feature_unavailable")
        except Exception as e:
            messages = self.translator.translate("debug_dev_mode_error") + f": {str(e)}"
        return messages