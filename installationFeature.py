import os
import shutil
import subprocess
import requests
import tempfile
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
                        ['powershell.exe', '-Command', 'Start-Process ms-windows-store://pdp/?ProductId=9PM860492SZD'], creationflags=subprocess.CREATE_NO_WINDOW)
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
                       ("*", "*")])

        if not all_users_application_package_file_path:
            return self.translator.translate("install_for_all_users_no_file_selected")

        # 弹出提示框询问用户是否选择许可证文件
        response_for_all_users_license = messagebox.askyesno(
            self.translator.translate("install_for_all_users_license_select_notice"),
            self.translator.translate("install_for_all_users_license_select")
        )

        all_users_dependency_package_path = None
        if response_for_all_users_license:  # 使用许可证
            all_users_license_path = filedialog.askopenfilename(
                filetypes=[("License.xml", "*.xml"), ("*", "*")])
            if not all_users_license_path:
                return self.translator.translate("install_for_all_users_no_file_selected")
        else:
            all_users_license_path = None

        # 弹出提示框询问用户是否选择依赖包
        response_for_all_users_dependency = messagebox.askyesno(
            self.translator.translate("install_for_all_users_dependency_package_select_notice"),
            self.translator.translate("install_for_all_users_dependency_package_select")
        )

        if response_for_all_users_dependency:  # 选择依赖包
            all_users_dependency_package_path = filedialog.askopenfilename(
                filetypes=[("Msix", "*.msix"),
                           ("*", "*")])
            if not all_users_dependency_package_path:
                return self.translator.translate("install_for_all_users_no_file_selected")

        try:
            # 构建 Dism.exe 命令
            all_users_dism_command = ['Dism.exe', '/Online', '/Add-ProvisionedAppxPackage',
                            f'/PackagePath:{all_users_application_package_file_path}']

            if all_users_license_path: # 使用许可证文件
                all_users_dism_command.append(f'/LicensePath:{all_users_license_path}')
            else: # 不使用许可证文件
                all_users_dism_command.append('/SkipLicense')

            if all_users_dependency_package_path: # 使用依赖包，若不使用则跳过
                all_users_dism_command.insert(-1, f'/DependencyPackagePath:{all_users_dependency_package_path}')

            # 使用 Dism.exe 安装应用
            result = subprocess.run(all_users_dism_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

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
                       ("*", "*")])

        if not current_user_application_package_file_path:
            return self.translator.translate("install_for_current_user_no_file_selected")

        # 弹出提示框询问用户是否选择依赖包
        response_for_current_user_dependency = messagebox.askyesno(
            self.translator.translate("install_for_current_user_dependency_package_select_notice"),
            self.translator.translate("install_for_current_user_dependency_package_select")
        )

        current_user_dependency_package_path = None
        if response_for_current_user_dependency:  # 选择依赖包
            current_user_dependency_package_path = filedialog.askopenfilename(
                filetypes=[("Msix", "*.msix"),
                           ("*", "*")])
            if not current_user_dependency_package_path:
                return self.translator.translate("install_for_current_user_no_file_selected")

        try:
            # 构建 Add-AppxPackage 命令
            command = ['powershell.exe', '-Command',
                       f'Add-AppxPackage -Path {current_user_application_package_file_path}']
            if current_user_dependency_package_path: # 使用依赖包，若不使用则跳过
                command.append(f'-DependencyPackages {current_user_dependency_package_path}')

            # 执行 Add-AppxPackage 命令安装应用
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return self.translator.translate("install_for_current_user_success")
            else:
                return self.translator.translate(
                    "install_for_current_user_error") + f": {result.stderr}\n{result.stdout}"
        except Exception as e:
            return self.translator.translate("install_for_current_user_error") + f": {str(e)}"

    def update_from_application_package(self):
        # 打开文件选择对话框选择文件
        update_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("Msix/MsixBundle", "*.msix;*.msixbundle"),
                       ("*", "*")])

        if not update_application_package_file_path:
            return self.translator.translate("update_from_application_package_no_file_selected")

        # 弹出提示框询问用户是否选择依赖包
        response_for_update_dependency = messagebox.askyesno(
            self.translator.translate("update_from_application_package_dependency_package_select_notice"),
            self.translator.translate("update_from_application_package_dependency_package_select")
        )

        update_dependency_package_path = None
        if response_for_update_dependency:  # 选择依赖包
            update_dependency_package_path = filedialog.askopenfilename(
                filetypes=[("Msix", "*.msix"),
                           ("*", "*")])
            if not update_dependency_package_path:
                return self.translator.translate("update_from_application_package_no_file_selected")

        try:
            # 构建 Add-AppxPackage 命令
            command = ['powershell.exe', '-Command',
                       f'Add-AppxPackage -Path {update_application_package_file_path}']
            if update_dependency_package_path:  # 使用依赖包，若不使用则跳过
                command.append(f'-DependencyPackages {update_dependency_package_path}')

            # 执行 Add-AppxPackage 命令安装应用
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return self.translator.translate("update_from_application_package_success")
            else:
                return self.translator.translate(
                    "update_from_application_package_error") + f": {result.stderr}\n{result.stdout}"
        except Exception as e:
            return self.translator.translate("update_from_application_package_error") + f": {str(e)}"

    def install_from_appxmanifest(self):
        return self.translator.translate("feature_unavailable")

    def install_wv2_runtime(self, app):
        wv2_installer_temp_dir = os.path.join(tempfile.gettempdir(), "MSPCManagerHelper")
        installer_path = os.path.join(wv2_installer_temp_dir, "MicrosoftEdgeWebView2Setup.exe")
        download_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"

        try:
            # 检查临时目录是否存在
            if os.path.exists(wv2_installer_temp_dir):
                shutil.rmtree(wv2_installer_temp_dir)  # 删除临时目录

            # 创建临时目录
            os.makedirs(wv2_installer_temp_dir, exist_ok=True)

            # 下载文件
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(installer_path, 'wb') as file:
                    file.write(response.content)
            else:
                return self.translator.translate("wv2_download_error")

            # 运行安装程序
            app.current_process = subprocess.Popen([installer_path, "/install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = app.current_process.communicate()

            if app.cancelled:
                return self.translator.translate("wv2_installation_cancelled")

            if app.current_process.returncode == 0:
                return self.translator.translate("wv2_runtime_install_success")
            elif app.current_process.returncode == 2147747880:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {app.current_process.returncode}\n{self.translator.translate('wv2_runtime_already_installed')}"
            elif app.current_process.returncode == 2147747596:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {app.current_process.returncode}\n{self.translator.translate('wv2_installer_exit_code_0x8004070c')}"
            elif app.current_process.returncode == 2147942583:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {app.current_process.returncode}\n{self.translator.translate('wv2_installer_exit_code_0x800700b7')}"
            else:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {app.current_process.returncode}\n{self.translator.translate('wv2_installer_error')}"
        except Exception as e:
            return f"{self.translator.translate('wv2_download_error_info')}: {str(e)}"
        finally:
            # 删除临时目录
            if os.path.exists(wv2_installer_temp_dir):
                shutil.rmtree(wv2_installer_temp_dir)
            app.current_process = None
