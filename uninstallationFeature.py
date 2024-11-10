import glob
import itertools
import os
import re
import subprocess
import tkinter as tk
from tkinter import messagebox

class UninstallationFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox

    def textbox(self, message):
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disable")
        self.result_textbox.update_idletasks()  # 刷新界面

    def uninstall_for_all_users(self):
        try:
            # 为所有用户卸载新版
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.name -like 'Microsoft.MicrosoftPCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 为所有用户卸载旧版
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.name -like 'Microsoft.PCManager'} | "
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

            if result1.returncode == 0 and result2.returncode == 0 and result3.returncode == 0 and result4.returncode == 0:
                if messagebox.askyesno(self.translator.translate("cleanup_config_and_files_notice_for_all_users"),
                                       self.translator.translate("cleanup_config_and_files_for_all_users")):
                    # 删除文件夹
                    folders_to_delete = [
                        os.path.join(os.environ['LocalAppData'], 'PC Manager Store'),
                        os.path.join(os.environ['LocalAppData'], 'Windows Master Store'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Store'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master')
                    ]
                    is_first = True
                    for folder in folders_to_delete:
                        if os.path.exists(folder):
                            try:
                                subprocess.run(['rmdir', '/S', '/Q', folder], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if is_first:
                                    self.textbox('\n' + self.translator.translate('clearing_configuration_files_for_all_users') + ':\n')  # 显示执行操作
                                    is_first = False
                                self.textbox('-' + folder + '\n')
                            except Exception as e:
                                self.textbox(self.translator.translate('fail_to_clear_configuration_files_path_for_all_users') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_configuration_files_info_for_all_users') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除注册表项
                    registry_keys_to_delete = [
                        r'HKLM\SOFTWARE\WOW6432Node\MSPCManager Store'
                    ]
                    is_first = True
                    for key in registry_keys_to_delete:
                        try:
                            subprocess.run(['reg', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_registries_for_all_users') + ':\n')  # 显示执行操作
                                is_first = False
                            self.textbox('-' + key + '\n')  # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_registries_info_for_all_users') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除文件
                    file_paths = os.path.join(os.environ['SystemRoot'], 'Prefetch')
                    prefetch_files = itertools.chain(
                        glob.iglob(os.path.join(file_paths, '*BGADEFMGR*.pf')),
                        glob.iglob(os.path.join(file_paths, '*CREATEDUMP*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MICROSOFT.WIC.PCWNDMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MSPCMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MSPCWNDMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*PCMAUTORUN*.pf')),
                        glob.iglob(os.path.join(file_paths, '*PCMCHECKSUM*.pf'))
                    )
                    is_first = True
                    for files in prefetch_files:
                        try:
                            os.remove(files)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_other_files_for_all_users') + ':\n')
                                is_first = False
                            self.textbox('-' + files + '\n')
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_other_files_for_all_users') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_other_files_info_for_all_users') + ': ' + str(e) + '\n')

                    return '\n' + self.translator.translate("uninstall_and_cleanup_for_all_users_success")
                else:
                    return self.translator.translate('uninstall_for_all_users_success')
            elif result1.returncode == 1 or result2.returncode == 1 or result3.returncode == 1 or result4.returncode == 1:
                return self.translator.translate("uninstall_for_all_users_error_code_1")
            else:
                return f"{self.translator.translate('uninstall_for_all_users_error')}: {result1.stderr.strip()} {result2.stderr.strip()} {result3.stderr.strip()} {result4.stderr.strip()}\n{self.translator.translate('uninstall_for_all_users_error_code')}: {result1.returncode} {result2.returncode} {result3.returncode} {result4.returncode}"
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

            if result1.returncode == 0 and result2.returncode == 0:
                if messagebox.askyesno(self.translator.translate("cleanup_config_and_files_notice_for_current_user"),
                                       self.translator.translate("cleanup_config_and_files_for_current_user")):
                    # 删除文件夹
                    folders_to_delete = [
                        os.path.join(os.environ['LocalAppData'], 'PC Manager Store'),
                        os.path.join(os.environ['LocalAppData'], 'Windows Master Store'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                        os.path.join(os.environ['ProgramData'], 'Windows Master Store'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Packages', 'Microsoft.MicrosoftPCManager_8wekyb3d8bbwe'),
                        os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master')
                    ]
                    is_first = True
                    for folder in folders_to_delete:
                        if os.path.exists(folder):
                            try:
                                subprocess.run(['rmdir', '/S', '/Q', folder], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                                if is_first:
                                    self.textbox('\n' + self.translator.translate('clearing_configuration_files_for_current_user') + ':\n')  # 显示执行操作
                                    is_first = False
                                self.textbox('-' + folder + '\n')
                            except Exception as e:
                                self.textbox(self.translator.translate('fail_to_clear_configuration_files_path_for_current_user') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_configuration_files_info_for_current_user') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除注册表项
                    registry_keys_to_delete = [
                        r'HKLM\SOFTWARE\WOW6432Node\MSPCManager Store'
                    ]
                    is_first = True
                    for key in registry_keys_to_delete:
                        try:
                            subprocess.run(['reg', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_registries_for_current_user') + ':\n')  # 显示执行操作
                                is_first = False
                            self.textbox('-' + key + '\n')  # 显示执行操作
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_registries_info_for_current_user') + ': ' + str(e) + '\n')  # 显示错误内容

                    # 删除文件
                    file_paths = os.path.join(os.environ['SystemRoot'], 'Prefetch')
                    prefetch_files = itertools.chain(
                        glob.iglob(os.path.join(file_paths, '*BGADEFMGR*.pf')),
                        glob.iglob(os.path.join(file_paths, '*CREATEDUMP*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MICROSOFT.WIC.PCWNDMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MSPCMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*MSPCWNDMANAGER*.pf')),
                        glob.iglob(os.path.join(file_paths, '*PCMAUTORUN*.pf')),
                        glob.iglob(os.path.join(file_paths, '*PCMCHECKSUM*.pf'))
                    )
                    is_first = True
                    for files in prefetch_files:
                        try:
                            os.remove(files)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_other_files_for_current_user') + ':\n')
                                is_first = False
                            self.textbox('-' + files + '\n')
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_other_files_for_current_user') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_other_files_info_for_current_user') + ': ' + str(e) + '\n')

                    return '\n' + self.translator.translate("uninstall_and_cleanup_for_current_user_success")
                else:
                    return self.translator.translate('uninstall_for_current_user_success')
            elif result1.returncode == 1 or result2.returncode == 1:
                return self.translator.translate("uninstall_for_current_user_error_code_1")
            else:
                return f"{self.translator.translate('uninstall_for_current_user_error')}: {result1.stderr.strip()} {result2.stderr.strip()}\n{self.translator.translate('uninstall_for_current_user_error_code')}: {result1.returncode} {result2.returncode}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_current_user_error')}: {str(e)}"

    def uninstall_pc_manager_beta(self):
        try:
            pcm_path = os.path.join(os.environ['ProgramFiles'], 'Microsoft PC Manager')
            if not os.path.exists(pcm_path):
                return self.translator.translate("pc_manager_beta_not_found")

            # 检测 Uninst.exe 是否存在
            pc_manager_beta_uninst_exe = os.path.join(pcm_path, 'Uninst.exe')
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
            pc_manager_beta_uninst_exe = os.path.join(pcm_path, 'Uninst.exe')
            if not os.path.exists(pc_manager_beta_uninst_exe):
                if not messagebox.askyesno(self.translator.translate("cleanup_pc_manager_beta_config_and_files_notice"),
                                            self.translator.translate("cleanup_pc_manager_beta_config_and_files")):
                    return self.translator.translate("pc_manager_beta_uninstalled")

                # 删除文件夹
                folders_to_delete = [
                    os.path.join(os.environ['LocalAppData'], 'PC Manager'),
                    os.path.join(os.environ['LocalAppData'], 'Windows Master'),
                    os.path.join(os.environ['ProgramData'], 'PCMConfigPath'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                    os.path.join(os.environ['SystemRoot'], 'System32', 'config', 'systemprofile', 'AppData', 'Local', 'Windows Master')
                ]
                is_first = True
                for folder in folders_to_delete:
                    if os.path.exists(folder):
                        try:
                            subprocess.run(['rmdir', '/S', '/Q', folder], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_configuration_files') + ':\n')   # 显示执行操作
                                is_first = False
                            self.textbox('-' + folder + '\n')
                        except Exception as e:
                            self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_path') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_info') + ': ' + str(e) + '\n')   # 显示错误内容

                # 删除注册表项
                registry_keys_to_delete = [
                    r'HKCU\Software\WindowsMaster',
                    r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run\WindowsMasterUI',
                    r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsMasterUI',
                    r'HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager',
                    r'HKLM\SOFTWARE\WOW6432Node\MSPCManager'
                ]
                is_first = True
                for key in registry_keys_to_delete:
                    try:
                        subprocess.run(['reg', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)
                        if is_first:
                            self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_registries') + ':\n')  # 显示执行操作
                            is_first = False
                        self.textbox('-' + key + '\n')   # 显示执行操作
                    except Exception as e:
                        self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_registries_info') + ': ' + str(e) + '\n')  # 显示错误内容

                # 删除文件
                file_paths = os.path.join(os.environ['SystemRoot'], 'Prefetch')
                prefetch_files = itertools.chain(
                    glob.iglob(os.path.join(file_paths, '*BGADEFMGR*.pf')),
                    glob.iglob(os.path.join(file_paths, '*MSPCMANAGER*.pf')),
                    glob.iglob(os.path.join(file_paths, '*MSPCWNDMANAGER*.pf')),
                    glob.iglob(os.path.join(file_paths, '*PCMAUTORUN*.pf')),
                    glob.iglob(os.path.join(file_paths, '*PCMCHECKSUM*.pf')),
                    glob.iglob(os.path.join(file_paths, '*UNINST*.pf'))
                )
                is_first = True
                for files in prefetch_files:
                    try:
                        os.remove(files)
                        if is_first:
                            self.textbox('\n' + self.translator.translate('clearing_pc_manager_beta_other_files') + ':\n')
                            is_first = False
                        self.textbox('-' + files + '\n')
                    except Exception as e:
                        self.textbox(self.translator.translate('fail_to_clear_pc_manager_beta_other_files') + ': ' + str(files) + ', ' + self.translator.translate('fail_to_clear_pc_manager_beta_other_files_info') + ': ' + str(e) + '\n')

                return '\n' + self.translator.translate("uninstalled_cleanup_pc_manager_beta_config_and_files")
            else:
                return self.translator.translate('user_canceled')
        except Exception as e:
            return f"{self.translator.translate('uninstall_pc_manager_beta_error_info')}: {str(e)}"
