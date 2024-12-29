import os
import shutil
import subprocess
import tkinter as tk
import sys
import winreg
from datetime import datetime
from tkinter import messagebox
from otherFeature import OtherFeature
from uninstallationFeature import UninstallationFeature

class MainFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox
        self.other_feature = OtherFeature(self.translator, self.result_textbox)
        self.uninstallation_feature = UninstallationFeature(self.translator, self.result_textbox)

    def textbox(self, message):
        message = str(message)
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disable")
        self.result_textbox.update_idletasks()  # 刷新界面

    def refresh_result_textbox(self):
        self.other_feature.result_textbox = self.result_textbox
        self.uninstallation_feature.result_textbox = self.result_textbox

    def repair_pc_manager(self):
        try:
            response = messagebox.askyesno(self.translator.translate("repair_pc_manager_notice"),
                                           self.translator.translate("repair_pc_manager_to_perform"))
            if response:
                self.textbox(self.uninstallation_feature.uninstall_for_all_users_in_dism())
                self.textbox(self.uninstallation_feature.uninstall_pc_manager_beta())
                self.textbox(self.other_feature.repair_edge_wv2_setup())
                return self.translator.translate("repair_pc_manager_success")
            else:
                return self.translator.translate("user_canceled")
        except Exception as e:
            return f"{self.translator.translate('repair_pc_manager_error')}: {str(e)}"

    def get_pc_manager_logs(self):
        # 获取进程 PID
        def get_pid(processes: list):
            pc_manager_processes_pids = []
            pc_manager_processes_pids_result = os.popen('tasklist.exe').read()
            for process in processes:
                process = process[:25]
                if process in pc_manager_processes_pids_result:
                    for line in pc_manager_processes_pids_result.split(process)[1:]:
                        pc_manager_processes_pids.append((process, line.split()[0]))
            return pc_manager_processes_pids

        try:
            # 设置路径变量
            date_str = datetime.now().strftime(datetime.now().isoformat().replace(":", "."))
            logs_destination = os.path.join(os.getenv('UserProfile'), 'Desktop', 'Microsoft PC Manager Logs', date_str)
            program_logs_source_path = os.path.join(os.getenv('ProgramData'), 'Windows Master Store')
            app_logs_source = os.path.join(program_logs_source_path, 'Common')
            setup_logs_source = os.path.join(program_logs_source_path, 'Setup')
            service_logs_source = os.path.join(program_logs_source_path, 'ServiceData')
            exe_setup_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Setup')
            logs_zip_archive = os.path.join(os.getenv('UserProfile'), 'Desktop')

            isfile = [file for file in os.listdir(program_logs_source_path) if not os.path.isfile(os.path.join(program_logs_source_path, file))]
            filtered = ['Common', 'Setup', 'ServiceData']
            other_logs_destinations = []
            for name in isfile:
                try:
                    if any(['.log' in file for file in os.listdir(os.path.join(program_logs_source_path, name))]) and name not in filtered:
                        other_logs_destinations.append((os.path.join(program_logs_source_path, name), name))
                except:
                    pass

            # 创建目标目录
            os.makedirs(logs_destination, exist_ok=True)
            os.makedirs(os.path.join(logs_destination, 'Common'), exist_ok=True)

            # 读取注册表值并使用 NSudoLC
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                    processor_architecture = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]

                # 根据处理器架构设定 NSudoLC 变量
                if processor_architecture == "AMD64":
                    if hasattr(sys, '_MEIPASS'):
                        nsudolc_path = os.path.join(sys._MEIPASS, "tools", "NSudo", "NSudoLC_x64.exe")
                    else:
                        nsudolc_path = os.path.join("tools", "NSudo", "NSudoLC_x64.exe")
                elif processor_architecture == "ARM64":
                    if hasattr(sys, '_MEIPASS'):
                        nsudolc_path = os.path.join(sys._MEIPASS, "tools", "NSudo", "NSudoLC_ARM64.exe")
                    else:
                        nsudolc_path = os.path.join("tools", "NSudo", "NSudoLC_ARM64.exe")
                else:
                    self.textbox(self.translator.translate("no_match_nsudo_version"))
                    return "\n.join(messages)"
            except Exception as e:
                self.textbox(self.translator.translate("no_match_nsudo_version") + f": {str(e)}")
                return "\n.join(messages)"

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

            # 复制服务日志
            try:    # 使用 cmd.exe 拉起进程时需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                nsudolc_copy_svc_logs_cmd = [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe", service_logs_source,
                                 os.path.join(logs_destination, 'ServiceData'), "/E", "/H", "/C", "/I"]
                result = subprocess.run(nsudolc_copy_svc_logs_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode == 0:
                    self.textbox(self.translator.translate("retrieve_pc_manager_service_logs_success"))
                else:
                    self.textbox(
                        self.translator.translate("retrieve_pc_manager_service_logs_error") + f": {result.stdout}")
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_service_logs_error") + f": {str(e)}")

            # 复制 EXE 安装日志
            try:
                shutil.copytree(exe_setup_logs_source, os.path.join(logs_destination, 'Windows Master Setup'), dirs_exist_ok=True)
                self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_error") + f": {str(e)}")

            # 复制未列出的日志
            for destination, file_name in other_logs_destinations:
                try:    # 使用 cmd.exe 拉起进程时需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    nsudolc_copy_other_logs_cmd = [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe", destination,
                                        os.path.join(os.path.join(logs_destination, 'OtherLogs'), file_name), "/E", "/H", "/C", "/I"]
                    result = subprocess.run(nsudolc_copy_other_logs_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_other_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_other_logs_error") + f": {result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_other_logs_error") + f": {str(e)}")

            # 复制 Application.evtx
            try:
                system_root = os.getenv('SystemRoot')
                application_evtx_source = os.path.join(system_root, 'System32', 'winevt', 'Logs', 'Application.evtx')
                shutil.copy(application_evtx_source, logs_destination)
                self.textbox(self.translator.translate("retrieve_pc_manager_evtx_success"))
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_evtx_error") + f": {str(e)}")

            # 弹出提示框询问用户是否选择获取 Dumps
            response_for_dumps = messagebox.askyesno(
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
                    pc_manager_processes_pids = get_pid(processes)
                    for process, pid in pc_manager_processes_pids:
                        self.textbox('\n' + self.translator.translate("retrieving_progress_name") + f": {process}")

                        dump_file = os.path.join(dumps_destination, f"{process}_{date_str}.dmp")
                        try:
                            result = subprocess.run([procdump_path, "-ma", pid, dump_file], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if result.returncode == 0:
                                self.textbox('\n'.join(result.stdout.split('\n')[5:-2]))
                                self.textbox(self.translator.translate("retrieve_pc_manager_dumps_success") + f": {dump_file}")
                            else:
                                self.textbox(self.translator.translate("retrieve_pc_manager_dumps_error") + f": {result.stdout}")
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