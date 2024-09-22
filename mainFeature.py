import os
import shutil
import subprocess
import winreg
import zipfile
from datetime import datetime

class MainFeature:
    def __init__(self, translator):
        self.translator = translator

    def repair_pc_manager(self):
        return self.translator.translate("feature_unavailable")

    def get_pc_manager_logs(self):
        date_str = datetime.now().strftime(datetime.now().isoformat().replace(":", "."))
        logs_destination = os.path.join(os.getenv('UserProfile'), 'Desktop', 'Microsoft PC Manager Logs', date_str)
        dumps_destination = os.path.join(logs_destination, 'Dumps')

        try:
            # 设置路径变量
            app_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Store', 'Common')
            setup_logs_source = os.path.join(os.getenv('ProgramData'), 'Windows Master Store', 'Setup')

            # 创建目标目录
            os.makedirs(os.path.join(logs_destination, 'Common'), exist_ok=True)
            os.makedirs(dumps_destination, exist_ok=True)

            # 复制 Microsoft PC Manager 日志
            for file_name in os.listdir(app_logs_source):
                if file_name.endswith('.log'):
                    full_file_name = os.path.join(app_logs_source, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, os.path.join(logs_destination, 'Common'))

            # 复制安装日志
            shutil.copytree(setup_logs_source, os.path.join(logs_destination, 'Setup'))

            # 复制 Application.evtx
            application_evtx_source = os.path.join(os.getenv('SystemRoot'), 'System32', 'winevt', 'Logs', 'Application.evtx')
            shutil.copy(application_evtx_source, logs_destination)

            logs_result = self.translator.translate("retrieve_pc_manager_logs_success")
        except Exception as e:
            logs_result = f"{self.translator.translate('retrieve_pc_manager_logs_error')}: {str(e)}"

        try:
            # 获取 PIDs
            pids = MainFeature.get_pc_manager_pids()

            # 获取处理器架构
            processor_architecture = MainFeature.get_processor_architecture()

            # 确定 procdump 版本
            if processor_architecture == "AMD64":
                procdump_exe = os.path.join("tools", "procdump", "procdump64.exe")
            elif processor_architecture == "ARM64":
                procdump_exe = os.path.join("tools", "procdump", "procdump64a.exe")
            else:
                procdump_exe = os.path.join("tools", "procdump", "procdump64.exe")

            # 运行 procdump
            for process_name, pid in pids.items():
                dumps_file = os.path.join(dumps_destination, f"{process_name}_{pid}_{date_str}.dmp")
                subprocess.run([procdump_exe, "-ma", pid, dumps_file], check=True)

            dumps_result = self.translator.translate("retrieve_pc_manager_dumps_success")
        except Exception as e:
            dumps_result = f"{self.translator.translate('retrieve_pc_manager_dumps_error')}: {str(e)}"

        try:
            # 输出 compressing_pc_manager_log_files
            print(self.translator.translate("compressing_pc_manager_log_files"))

            # 压缩文件夹
            zip_file_name = self.translator.translate("pc_manager_logs_zip_archive")
            zip_file_path = os.path.join(os.getenv('UserProfile'), 'Desktop', f"{zip_file_name}.zip")
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(logs_destination):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), logs_destination))

            final_result = self.translator.translate("retrieve_pc_manager_logs_and_dumps_success")
        except Exception as e:
            final_result = f"{self.translator.translate('retrieve_pc_manager_logs_and_dumps_error')}: {str(e)}"

        return f"{logs_result}\n{dumps_result}\n{final_result}"

    @staticmethod
    def get_pc_manager_pids():
        pids = {}
        process_names = ["MSPCManager.exe", "MSPCManagerService.exe", "Microsoft.WIC.PCWndManager.Plugin.exe", "MSPCWndManager.exe"]
        for line in os.popen('tasklist.exe').read().splitlines():
            for process_name in process_names:
                if process_name in line:
                    split = line.split()
                    if 'Console' in split:
                        pids[process_name] = split[1]  # PID 通常是第二个元素
        return pids

    @staticmethod
    def get_processor_architecture():
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
        value, _ = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")
        winreg.CloseKey(key)
        return value

    def debug_dev_mode(self):
        return self.translator.translate("feature_unavailable")