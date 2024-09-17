import os
import re
import subprocess
from tkinter import messagebox

class UninstallationFeature:
    def __init__(self, translator):
        self.translator = translator

    def uninstall_for_all_users(self):
        try:
            # 设置隐藏窗口的标志
            creationflags = subprocess.CREATE_NO_WINDOW

            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage -AllUsers | Where-Object {$_.name -like 'Microsoft.MicrosoftPCManager'} | "
                  "Remove-AppxPackage -AllUsers")],
                capture_output=True, text=True, creationflags=creationflags
            )

            if result.returncode == 0:
                return self.translator.translate("uninstall_for_all_users_success")
            elif result.returncode == 1:
                return self.translator.translate("uninstall_for_current_users_error_code_1")
            else:
                return f"{self.translator.translate('uninstall_for_all_users_error')}: {result.stderr.strip()}\n{self.translator.translate('uninstall_for_all_users_error_code')}: {result.returncode}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_all_users_error')}: {str(e)}"

    def uninstall_for_current_user(self):
        try:
            # 设置隐藏窗口的标志
            creationflags = subprocess.CREATE_NO_WINDOW

            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-AppxPackage | Where-Object {$_.Name -like '*Microsoft.MicrosoftPCManager*'} | "
                  "ForEach-Object {Remove-AppxPackage -Package $_.PackageFullName}")],
                capture_output=True, text=True, creationflags=creationflags
            )

            if result.returncode == 0:
                return self.translator.translate("uninstall_for_current_user_success")
            elif result.returncode == 1:
                return self.translator.translate("uninstall_for_current_users_error_code_1")
            else:
                return f"{self.translator.translate('uninstall_for_current_user_error')}: {result.stderr.strip()}\n{self.translator.translate('uninstall_for_current_user_error_code')}: {result.returncode}"
        except Exception as e:
            return f"{self.translator.translate('uninstall_for_current_user_error')}: {str(e)}"

    def uninstall_beta(self):
        try:
            pcm_path = os.path.join(os.environ['ProgramFiles'], 'Microsoft PC Manager')
            if not os.path.exists(pcm_path):
                return self.translator.translate("pcm_beta_not_found")

            # 检测 Uninst.exe 是否存在
            pcm_uninst_exe = os.path.join(pcm_path, 'Uninst.exe')
            if not os.path.exists(pcm_uninst_exe):
                return self.translator.translate("pcm_beta_not_found")

            # 运行卸载程序
            result = subprocess.run([pcm_uninst_exe], capture_output=True, text=True)
            if result.returncode != 0:
                return f"{self.translator.translate('uninstall_pcm_beta_error_info')}: {result.stderr.strip()}"

            # 弹出窗口询问是否清理配置和文件
            tf = True
            while tf:
                if re.search(r'Uninst\w+\.exe', os.popen('tasklist.exe').read()):
                    pass
                else:
                    tf = False
            if not messagebox.askyesno(self.translator.translate("cleanup_pcm_beta_config_and_files_notice"),
                                       self.translator.translate("cleanup_pcm_beta_config_and_files")):
                return self.translator.translate("pcm_beta_uninstalled")

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
            for folder in folders_to_delete:
                if os.path.exists(folder):
                    subprocess.run(['rmdir', '/S', '/Q', folder], creationflags=subprocess.CREATE_NO_WINDOW)

            # 删除注册表项
            registry_keys_to_delete = [
                r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsMasterUI',
                r'HKCU\Software\WindowsMaster\HealthCheck',
                r'HKCU\Software\WindowsMaster\AntiVirus',
                r'HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run\WindowsMasterUI',
                r'HKLM\Software\WOW6432Node\MSPCManager',
                r'HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MSPCManager'
            ]
            for key in registry_keys_to_delete:
                subprocess.run(['reg', 'delete', key, '/f'], creationflags=subprocess.CREATE_NO_WINDOW)

            return self.translator.translate("uninstalled_cleanup_pcm_beta_config_and_files")
        except Exception as e:
            return f"{self.translator.translate('uninstall_pcm_beta_error_info')}: {str(e)}"
