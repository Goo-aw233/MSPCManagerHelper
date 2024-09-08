import subprocess
import webbrowser
from tkinter import filedialog
from tkinter import messagebox

class InstallationFeature:
    def __init__(self, translator):
        self.translator = translator

    def download_from_winget(self):
        return self.translator.translate("feature_unavailable")

    def download_from_store(self):
        try:
            # 检测 Microsoft Store 是否安装
            result = subprocess.run(
                ['powershell.exe', '-Command', 'Get-AppxPackage -Name Microsoft.WindowsStore'],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if 'Microsoft.WindowsStore' in result.stdout:
                try:
                    # 如果安装了 Microsoft Store，运行命令
                    subprocess.run(
                        ['powershell.exe', '-Command', 'Start-Process ms-windows-store://pdp/?ProductId=9PM860492SZD'],
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    return self.translator.translate("download_from_store_app_opened")
                except Exception as e:
                    return f"{self.translator.translate('download_from_store_app_error')}: {str(e)}"
            else:
                # 如果没有安装 Microsoft Store，打开指定的 URL
                webbrowser.open("https://www.microsoft.com/store/productid/9PM860492SZD")
                return self.translator.translate("download_from_store_site_opened")
        except Exception as e:
            return f"{self.translator.translate('download_from_store_site_error')}: {str(e)}"

    def install_for_all_users(self):
        # 打开文件选择对话框选择文件
        all_users_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("Msix/MsixBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not all_users_application_package_file_path:
            return self.translator.translate("install_for_all_users_no_file_selected")

        # 弹出提示框询问用户是否选择许可证文件
        user_response = messagebox.askyesno(
            self.translator.translate("install_for_all_users_license_select_notice"),
            self.translator.translate("install_for_all_users_license_select")
        )

        try:
            if user_response:  # 使用许可证
                all_users_license_path = filedialog.askopenfilename(
                    filetypes=[("License.xml", "*.xml"), ("*", "*")])
                if all_users_license_path:
                    # 执行 DISM.exe 命令安装应用并指定许可证文件
                    result = subprocess.run(
                        ['DISM.exe', '/Online', '/Add-ProvisionedAppxPackage',
                         f'/PackagePath:{all_users_application_package_file_path}',
                         f'/LicensePath:{all_users_license_path}'],
                        capture_output=True, text=True)
                else:
                    return self.translator.translate("install_for_all_users_no_file_selected")
            else:  # 不使用许可证
                # 执行 DISM.exe 命令安装应用并跳过许可证
                result = subprocess.run(
                    ['DISM.exe', '/Online', '/Add-ProvisionedAppxPackage', f'/PackagePath:{all_users_application_package_file_path}', '/SkipLicense'],
                    capture_output=True, text=True)

            if result.returncode == 0:
                return self.translator.translate("install_for_all_users_success")
            else:
                return self.translator.translate("install_for_all_users_error") + f": {result.stderr}\n{result.stdout}"
        except Exception as e:
            return self.translator.translate("install_for_all_users_error") + f": {str(e)}"

    def install_for_current_user(self):
        # 打开文件选择对话框选择文件
        current_user_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("Msix/MsixBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not current_user_application_package_file_path:
            return self.translator.translate("install_for_current_user_no_file_selected")

        try:
            # 执行 Add-AppxPackage 命令安装应用
            result = subprocess.run(
                ['powershell.exe', '-Command', f'Add-AppxPackage -Path {current_user_application_package_file_path}'],
                capture_output=True, text=True)

            if result.returncode == 0:
                return self.translator.translate("install_for_current_user_success")
            else:
                return self.translator.translate(
                    "install_for_current_user_error") + f": {result.stderr}\n{result.stdout}"
        except Exception as e:
            return self.translator.translate("install_for_current_user_error") + f": {str(e)}"
