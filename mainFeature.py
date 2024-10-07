import os
import shutil
import subprocess
import winreg
from datetime import datetime
from tkinter import messagebox

class MainFeature:
    def __init__(self, translator):
        self.translator = translator

    def repair_pc_manager(self):
        return self.translator.translate("feature_unavailable")

    def get_pc_manager_logs(self):
        messages = []
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
                messages.append(self.translator.translate("retrieve_pc_manager_app_logs_success"))
            except Exception as e:
                messages.append(self.translator.translate("retrieve_pc_manager_app_logs_error") + f": {str(e)}")

            # 复制安装日志
            try:
                shutil.copytree(setup_logs_source, os.path.join(logs_destination, 'Setup'), dirs_exist_ok=True)
                messages.append(self.translator.translate("retrieve_pc_manager_setup_logs_success"))
            except Exception as e:
                messages.append(self.translator.translate("retrieve_pc_manager_setup_logs_error") + f": {str(e)}")

            # 复制 EXE 安装日志
            try:
                shutil.copytree(exe_setup_logs_source, os.path.join(logs_destination, 'Windows Master Setup'),
                                dirs_exist_ok=True)
                messages.append(self.translator.translate("retrieve_pc_manager_exe_setup_logs_success"))
            except Exception as e:
                messages.append(self.translator.translate("retrieve_pc_manager_exe_setup_logs_error") + f": {str(e)}")

            # 复制 Application.evtx
            try:
                system_root = os.getenv('SystemRoot')
                application_evtx_source = os.path.join(system_root, 'System32', 'winevt', 'Logs', 'Application.evtx')
                shutil.copy(application_evtx_source, logs_destination)
                messages.append(self.translator.translate("retrieve_pc_manager_evtx_success"))
            except Exception as e:
                messages.append(self.translator.translate("retrieve_pc_manager_evtx_error") + f": {str(e)}")

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
                        procdump_path = os.path.join("tools", "procdump", "procdump64.exe")
                    elif processor_architecture == "ARM64":
                        procdump_path = os.path.join("tools", "procdump", "procdump64a.exe")
                    else:
                        messages.append(self.translator.translate("no_match_procdump_version"))
                        return "\n.join(messages)"

                    # 输出许可协议
                    messages.append(self.translator.translate("procdump_agreement"))

                    # 获取进程 PID 并生成转储文件
                    processes = ["MSPCManager.exe", "MSPCManagerService.exe", "Microsoft.WIC.PCWndManager.Plugin.exe",
                                 "MSPCWndManager.exe"]
                    for process in processes:
                        try:
                            messages.append(self.translator.translate("retrieving_progress_name") + f": {process}")
                            tasklist_proc = subprocess.Popen(["tasklist.exe"], stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
                            findstr_proc = subprocess.Popen(["findstr.exe", process], stdin=tasklist_proc.stdout,
                                                            stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            tasklist_proc.stdout.close()  # 关闭 tasklist_proc 的标准输出管道，以便在 findstr_proc 退出时 tasklist_proc 能够接收到 SIGPIPE 信号
                            result = findstr_proc.communicate()[0]

                            if result:
                                pid = result.split()[1]
                                dump_file = os.path.join(dumps_destination, f"{process}_{date_str}.dmp")
                                subprocess.run([procdump_path, "-ma", pid, dump_file], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                messages.append(
                                    self.translator.translate("retrieve_pc_manager_dumps_success") + f": {dump_file}")
                        except subprocess.CalledProcessError as e:
                            messages.append(self.translator.translate("retrieve_pc_manager_dumps_error") + f": {str(e)}")
                            messages.append("")

                except Exception as e:
                    messages.append(self.translator.translate("retrieve_pc_manager_logs_error") + f": {str(e)}")

            # 压缩日志文件夹
            zip_file_name = self.translator.translate("pc_manager_logs_zip_archive")
            zip_file_path = os.path.join(logs_zip_archive, zip_file_name)
            shutil.make_archive(zip_file_path, 'zip', logs_destination)
            messages.append(self.translator.translate("path_to_pc_manager_logs_zip_archive") + f": {zip_file_path}.zip")
            messages.append("")
            messages.append(self.translator.translate("retrieve_pc_manager_logs_and_dumps_success"))

        except Exception as e:
            messages.append(self.translator.translate("retrieve_pc_manager_logs_error") + f": {str(e)}")

        return "\n".join(messages)

    def debug_dev_mode(self):
        messages = []
        try:
            messages.append(self.translator.translate("feature_unavailable"))
        except Exception as e:
            messages.append(self.translator.translate("debug_dev_mode_error") + f": {str(e)}")
        return "\n".join(messages)