import os
import re
import subprocess
import tkinter as tk
import winreg
from tkinter import messagebox

class UninstallationFeature:
    def __init__(self, translator):
        self.translator = translator

    def uninstall_for_all_users(self):
        try:
            # 执行第一个 PowerShell 命令
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.name -like 'Microsoft.MicrosoftPCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 执行第二个 PowerShell 命令
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.name -like 'Microsoft.PCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 删除 EXE 升级后遗留注册表项
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager Store", 0,
                                    winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, "ProductVersion")
            except FileNotFoundError:
                pass

            if result1.returncode == 0 and result2.returncode == 0:
                return self.translator.translate("uninstall_for_all_users_success")
            elif result1.returncode == 1 or result2.returncode == 1:
                return self.translator.translate("uninstall_for_current_users_error_code_1")
            else:
                return f"{self.translator.translate('uninstall_for_all_users_error')}: {result1.stderr.strip()} {result2.stderr.strip()}\n{self.translator.translate('uninstall_for_all_users_error_code')}: {result1.returncode} {result2.returncode}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_all_users_error')}: {str(e)}"

    def uninstall_for_current_user(self):
        try:
            # 执行第一个 PowerShell 命令
            result1 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.MicrosoftPCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 执行第二个 PowerShell 命令
            result2 = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.PCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 删除 EXE 升级后遗留注册表项
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager Store", 0,
                                    winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, "ProductVersion")
            except FileNotFoundError:
                pass

            if result1.returncode == 0 and result2.returncode == 0:
                return self.translator.translate("uninstall_for_current_user_success")
            elif result1.returncode == 1 or result2.returncode == 1:
                return self.translator.translate("uninstall_for_current_users_error_code_1")
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
                    os.path.join(os.environ['LocalAppData'], 'Windows Master'),
                    os.path.join(os.environ['LocalAppData'], 'PC Manager'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master'),
                    os.path.join(os.environ['ProgramData'], 'Windows Master Setup'),
                    os.path.join(os.environ['ProgramData'], 'PCMConfigPath'),
                    os.path.join(os.environ['WinDir'], 'System32', 'config', 'systemprofile', 'AppData', 'Local',
                                'Windows Master')
                ]
                is_first = True
                for folder in folders_to_delete:
                    if os.path.exists(folder):
                        try:
                            subprocess.run(['rmdir', '/S', '/Q', folder], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                            if is_first:
                                self.result_textbox.config(state="normal")
                                self.result_textbox.insert(tk.END, '\n' + self.translator.translate('clearing_pc_manager_beta_configuration_files') + ':\n')  # 显示执行操作
                                self.result_textbox.config(state="disabled")
                                is_first = False
                            self.result_textbox.config(state="normal")
                            self.result_textbox.insert(tk.END, '-'+folder+'\n')  # 显示执行内容
                            self.result_textbox.config(state="disabled")
                        except Exception as e:
                            self.result_textbox.config(state="normal")
                            self.result_textbox.insert(tk.END, self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_path') + ': ' + str(folder) + ', ' + self.translator.translate('fail_to_clear_pc_manager_beta_configuration_files_info') + ': ' + str(e) + '\n')  # 显示错误内容
                            self.result_textbox.config(state="disabled")

                # 删除注册表项
                registry_keys_to_delete = [
                    r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsMasterUI',
                    r'HKCU\Software\WindowsMaster'
                    r'HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run\WindowsMasterUI',
                    r'HKLM\Software\WOW6432Node\MSPCManager',
                    r'HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager',
                ]
                is_first = True
                for key in registry_keys_to_delete:
                    try:
                        subprocess.run(['reg', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)
                        if is_first:
                            self.result_textbox.config(state="normal")
                            self.result_textbox.insert(tk.END, '\n' + self.translator.translate('clearing_pc_manager_beta_registries') + ':\n')  # 显示执行操作
                            self.result_textbox.config(state="disabled")
                            is_first = False
                        self.result_textbox.config(state="normal")
                        self.result_textbox.insert(tk.END, '-'+key+'\n')  # 显示执行内容
                        self.result_textbox.config(state="disabled")
                    except Exception as e:
                        self.result_textbox.config(state="normal")
                        self.result_textbox.insert(tk.END, self.translator.translate('fail_to_clear_pc_manager_beta_registries_info') + ': ' + str(e) + '\n')  # 显示错误内容
                        self.result_textbox.config(state="disabled")

                return '\n' + self.translator.translate("uninstalled_cleanup_pc_manager_beta_config_and_files")
            else:
                return self.translator.translate('user_canceled')
        except Exception as e:
            return f"{self.translator.translate('uninstall_pc_manager_beta_error_info')}: {str(e)}"
