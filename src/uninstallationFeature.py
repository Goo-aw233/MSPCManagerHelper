import glob
import itertools
import os
import re
import subprocess
import sys
import winreg
import tkinter as tk
from tkinter import messagebox

class UninstallationFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox

    def textbox(self, message):
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
                    return os.path.join(sys._MEIPASS, "tools", "NSudo", "NSudoLC_x64.exe")
                else:
                    return os.path.join("tools", "NSudo", "NSudoLC_x64.exe")
            elif processor_architecture == "ARM64":
                if hasattr(sys, '_MEIPASS'):
                    return os.path.join(sys._MEIPASS, "tools", "NSudo", "NSudoLC_ARM64.exe")
                else:
                    return os.path.join("tools", "NSudo", "NSudoLC_ARM64.exe")
            else:
                self.textbox(self.translator.translate("no_match_nsudo_version"))
                return None
        except Exception as e:
            self.textbox(self.translator.translate("error_getting_nsudo_path") + f": {str(e)}")
            return None

    def refresh_result_textbox(self):
        pass

    def uninstall_for_all_users_in_dism(self):
        try:
            # 获取预配包结果
            provisioned_packages_result = subprocess.run(
                ["Dism.exe", "/Online", "/Get-ProvisionedAppxPackages"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 需要以管理员身份运行
            if provisioned_packages_result.returncode == 740:
                return f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code_740')}\n\n{provisioned_packages_result.stdout.strip()}"

            # 通过 findstr.exe 过滤出带有 Microsoft.MicrosoftPCManager 和 Microsoft.PCManager 的结果
            provisioned_pc_manager_packages = subprocess.run(
                ["findstr.exe", "Microsoft.MicrosoftPCManager"],
                input=provisioned_packages_result.stdout, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout

            provisioned_pc_manager_packages_result = subprocess.run(
                ["findstr.exe", "Microsoft.PCManager"],
                input=provisioned_packages_result.stdout, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout

            # 合并结果并提取 PackageFullName
            pc_manager_packages_to_remove = []
            if provisioned_pc_manager_packages:
                pc_manager_packages_to_remove.append(str(provisioned_pc_manager_packages).split('PackageName : ')[1].split('\n')[0])
            if provisioned_pc_manager_packages_result:
                pc_manager_packages_to_remove.append(str(provisioned_pc_manager_packages_result).split('PackageName : ')[1].split('\n')[0])

            # 如果有符合的结果，移除预配包
            if pc_manager_packages_to_remove:
                for provisioned_package_name in pc_manager_packages_to_remove:
                    remove_package_result = subprocess.run(
                        ["Dism.exe", "/Online", "/Remove-ProvisionedAppxPackage", f"/PackageName:{provisioned_package_name}"],
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                    )

                    if remove_package_result.returncode != 0:
                        return f"{self.translator.translate('uninstall_for_all_users_in_dism_error')}: {remove_package_result.stderr.strip()}\n{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {remove_package_result.returncode}\n{remove_package_result.stdout.strip()}"

            # 为所有用户卸载新版
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.Name -like 'Microsoft.MicrosoftPCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为所有用户卸载旧版
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.Name -like 'Microsoft.PCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为当前用户卸载新版
            result3 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.MicrosoftPCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为当前用户卸载旧版
            result4 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.PCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            if all(result.returncode == 0 for result in [result1, result2, result3, result4]):
                if messagebox.askyesno(self.translator.translate("cleanup_config_and_files_notice_for_all_users_in_dism"),
                                       self.translator.translate("cleanup_config_and_files_for_all_users_in_dism")):

                    nsudolc_path = self.get_nsudolc_path()
                    if not nsudolc_path:
                        return "\n.join(messages)"

                    # 删除文件夹
                    folders_to_delete = [
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'PC Manager Store'),
                        os.path.join(os.environ['LocalAppData'], 'Windows Master Store'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Store'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master Store'),
                        os.path.join(os.environ['Temp'], 'WM Scan Test')
                    ]
                    is_first = True
                    for folder in folders_to_delete:
                        if os.path.exists(folder):
                            try:
                                subprocess.run(
                                    [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", folder],
                                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if is_first:
                                    self.textbox('\n' + self.translator.translate('clearing_configuration_files_for_all_users_in_dism') + ':\n')  # 显示执行操作
                                    is_first = False
                                self.textbox('-' + folder + '\n')   # 显示执行操作
                            except Exception as e:
                                self.textbox(self.translator.translate('fail_to_clear_configuration_files_path_for_all_users_in_dism') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_configuration_files_info_for_all_users_in_dism') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除注册表项
                    registry_keys_to_delete = [
                        r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager Store'
                    ]
                    is_first = True
                    for key in registry_keys_to_delete:
                        try:
                            subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "reg.exe", "delete", key, "/f"],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_registries_for_all_users_in_dism') + ':\n')  # 显示执行操作
                                is_first = False
                            self.textbox('-' + key + '\n')  # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_registries_info_for_all_users_in_dism') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除文件
                    file_paths = [
                        os.path.join(os.environ['LocalAppData'], 'Microsoft', 'CLR_v4.0', 'UsageLogs'),
                        os.path.join(os.environ['SystemRoot'], 'Prefetch'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Microsoft', 'CLR_v4.0', 'UsageLogs')
                    ]

                    prefetch_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADEFMGR*.pf',
                            '*CREATEDUMP*.pf',
                            '*MICROSOFT.WIC.PCWNDMANAGER*.pf',
                            '*MSPCMANAGER*.pf',
                            '*MSPCWNDMANAGER*.pf',
                            '*PCMAUTORUN*.pf',
                            '*PCMCHECKSUM*.pf'
                        ]
                    )

                    clr_logs_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADefMgr*.log',
                            '*Microsoft.WIC.PCWndManager.Plugin*.log',
                            '*MSPCManager*.log',
                            '*MSPCWndManager*.log',
                            '*PCMAutoRun*.log',
                            '*PCMCheckSum*.log'
                        ]
                    )

                    is_first = True
                    for files in itertools.chain(prefetch_files, clr_logs_files):
                        try:
                            subprocess.run(
                                [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "del", "/F", "/Q", files],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_other_files_for_all_users_in_dism') + ':\n')
                                is_first = False
                            self.textbox('-' + files + '\n')    # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_other_files_for_all_users_in_dism') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_other_files_info_for_all_users_in_dism') + ': ' + str(e) + '\n')

                    # 进阶清理
                    response_for_advanced_cleanup = messagebox.askyesno(
                        self.translator.translate("advanced_cleanup_config_and_files_notice_for_all_users_in_dism"),
                        self.translator.translate("advanced_cleanup_config_and_files_for_all_users_in_dism")
                    )

                    if response_for_advanced_cleanup:
                        try:
                            # 结束进程
                            processes = ["MSPCManager.exe", "MSPCManagerService.exe",
                                         "MSPCManagerCore.exe", "Microsoft.WIC.PCWndManager.Plugin.exe",
                                         "MSPCWndManager.exe", "MSPCManagerWidget.exe"]
                            is_first = True
                            any_process_killed = False
                            for process in processes:
                                try:
                                    result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "taskkill.exe", "/F", "/IM", process],
                                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                    if result.returncode == 0:  # 128 为找不到正在运行的进程
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_cleanup_taskkill_process_for_all_users_in_dism') + ':\n')
                                            is_first = False
                                        self.textbox('-' + process + '\n')  # 显示执行操作
                                        any_process_killed = True
                                except Exception as e:
                                    continue

                            if not any_process_killed:
                                self.textbox(self.translator.translate('advanced_cleanup_no_processes_killed_for_all_users_in_dism'))

                            # 删除文件夹
                            folders_to_delete = [
                                # os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.Windows.Search_cw5n1h2txyewy', 'LocalState', 'AppIconCache', '*', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                                # os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.Windows.Search_cw5n1h2txyewy', 'LocalState', 'AppIconCache', '*', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'MSPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Packages', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Packages', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'WindowsApps', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'WindowsApps', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramFiles'], 'WindowsApps', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramFiles'], 'WindowsApps', 'Microsoft.PCManager_*_8wekyb3d8bbwe')
                            ]
                            # 删除文件
                            files_to_delete = [
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe.xml'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Microsoft.PCManager_*_8wekyb3d8bbwe.xml')
                            ]

                            is_first = True
                            for folder in folders_to_delete:
                                for path in glob.glob(folder):
                                    try:
                                        subprocess.run(
                                            [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", path],
                                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_clearing_folders_for_all_users_in_dism') + ':\n')
                                            is_first = False
                                        self.textbox('-' + path + '\n') # 显示执行操作
                                    except Exception as e:
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_for_all_users_in_dism") + f": {path}")
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_info_for_all_users_in_dism") + f": {str(e)}")

                            is_first = True
                            for file in files_to_delete:
                                for path in glob.glob(file):
                                    try:
                                        subprocess.run(
                                            [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "del", "/F", "/Q", path],
                                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_clearing_config_and_files_for_all_users_in_dism') + ':\n')
                                            is_first = False
                                        self.textbox('-' + path + '\n') # 显示执行操作
                                    except Exception as e:
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_for_all_users_in_dism") + f": {path}")
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_info_for_all_users_in_dism") + f": {str(e)}")

                        except Exception as e:
                            self.textbox(self.translator.translate("advanced_cleanup_error") + f": {str(e)}")

                    return '\n' + self.translator.translate("uninstall_and_cleanup_for_all_users_in_dism_success")
                else:
                    return self.translator.translate('uninstall_for_all_users_in_dism_success')

            # 需要以管理员身份运行或包异常
            elif any(result.returncode == 1 for result in [result1, result2, result3, result4]):
                return (
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code_1')}\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result3.returncode}\n"
                    f"{result3.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result4.returncode}\n"
                    f"{result4.stderr.strip()}"
                )
            else:
                return (
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error')}\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result3.returncode}\n"
                    f"{result3.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_in_dism_error_code')}: {result4.returncode}\n"
                    f"{result4.stderr.strip()}"
                )

        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{self.translator.translate('dism_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_all_users_in_dism_error')}: {str(e)}"

    def uninstall_for_all_users(self):
        try:
            # 为所有用户卸载新版
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.Name -like 'Microsoft.MicrosoftPCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为所有用户卸载旧版
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.Name -like 'Microsoft.PCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为当前用户卸载新版
            result3 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.MicrosoftPCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为当前用户卸载旧版
            result4 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.PCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            if all(result.returncode == 0 for result in [result1, result2, result3, result4]):
                if messagebox.askyesno(self.translator.translate("cleanup_config_and_files_notice_for_all_users"),
                                       self.translator.translate("cleanup_config_and_files_for_all_users")):

                    nsudolc_path = self.get_nsudolc_path()
                    if not nsudolc_path:
                        return "\n.join(messages)"

                    # 删除文件夹
                    folders_to_delete = [
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'PC Manager Store'),
                        os.path.join(os.environ['LocalAppData'], 'Windows Master Store'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Store'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master Store'),
                        os.path.join(os.environ['Temp'], 'WM Scan Test')
                    ]
                    is_first = True
                    for folder in folders_to_delete:
                        if os.path.exists(folder):
                            try:
                                subprocess.run(
                                    [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", folder],
                                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if is_first:
                                    self.textbox('\n' + self.translator.translate('clearing_configuration_files_for_all_users') + ':\n')  # 显示执行操作
                                    is_first = False
                                self.textbox('-' + folder + '\n')   # 显示执行操作
                            except Exception as e:
                                self.textbox(self.translator.translate('fail_to_clear_configuration_files_path_for_all_users') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_configuration_files_info_for_all_users') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除注册表项
                    registry_keys_to_delete = [
                        r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager Store'
                    ]
                    is_first = True
                    for key in registry_keys_to_delete:
                        try:
                            subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "reg.exe", "delete", key, "/f"],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_registries_for_all_users') + ':\n')  # 显示执行操作
                                is_first = False
                            self.textbox('-' + key + '\n')  # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_registries_info_for_all_users') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除文件
                    file_paths = [
                        os.path.join(os.environ['LocalAppData'], 'Microsoft', 'CLR_v4.0', 'UsageLogs'),
                        os.path.join(os.environ['SystemRoot'], 'Prefetch'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Microsoft', 'CLR_v4.0', 'UsageLogs')
                    ]

                    prefetch_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADEFMGR*.pf',
                            '*CREATEDUMP*.pf',
                            '*MICROSOFT.WIC.PCWNDMANAGER*.pf',
                            '*MSPCMANAGER*.pf',
                            '*MSPCWNDMANAGER*.pf',
                            '*PCMAUTORUN*.pf',
                            '*PCMCHECKSUM*.pf'
                        ]
                    )

                    clr_logs_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADefMgr*.log',
                            '*Microsoft.WIC.PCWndManager.Plugin*.log',
                            '*MSPCManager*.log',
                            '*MSPCWndManager*.log',
                            '*PCMAutoRun*.log',
                            '*PCMCheckSum*.log'
                        ]
                    )

                    is_first = True
                    for files in itertools.chain(prefetch_files, clr_logs_files):
                        try:
                            subprocess.run(
                                [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "del", "/F", "/Q", files],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_other_files_for_all_users') + ':\n')
                                is_first = False
                            self.textbox('-' + files + '\n')    # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_other_files_for_all_users') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_other_files_info_for_all_users') + ': ' + str(e) + '\n')

                    # 进阶清理
                    response_for_advanced_cleanup = messagebox.askyesno(
                        self.translator.translate("advanced_cleanup_config_and_files_notice_for_all_users"),
                        self.translator.translate("advanced_cleanup_config_and_files_for_all_users")
                    )

                    if response_for_advanced_cleanup:
                        try:
                            # 结束进程
                            processes = ["MSPCManager.exe", "MSPCManagerService.exe",
                                         "MSPCManagerCore.exe", "Microsoft.WIC.PCWndManager.Plugin.exe",
                                         "MSPCWndManager.exe", "MSPCManagerWidget.exe"]
                            is_first = True
                            any_process_killed = False
                            for process in processes:
                                try:
                                    result = subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "taskkill.exe", "/F", "/IM", process],
                                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                    if result.returncode == 0:  # 128 为找不到正在运行的进程
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_cleanup_taskkill_process_for_all_users') + ':\n')
                                            is_first = False
                                        self.textbox('-' + process + '\n')  # 显示执行操作
                                        any_process_killed = True
                                except Exception as e:
                                    continue

                            if not any_process_killed:
                                self.textbox(self.translator.translate('advanced_cleanup_no_processes_killed_for_all_users'))

                            # 删除文件夹
                            folders_to_delete = [
                                # os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.Windows.Search_cw5n1h2txyewy', 'LocalState', 'AppIconCache', '*', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                                # os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.Windows.Search_cw5n1h2txyewy', 'LocalState', 'AppIconCache', '*', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'MSPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe', 'LocalCache', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Packages', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Packages', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'WindowsApps', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'WindowsApps', 'Microsoft.PCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramData'], 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramFiles'], 'WindowsApps', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe'),
                                os.path.join(os.environ['ProgramFiles'], 'WindowsApps', 'Microsoft.PCManager_*_8wekyb3d8bbwe')
                            ]
                            # 删除文件
                            files_to_delete = [
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Microsoft.MicrosoftPCManager_*_8wekyb3d8bbwe.xml'),
                                os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'AppRepository', 'Microsoft.PCManager_*_8wekyb3d8bbwe.xml')
                            ]

                            is_first = True
                            for folder in folders_to_delete:
                                for path in glob.glob(folder):
                                    try:
                                        subprocess.run(
                                            [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", path],
                                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_clearing_folders_for_all_users') + ':\n')
                                            is_first = False
                                        self.textbox('-' + path + '\n') # 显示执行操作
                                    except Exception as e:
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_for_all_users") + f": {path}")
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_info_for_all_users") + f": {str(e)}")

                            is_first = True
                            for file in files_to_delete:
                                for path in glob.glob(file):
                                    try:
                                        subprocess.run(
                                            [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "del", "/F", "/Q", path],
                                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                        if is_first:
                                            self.textbox('\n' + self.translator.translate('advanced_clearing_config_and_files_for_all_users') + ':\n')
                                            is_first = False
                                        self.textbox('-' + path + '\n') # 显示执行操作
                                    except Exception as e:
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_for_all_users") + f": {path}")
                                        self.textbox(self.translator.translate("advanced_fail_to_config_and_files_info_for_all_users") + f": {str(e)}")

                        except Exception as e:
                            self.textbox(self.translator.translate("advanced_cleanup_error") + f": {str(e)}")

                    return '\n' + self.translator.translate("uninstall_and_cleanup_for_all_users_success")
                else:
                    return self.translator.translate('uninstall_for_all_users_success')

            # 需要以管理员身份运行或包异常
            elif any(result.returncode == 1 for result in [result1, result2, result3, result4]):
                return (
                    f"{self.translator.translate('uninstall_for_all_users_error_code_1')}\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result3.returncode}\n"
                    f"{result3.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result4.returncode}\n"
                    f"{result4.stderr.strip()}"
                )
            else:
                return (
                    f"{self.translator.translate('uninstall_for_all_users_error')}\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result3.returncode}\n"
                    f"{result3.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result4.returncode}\n"
                    f"{result4.stderr.strip()}"
                )

        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_all_users_error')}: {str(e)}"

    def uninstall_for_current_user(self):
        try:
            # 为当前用户卸载新版
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.MicrosoftPCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为当前用户卸载旧版
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.PCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            if all(result.returncode == 0 for result in [result1, result2]):
                if messagebox.askyesno(self.translator.translate("cleanup_config_and_files_notice_for_current_user"),
                                       self.translator.translate("cleanup_config_and_files_for_current_user")):

                    nsudolc_path = self.get_nsudolc_path()
                    if not nsudolc_path:
                        return "\n.join(messages)"

                    # 删除文件夹
                    folders_to_delete = [
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['LocalAppData'], 'PC Manager Store'),
                        os.path.join(os.environ['LocalAppData'], 'Windows Master Store'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Store'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.PCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master Store'),
                        os.path.join(os.environ['Temp'], 'WM Scan Test')
                    ]
                    is_first = True
                    for folder in folders_to_delete:
                        if os.path.exists(folder):
                            try:
                                subprocess.run(
                                    [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "rmdir", "/S", "/Q", folder],
                                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if is_first:
                                    self.textbox('\n' + self.translator.translate('clearing_configuration_files_for_current_user') + ':\n')  # 显示执行操作
                                    is_first = False
                                self.textbox('-' + folder + '\n')   # 显示执行操作
                            except Exception as e:
                                self.textbox(self.translator.translate('fail_to_clear_configuration_files_path_for_current_user') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_configuration_files_info_for_current_user') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除注册表项
                    registry_keys_to_delete = [
                        r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager Store'
                    ]
                    is_first = True
                    for key in registry_keys_to_delete:
                        try:
                            subprocess.run([nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "reg.exe", "delete", key, "/f"],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_registries_for_current_user') + ':\n')  # 显示执行操作
                                is_first = False
                            self.textbox('-' + key + '\n')  # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_registries_info_for_current_user') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除文件
                    file_paths = [
                        os.path.join(os.environ['LocalAppData'], 'Microsoft', 'CLR_v4.0', 'UsageLogs'),
                        os.path.join(os.environ['SystemRoot'], 'Prefetch'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Microsoft', 'CLR_v4.0', 'UsageLogs')
                    ]

                    prefetch_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADEFMGR*.pf',
                            '*CREATEDUMP*.pf',
                            '*MICROSOFT.WIC.PCWNDMANAGER*.pf',
                            '*MSPCMANAGER*.pf',
                            '*MSPCWNDMANAGER*.pf',
                            '*PCMAUTORUN*.pf',
                            '*PCMCHECKSUM*.pf'
                        ]
                    )

                    clr_logs_files = itertools.chain.from_iterable(
                        glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                            '*BGADefMgr*.log',
                            '*Microsoft.WIC.PCWndManager.Plugin*.log',
                            '*MSPCManager*.log',
                            '*MSPCWndManager*.log',
                            '*PCMAutoRun*.log',
                            '*PCMCheckSum*.log'
                        ]
                    )

                    is_first = True
                    for files in itertools.chain(prefetch_files, clr_logs_files):
                        try:
                            subprocess.run(
                                [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "cmd.exe", "/C", "del", "/F", "/Q", files],
                                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_other_files_for_current_user') + ':\n')
                                is_first = False
                            self.textbox('-' + files + '\n')    # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_other_files_for_current_user') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_other_files_info_for_current_user') + ': ' + str(e) + '\n')

                    return '\n' + self.translator.translate("uninstall_and_cleanup_for_current_user_success")
                else:
                    return self.translator.translate('uninstall_for_current_user_success')

            # 需要以管理员身份运行或包异常
            elif any(result.returncode == 1 for result in [result1, result2]):
                return (
                    f"{self.translator.translate('uninstall_for_current_user_error_code_1')}\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_all_users_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}"
                )
            else:
                return (
                    f"{self.translator.translate('uninstall_for_current_user_error')}\n\n"
                    f"{self.translator.translate('uninstall_for_current_user_error_code')}: {result1.returncode}\n"
                    f"{result1.stderr.strip()}\n\n\n"
                    f"{self.translator.translate('uninstall_for_current_user_error_code')}: {result2.returncode}\n"
                    f"{result2.stderr.strip()}"
                )

        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_current_user_error')}: {str(e)}"

    def uninstall_pc_manager_beta(self):
        try:
            pc_manager_beta_path = os.path.join(os.environ['ProgramFiles'], 'Microsoft PC Manager')
            if not os.path.exists(pc_manager_beta_path):
                return self.translator.translate("pc_manager_beta_not_found")

            # 检测 Uninst.exe 是否存在
            pc_manager_beta_uninst_exe = os.path.join(pc_manager_beta_path, 'Uninst.exe')
            if not os.path.exists(pc_manager_beta_uninst_exe):
                return self.translator.translate("pc_manager_beta_not_found")

            # 运行卸载程序
            result = subprocess.run([pc_manager_beta_uninst_exe], capture_output=True, text=True)
            if result.returncode != 0:
                return f"{self.translator.translate('uninstall_pcm_beta_error_info')}: {result.stderr.strip()}"

            # 弹出窗口询问是否清理配置和文件
            tf = True
            while tf:
                if re.search(r'Uninst\w+\.exe', os.popen('tasklist.exe').read()):
                    pass
                else:
                    tf = False
            pc_manager_beta_uninst_exe = os.path.join(pc_manager_beta_path, 'Uninst.exe')
            if not os.path.exists(pc_manager_beta_uninst_exe):
                if not messagebox.askyesno(self.translator.translate("cleanup_pc_manager_beta_config_and_files_notice"),
                                            self.translator.translate("cleanup_pc_manager_beta_config_and_files")):
                    return self.translator.translate("pc_manager_beta_uninstalled")

                # 停止并删除服务

                # 删除文件夹
                folders_to_delete = [
                    os.path.join(os.environ['LocalAppData'], 'PC Manager'),
                    os.path.join(os.environ['LocalAppData'], 'Windows Master'),
                    os.path.join(os.environ['ProgramData'], 'PCMConfigPath'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                    os.path.join(os.environ['ProgramFiles'], 'Microsoft PC Manager'),
                    os.path.join(os.environ['ProgramFiles'], 'WindowsMaster'),
                    os.path.join(os.environ['ProgramFiles'], 'Windows Master'),
                    os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master'),
                    os.path.join(os.environ['SystemRoot'], 'SystemTemp', 'Windows Master'),
                    os.path.join(os.environ['Temp'], 'Windows Master'),
                    os.path.join(os.environ['Temp'], 'WM Scan Test')
                ]
                is_first = True
                for folder in folders_to_delete:
                    if os.path.exists(folder):
                        try:
                            subprocess.run(['rmdir', '/S', '/Q', folder], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_configuration_files') + ':\n')   # 显示执行操作
                                is_first = False
                            self.textbox('-' + folder + '\n')   # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_path') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_info') + ': ' + str(e) + '\n')   # 显示错误内容

                # 删除注册表项
                registry_keys_to_delete = [
                    r'HKEY_CURRENT_USER\Software\WindowsMaster',
                    r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run\WindowsMasterUI',
                    r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsMasterUI',
                    r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager',
                    r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\微软电脑管家',
                    r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager'
                ]
                is_first = True
                for key in registry_keys_to_delete:
                    try:
                        subprocess.run(['reg.exe', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)
                        if is_first:
                            self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_registries') + ':\n')  # 显示执行操作
                            is_first = False
                        self.textbox('-' + key + '\n')   # 显示执行操作
                    except Exception as e:
                        self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_registries_info') + ': ' + str(e) + '\n')  # 显示错误内容

                # 删除文件
                file_paths = [
                    os.path.join(os.environ['AppData'], 'Microsoft', 'Internet Explorer', 'Quick Launch', 'User Pinned', 'TaskBar'),
                    os.path.join(os.environ['AppData'], 'Microsoft', 'Windows', 'Start Menu'),
                    os.path.join(os.environ['LocalAppData'], 'Microsoft', 'CLR_v4.0', 'UsageLogs'),
                    os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
                    os.path.join(os.environ['Public'], 'Desktop'),
                    os.path.join(os.environ['SystemRoot'], 'Prefetch'),
                    os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Microsoft', 'CLR_v4.0', 'UsageLogs'),
                    os.path.join(os.environ['UserProfile'], 'Desktop')
                ]

                prefetch_files = itertools.chain.from_iterable(
                    glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                        '*BGADEFMGR*.pf',
                        '*MSPCMANAGER*.pf',
                        '*MSPCWNDMANAGER*.pf',
                        '*PCMAUTORUN*.pf',
                        '*PCMCHECKSUM*.pf',
                        '*UNINST*.pf',
                        '*WINDOWSMASTER*.pf'
                    ]
                )

                shortcuts = itertools.chain.from_iterable(
                    glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                        '*PC Manager*.lnk',
                        '*MSPCManager*.lnk',
                        '*Microsoft PC Manager*.lnk',
                        '*Microsoft 電腦管家*.lnk',
                        '*Windows Master*.lnk',
                        '*微软电脑管家*.lnk'
                    ]
                )

                clr_logs_files = itertools.chain.from_iterable(
                    glob.iglob(os.path.join(paths, pattern)) for paths in file_paths for pattern in [
                        '*BGADefMgr*.log',
                        '*Microsoft.WIC.PCWndManager.Plugin*.log',
                        '*MSPCManager*.log',
                        '*MSPCWndManager*.log',
                        '*PCMAutoRun*.log',
                        '*PCMCheckSum*.log'
                    ]
                )

                is_first = True
                for files in itertools.chain(clr_logs_files, prefetch_files, shortcuts):
                    try:
                        os.remove(files)
                        if is_first:
                            self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_other_files') + ':\n')
                            is_first = False
                        self.textbox('-' + files + '\n')    # 显示执行操作
                    except Exception as e:
                        self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_other_files') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_pc_manager_beta_other_files_info') + ': ' + str(e) + '\n')

                return '\n' + self.translator.translate("uninstalled_cleanup_pc_manager_beta_config_and_files")
            else:
                return self.translator.translate('user_canceled')
        except Exception as e:
            return f"{self.translator.translate('uninstall_pc_manager_beta_error_info')}: {str(e)}"
