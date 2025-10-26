import os
import shutil
import subprocess
import sys
import tkinter as tk
import winreg
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

from other_feature import OtherFeature
from uninstallation_feature import UninstallationFeature


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
        self.result_textbox.config(state="disabled")
        self.result_textbox.update_idletasks()  # 刷新界面

    def get_nsudolc_path(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                processor_architecture = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]

            if processor_architecture == "AMD64":
                if hasattr(sys, '_MEIPASS'):
                    return str(Path(sys._MEIPASS) / "tools" / "NSudo" / "NSudoLC_x64.exe")
                else:
                    return str(Path("tools") / "NSudo" / "NSudoLC_x64.exe")
            elif processor_architecture == "ARM64":
                if hasattr(sys, '_MEIPASS'):
                    return str(Path(sys._MEIPASS) / "tools" / "NSudo" / "NSudoLC_ARM64.exe")
                else:
                    return str(Path("tools") / "NSudo" / "NSudoLC_ARM64.exe")
            else:
                self.textbox(self.translator.translate("no_match_nsudo_version"))
                return None
        except Exception as e:
            self.textbox(self.translator.translate("error_getting_nsudo_path") + f": {str(e)}")
            return None

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
        try:
            # 设置 NSudoLC 路径变量
            nsudolc_path = self.get_nsudolc_path()
            if not nsudolc_path:
                return "\n.join(messages)"

            # 设置路径变量
            date_str = datetime.now().strftime(datetime.now().isoformat().replace(":", "."))    # 日期字符串
            desktop_path = Path(os.getenv("UserProfile")) / "Desktop"
            logs_destination = desktop_path / "Microsoft PC Manager Logs" / date_str   # 日志目标路径
            program_logs_source_path = Path(os.getenv("ProgramData")) / "Windows Master Store"   # 程序日志源路径
            appdata_clr_4_0_logs_source = Path(os.getenv("LocalAppData")) / "Microsoft" / "CLR_v4.0" / "UsageLogs"  # LocalAppData 下 CLR_v4.0 日志源路径
            systemroot_clr_4_0_logs_source = Path(os.getenv("SystemRoot")) / "System32" / "config" / "systemprofile" / "AppData" / "Local" / "Microsoft" / "CLR_v4.0" / "UsageLogs"  # SystemRoot 下 CLR_v4.0 日志源路径
            common_logs_source = program_logs_source_path / "Common"  # Common 日志源路径
            crash_files_source = common_logs_source / "Crash"  # Crash 源路径
            setup_logs_source = program_logs_source_path / "Setup"  # Setup 日志源路径
            service_logs_source = program_logs_source_path / "ServiceData" # ServiceData 日志源路径
            exe_setup_logs_source = Path(os.getenv("ProgramData")) / "Windows Master Setup"  # EXE 安装器日志源路径
            logs_zip_archive = desktop_path    # 日志压缩包路径

            # 创建目标目录
            os.makedirs(logs_destination, exist_ok=True)    # 创建日志目标目录
            os.makedirs(logs_destination / "Common", exist_ok=True)    # 创建 Common 目标目录

            # 复制 AppData 下的 CLR_v4.0 日志
            if appdata_clr_4_0_logs_source.exists():
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    appdata_clr_4_0_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "Robocopy.exe",
                                                             str(appdata_clr_4_0_logs_source), str(logs_destination / "AppData_CLR_v4.0"),
                                                             "*Microsoft.WIC.PCWndManager.Plugin*.log",
                                                             "*MSPCManager*.log", "*MSPCWndManager*.log",
                                                             "*PCMAutoRun*.log", "*PCMCheckSum*.log"],
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if appdata_clr_4_0_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_appdata_clr_4_0_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_appdata_clr_4_0_logs_error") + f":\n{appdata_clr_4_0_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_appdata_clr_4_0_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 SystemRoot 下的 CLR_v4.0 日志
            if systemroot_clr_4_0_logs_source.exists():
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    systemroot_clr_4_0_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "Robocopy.exe",
                                                                str(systemroot_clr_4_0_logs_source), str(logs_destination / "SystemRoot_CLR_v4.0"),
                                                                "*Microsoft.WIC.PCWndManager.Plugin*.log",
                                                                "*MSPCManager*.log", "*MSPCWndManager*.log",
                                                                "*PCMAutoRun*.log", "*PCMCheckSum*.log"],
                         capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if systemroot_clr_4_0_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_systemroot_clr_4_0_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_systemroot_clr_4_0_logs_error") + f":\n{systemroot_clr_4_0_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_systemroot_clr_4_0_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 Common 下的 .log 文件（使用日志）
            if common_logs_source.exists():
                try:    # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    common_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(common_logs_source / "*.log"), str(logs_destination / "Common"),
                         "/H", "/I", "/S", "/Y"],  # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if common_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_common_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_common_logs_error") + f":\n{common_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_common_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 Crash 文件夹（崩溃文件）
            if crash_files_source.exists() and any(crash_files_source.iterdir()):
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    common_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(crash_files_source / "*.*"), str(logs_destination / "Common" / "Crash"),
                         "/H", "/I", "/S", "/Y"], # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                         capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if common_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_crash_files_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_crash_files_error") + f":\n{common_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_crash_files_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 Setup 文件夹（安装日志）
            if setup_logs_source.exists():
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    setup_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(setup_logs_source), str(logs_destination / "Setup"), "/H", "/I", "/S", "/Y"],
                        # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if setup_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_setup_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_setup_logs_error") + f":\n{setup_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_setup_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 ServiceData 文件夹（服务日志）
            if service_logs_source.exists():
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    service_data_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(service_logs_source), str(logs_destination / "ServiceData"), "/H", "/I", "/S", "/Y"],
                        # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if service_data_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_service_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_service_logs_error") + f":\n{service_data_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_service_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制 EXE 安装器日志
            if exe_setup_logs_source.exists():
                try:  # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                    exe_setup_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(exe_setup_logs_source), str(logs_destination / "Windows Master Setup"), "/H", "/I", "/S", "/Y"],
                        # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if exe_setup_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_error") + f":\n{exe_setup_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_exe_setup_logs_error") + f":\n{str(e)}")
            else:
                pass

            # 复制未列出的日志
            try:
                subdirs = [p for p in program_logs_source_path.iterdir() if p.is_dir()]
                filtered = ["Common", "Setup", "ServiceData"]
                other_logs_destinations = []
                for subdir in subdirs:
                    try:
                        if subdir.name not in filtered and any(p.suffix == '.log' for p in subdir.iterdir()):
                            other_logs_destinations.append((str(subdir), subdir.name))
                    except:
                        pass

                for destination, file_name in other_logs_destinations:
                    try:  # 使用 cmd.exe 拉起进程时需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                        nsudolc_copy_other_logs_cmd = [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe", destination,
                                                       str(logs_destination / "OtherLogs" / file_name), "/H", "/I", "/S", "/Y"]
                        # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；包括子目录（不复制空目录）；覆盖
                        other_logs_result = subprocess.run(nsudolc_copy_other_logs_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        if other_logs_result.returncode == 0:
                            self.textbox(self.translator.translate("retrieve_pc_manager_other_logs_success"))
                        else:
                            self.textbox(self.translator.translate("retrieve_pc_manager_other_logs_error") + f": {other_logs_result.stdout}")
                    except Exception as e:
                        self.textbox(self.translator.translate("retrieve_pc_manager_other_logs_error") + f": {str(e)}")
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_other_logs_error") + f": {str(e)}")

            # 复制 Application.evtx
            application_evtx_path = Path(os.getenv("SystemRoot")) / "System32" / "winevt" / "Logs" / "Application.evtx"
            if application_evtx_path.exists():
                try:
                    application_evtx_result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "xcopy.exe",
                         str(application_evtx_path), str(logs_destination), "/H", "/I", "/Y"],
                        # 包含隐藏和系统文件；如果目标不存在，并且使用时未指定文件，则假定目标为目录；覆盖
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    if application_evtx_result.returncode == 0:
                        self.textbox(self.translator.translate("retrieve_pc_manager_evtx_success"))
                    else:
                        self.textbox(self.translator.translate("retrieve_pc_manager_evtx_error") + f":\n{application_evtx_result.stdout}")
                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_evtx_error") + f":\n{str(e)}")
            else:
                pass

            # 获取计算机信息并保存到 ComputerInfo.txt
            try:
                self.textbox("\n" + self.translator.translate("retrieving_computer_info"))
                computer_info_path = logs_destination / "ComputerInfo.txt"
                subprocess.run(["powershell.exe", "-Command", f"Get-ComputerInfo | Out-File -FilePath '{computer_info_path}' -Encoding utf8"],
                               capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self.textbox(self.translator.translate("retrieve_computer_info_success"))
            except FileNotFoundError as e:
                self.textbox(f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}")
            except Exception as e:
                self.textbox(self.translator.translate("retrieve_computer_info_error") + f":\n{str(e)}")

            # 输出 MSPCManagerHelper 版本到 MSPCManagerHelperInfo.txt

            # 传入用户输入的内容到 UserInputInfo.txt

            # 询问是否选择获取 Dumps
            response_for_retrieve_dumps = messagebox.askyesno(
                self.translator.translate("ask_to_retrieve_pc_manager_dumps_notice"),
                self.translator.translate("ask_to_retrieve_pc_manager_dumps")
            )

            if response_for_retrieve_dumps:
                dumps_destination = logs_destination / 'Dumps'
                os.makedirs(dumps_destination, exist_ok=True)  # 创建 Dumps 目标目录

                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                        processor_architecture = winreg.QueryValueEx(key, "PROCESSOR_ARCHITECTURE")[0]

                    # 根据处理器架构设定 ProcDump 变量
                    if processor_architecture == "AMD64":
                        if hasattr(sys, '_MEIPASS'):
                            procdump_path = Path(sys._MEIPASS) / "tools" / "ProcDump" / "procdump64.exe"
                        else:
                            procdump_path = Path("tools") / "ProcDump" / "procdump64.exe"
                    elif processor_architecture == "ARM64":
                        if hasattr(sys, '_MEIPASS'):
                            procdump_path = Path(sys._MEIPASS) / "tools" / "ProcDump" / "procdump64a.exe"
                        else:
                            procdump_path = Path("tools") / "ProcDump" / "procdump64a.exe"
                    else:
                        self.textbox(self.translator.translate("no_match_procdump_version"))
                        return "\n.join(messages)"

                    # 输出许可协议
                    self.textbox("\n" + self.translator.translate("procdump_agreement"))

                    # 获取 Dump 文件
                    for process_name in ["MSPCManager.exe", "MSPCManagerService.exe", "MSPCManagerCore.exe", "MSPCManagerWidget.exe",
                                 "Microsoft.WIC.PCWndManager.Plugin.exe", "MSPCWndManager.exe"]:
                        self.textbox("\n" + f"{self.translator.translate('retrieving_progress_name')}: {process_name}")
                        dump_file = dumps_destination / f"{process_name}_{date_str}.dmp"
                        try:
                            procdump_cmd = [str(procdump_path), "-accepteula", "-ma", process_name, str(dump_file)]
                            procdump_result = subprocess.run(procdump_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if procdump_result.returncode == 1:
                                self.textbox(self.translator.translate("retrieve_pc_manager_dumps_success") + f": {dump_file}")
                            elif procdump_result.returncode == 4294967294:  # 进程未启动
                                self.textbox(self.translator.translate("retrieve_pc_manager_dumps_code_4294967294"))
                            else:
                                self.textbox({procdump_result.returncode})
                                self.textbox(self.translator.translate("retrieve_pc_manager_dumps_error") + f": {procdump_result.stdout}")
                        except subprocess.CalledProcessError as e:
                            self.textbox(self.translator.translate("retrieve_pc_manager_dumps_error") + f":\n{str(e)}")

                except Exception as e:
                    self.textbox(self.translator.translate("retrieve_pc_manager_logs_error") + f":\n{str(e)}")

            # 压缩日志
            try:
                self.textbox("\n" + self.translator.translate("compressing_pc_manager_logs"))
                zip_file_name = f"{self.translator.translate('pc_manager_logs_zip_archive')}_{date_str}"
                zip_file_path = logs_zip_archive / zip_file_name
                shutil.make_archive(str(zip_file_path), 'zip', str(logs_destination))
                self.textbox(self.translator.translate("path_to_pc_manager_logs_zip_archive") + f": {zip_file_path}.zip")
                messagebox.showwarning(self.translator.translate("warning"),
                                        self.translator.translate("do_not_share_log_files_with_untrusted_users"))
                self.textbox("\n" + self.translator.translate("do_not_share_log_files_with_untrusted_users"))

            except Exception as e:
                self.textbox(self.translator.translate("retrieve_pc_manager_logs_error") + f":\n{str(e)}")

            # 清理获取到的日志的文件夹
            try:
                response_for_clear_logs = messagebox.askyesno(
                    self.translator.translate("ask_to_clear_pc_manager_logs_notice"),
                    self.translator.translate("ask_to_clear_pc_manager_logs")
                )

                if response_for_clear_logs:
                    nsudolc_path = self.get_nsudolc_path()
                    if nsudolc_path:    # 使用 cmd.exe 拉起的进程需要 "-ShowWindowMode:Hide" 参数，不依赖 cmd.exe 时不需要 "cmd.exe", "/C" 参数
                        clear_logs_destination = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", "%UserProfile%\\Desktop\\Microsoft PC Manager Logs"],
                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        if clear_logs_destination.returncode == 0:
                            self.textbox("\n" + self.translator.translate("clearing_pc_manager_logs_success"))
                        else:
                            self.textbox(self.translator.translate("clearing_pc_manager_logs_error") + f":\n{clear_logs_destination.stdout}")
                else:
                    pass

            except Exception as e:
                self.textbox(self.translator.translate("clearing_pc_manager_logs_error") + f":\n{str(e)}")

            return "\n" + self.translator.translate("retrieve_pc_manager_logs_success")

        except Exception as e:
            self.textbox(self.translator.translate("retrieve_pc_manager_logs_error") + f":\n{str(e)}")

    def debug_dev_mode(self):
        try:
            # 打开文件选择框
            file_paths = filedialog.askopenfilenames(filetypes=[("*", "*")])

            if file_paths:
                results = []
                for file_path in file_paths:
                    # 使用 subprocess 运行选中的文件
                    result = subprocess.run([file_path], capture_output=True, text=True)
                    results.append(result.stdout)
                return self.translator.translate("feature_unavailable") + '\n' + '\n'.join(results)
            else:
                return self.translator.translate("no_files_selected")
        except Exception as e:
            return self.translator.translate("warning") + f": {str(e)}"
