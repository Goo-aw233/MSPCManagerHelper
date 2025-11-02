import os
import requests
import shutil
import subprocess
import tempfile
import tkinter as tk
import webbrowser
import winreg
from tkinter import filedialog, messagebox
from pathlib import Path


class InstallationFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox

    def textbox(self, message):
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disabled")
        self.result_textbox.update_idletasks()  # 刷新界面

    def refresh_result_textbox(self):
        pass

    def download_from_winget(self):
        try:
            # 检查 WinGet 是否安装
            result = subprocess.Popen(['where.exe', 'winget.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = result.communicate()
            if result.returncode != 0:
                return self.translator.translate("winget_not_installed")

            # 弹出提示框询问用户是否同意 Microsoft Store 源协议
            self.textbox(self.translator.translate("winget_msstore_source_agreement") + '\n')
            response = messagebox.askyesnocancel(
                self.translator.translate("winget_msstore_source_agreement_notice"),
                self.translator.translate("ask_winget_msstore_source_agreement")
            )
            if response is None:
                return self.translator.translate("user_canceled")
            elif not response:
                return self.translator.translate("disagree_winget_msstore_source_agreement")

            # 使用 WinGet 搜索 Microsoft PC Manager
            result = subprocess.Popen(['winget.exe', 'search', 'Microsoft PC Manager', '--source', 'msstore', '--accept-source-agreements'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = result.communicate()
            if result.returncode != 0:
                # 无互联网连接
                if result.returncode == 2316632067:
                    return self.translator.translate("winget_not_internet_connection")
                # 找不到结果
                elif result.returncode == 2316632084:
                    return self.translator.translate("winget_no_results_found")
                # 需要重置 msstore 源或无互联网连接
                elif result.returncode == 2316632139:
                    return self.translator.translate("winget_source_reset_needed")
                else:
                    stderr = stderr.strip() if stderr else self.translator.translate("winget_not_error_info")
                    stdout = stdout.strip() if stdout else self.translator.translate("winget_not_output")
                    return f"{self.translator.translate('winget_error')}\n{self.translator.translate('winget_error_info')}: {stderr}\n{self.translator.translate('winget_error_code')}: {result.returncode}\n{self.translator.translate('winget_output')}: {stdout}"

            # 使用 WinGet 安装 Microsoft PC Manager
            result = subprocess.Popen(['winget.exe', 'install', 'Microsoft PC Manager', '--source', 'msstore', '--accept-source-agreements', '--accept-package-agreements'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = result.communicate()
            self.textbox(self.translator.translate("downloading_pc_manager_from_winget") + '\n')
            if result.returncode != 0:
                # Microsoft PC Manager 早已安装
                if result.returncode == 2316632107:
                    return self.translator.translate("already_installed_pc_manager_from_winget")
                else:
                    stderr = stderr.strip() if stderr else self.translator.translate("winget_not_error_info")
                    stdout = stdout.strip() if stdout else self.translator.translate("winget_not_output")
                    return f"{self.translator.translate('winget_error')}\n{self.translator.translate('winget_error_info')}: {stderr}\n{self.translator.translate('winget_error_code')}: {result.returncode}\n{self.translator.translate('winget_output')}: {stdout}"

            return self.translator.translate("pc_manager_has_been_installed_from_winget")
        except Exception as e:
            return f"{self.translator.translate('winget_error')}\n{self.translator.translate('winget_error_info')}: {str(e)}\n{self.translator.translate('winget_not_error_code')}"

    def download_from_msstore(self):
        try:
            # 检测 Microsoft Store 是否安装
            result = subprocess.run(
                ['powershell.exe', '-Command', 'Get-AppxPackage -Name Microsoft.WindowsStore'],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if 'PackageFamilyName : Microsoft.WindowsStore_8wekyb3d8bbwe' in result.stdout:
                try:
                    # 如果安装了 Microsoft Store，运行命令
                    subprocess.run(
                        ["start", "ms-windows-store://pdp/?ProductId=9PM860492SZD"],
                           check=True, shell=True)
                    return self.translator.translate("download_from_msstore_app_opened")
                except Exception as e:
                    return f"{self.translator.translate('download_from_msstore_app_error')}: {str(e)}"
            else:
                # 如果没有安装 Microsoft Store，打开指定的 URL
                webbrowser.open("https://apps.microsoft.com/detail/9PM860492SZD")
                return self.translator.translate("download_from_msstore_site_opened")
        except Exception as e:
            return f"{self.translator.translate('download_from_msstore_site_error')}: {str(e)}"

    def install_for_all_users(self):
        # 打开文件选择对话框选择文件
        all_users_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not all_users_application_package_file_path:
            return self.translator.translate("no_files_selected")

        # 弹出提示框询问用户是否选择许可证文件
        response_for_all_users_license = messagebox.askyesnocancel(
            self.translator.translate("install_for_all_users_license_select_notice"),
            self.translator.translate("install_for_all_users_license_select")
        )

        all_users_dependency_package_paths = None
        if response_for_all_users_license:  # 使用许可证
            all_users_license_path = filedialog.askopenfilename(
                filetypes=[("License.xml", "*.xml"), ("*", "*")])
            if not all_users_license_path:
                return self.translator.translate("no_files_selected")
        elif response_for_all_users_license is None:
            return self.translator.translate("user_canceled")
        else:
            all_users_license_path = None

        # 弹出提示框询问用户是否选择依赖包
        response_for_all_users_dependency = messagebox.askyesnocancel(
            self.translator.translate("install_for_all_users_dependency_package_select_notice"),
            self.translator.translate("install_for_all_users_dependency_package_select")
        )

        if response_for_all_users_dependency:  # 选择依赖包
            all_users_dependency_package_paths = filedialog.askopenfilenames(
                filetypes=[("MSIX", "*.msix"),
                           ("Appx", "*.appx"),
                           ("*", "*")])
            if not all_users_dependency_package_paths:
                return self.translator.translate("no_files_selected")
        elif response_for_all_users_dependency is None:
            return self.translator.translate("user_canceled")

        try:
            # 构建 Dism.exe 命令
            all_users_dism_command = ['Dism.exe', '/Online', '/Add-ProvisionedAppxPackage',
                                      f'/PackagePath:{all_users_application_package_file_path}']

            if all_users_license_path:  # 使用许可证文件
                all_users_dism_command.append(f'/LicensePath:{all_users_license_path}')
            else:  # 不使用许可证文件
                all_users_dism_command.append('/SkipLicense')

            if all_users_dependency_package_paths:  # 使用依赖包，若不使用则跳过
                for dependency_path in all_users_dependency_package_paths:
                    all_users_dism_command.append(f'/DependencyPackagePath:{dependency_path}')

            # 使用 Dism.exe 安装应用
            result = subprocess.run(all_users_dism_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return self.translator.translate("install_for_all_users_success")
            else:
                return self.translator.translate("install_for_all_users_error") + f": {result.stderr}\n{result.stdout}"
        except FileNotFoundError as e:
            return f"{self.translator.translate('dism_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return self.translator.translate("install_for_all_users_error") + f": {str(e)}"

    def install_for_current_user(self):
        # 打开文件选择对话框选择文件
        current_user_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not current_user_application_package_file_path:
            return self.translator.translate("no_files_selected")

        # 弹出提示框询问用户是否选择依赖包
        response_for_current_user_dependency = messagebox.askyesnocancel(
            self.translator.translate("install_for_current_user_dependency_package_select_notice"),
            self.translator.translate("install_for_current_user_dependency_package_select")
        )

        current_user_dependency_package_paths = None
        if response_for_current_user_dependency:  # 选择依赖包
            current_user_dependency_package_paths = filedialog.askopenfilenames(
                filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                           ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                           ("*", "*")])
            if not current_user_dependency_package_paths:
                return self.translator.translate("no_files_selected")
        elif response_for_current_user_dependency is None:
            return self.translator.translate("user_canceled")

        try:
            # 构建 Add-AppxPackage 命令
            command = ['powershell.exe', '-Command',
                       f'Add-AppxPackage -Path "{current_user_application_package_file_path}"']
            if current_user_dependency_package_paths:  # 使用依赖包，若不使用则跳过
                dependency_paths = ",".join([f'"{additional_dependency_paths}"' for additional_dependency_paths in current_user_dependency_package_paths])
                command.append(f'-DependencyPath {dependency_paths}')

            # 执行 Add-AppxPackage 命令安装应用
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return self.translator.translate("install_for_current_user_success")
            else:
                return self.translator.translate("install_for_current_user_error") + f": {result.stderr}\n{result.stdout}"
        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return self.translator.translate("install_for_current_user_error") + f": {str(e)}"

    def reinstall_pc_manager(self):
        whether_to_reinstall_for_all_users = messagebox.askyesnocancel(
            self.translator.translate("ask_whether_to_reinstall_for_all_users"),
            self.translator.translate("whether_to_reinstall_for_all_users")
        )

        if whether_to_reinstall_for_all_users is None:
            return self.translator.translate("user_canceled")

        if whether_to_reinstall_for_all_users:
            command = [
                "powershell.exe",
                "-Command",
                "Get-AppxPackage -AllUsers *Microsoft.MicrosoftPCManager* | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppxManifest.xml\"}"
            ]
        else:
            command = [
                "powershell.exe",
                "-Command",
                "Get-AppxPackage *Microsoft.MicrosoftPCManager* | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppxManifest.xml\"}"
            ]

        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

        if result.returncode == 0:
            # 资源正在使用
            if "0x80073D02" in result.stderr:
                return self.translator.translate("reintsall_pc_manager_error_code_0x80073D02") + f"\n\n{result.stdout}\n{result.stderr}"
            return self.translator.translate("reinstall_pc_manager_success")
        # 需要以管理员身份运行
        elif result.returncode == 1:
            return self.translator.translate("reintsall_pc_manager_error_code_1") + f"\n\n{result.stdout}\n{result.stderr}"
        # AppxManifest.xml 损坏
        elif result.returncode == 2:
            return self.translator.translate("reintsall_pc_manager_error_code_2") + f"\n\n{result.stdout}\n{result.stderr}"
        else:
            return f"{self.translator.translate('reinstall_pc_manager_error')}\n{self.translator.translate('reinstall_pc_manager_error_code')}: {result.returncode}\n\n{result.stdout}\n{result.stderr}"

    def update_from_application_package(self):
        # 打开文件选择对话框选择文件
        update_application_package_file_path = filedialog.askopenfilename(
            filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not update_application_package_file_path:
            return self.translator.translate("no_files_selected")

        # 弹出提示框询问用户是否选择依赖包
        response_for_update_dependency = messagebox.askyesnocancel(
            self.translator.translate("update_from_application_package_dependency_package_select_notice"),
            self.translator.translate("update_from_application_package_dependency_package_select")
        )

        update_dependency_package_paths = None
        if response_for_update_dependency:  # 选择依赖包
            update_dependency_package_paths = filedialog.askopenfilenames(
                filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                           ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                           ("*", "*")])
            if not update_dependency_package_paths:
                return self.translator.translate("no_files_selected")
        elif response_for_update_dependency is None:
            return self.translator.translate("user_canceled")

        try:
            # 构建 Add-AppxPackage 命令
            command = ['powershell.exe', '-Command',
                       f'Add-AppxPackage -Path "{update_application_package_file_path}"']
            if update_dependency_package_paths:  # 使用依赖包，若不使用则跳过
                dependency_paths = ",".join([f'"{additional_dependency_paths}"' for additional_dependency_paths in
                                             update_dependency_package_paths])
                command.append(f'-DependencyPath {dependency_paths}')

            # 执行 Add-AppxPackage 命令安装应用
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0:
                return self.translator.translate("update_from_application_package_success")
            else:
                return self.translator.translate("update_from_application_package_error") + f": {result.stderr}\n{result.stdout}"
        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return self.translator.translate("update_from_application_package_error") + f": {str(e)}"

    def install_from_appxmanifest(self):
        # 询问是否已经安装过 Microsoft PC Manager
        responding_to_whether_or_not_it_was_installed = messagebox.askyesnocancel(
            self.translator.translate("warning"),
            self.translator.translate("install_from_appxmanifest_warn")
        )

        if responding_to_whether_or_not_it_was_installed is None or not responding_to_whether_or_not_it_was_installed:
            return self.translator.translate("user_canceled")

        # 打开文件选择对话框选择文件
        pc_manager_package_file_path_str = filedialog.askopenfilename(
            filetypes=[("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                       ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                       ("*", "*")])

        if not pc_manager_package_file_path_str:
            return self.translator.translate("user_canceled")
        
        pc_manager_package_file_path = Path(pc_manager_package_file_path_str)

        try:
            # 创建临时目录
            mspcmanagerhelper_temp_dir = Path(tempfile.gettempdir()) / "MSPCManagerHelper"   # MSPCManagerHelper 临时目录
            if not mspcmanagerhelper_temp_dir.exists():
                os.makedirs(mspcmanagerhelper_temp_dir)

            # 复制文件到 MSPCManagerHelper 临时目录并重命名为 .zip
            pc_manager_package_file_name = pc_manager_package_file_path.name   # Microsoft PC Manager 包文件名
            pc_manager_zip_package_file_path = mspcmanagerhelper_temp_dir / (pc_manager_package_file_name + ".zip")  # 将包文件名去掉后缀添加 .zip
            self.textbox(self.translator.translate("install_from_appxmanifest_copying_files"))
            shutil.copyfile(pc_manager_package_file_path, pc_manager_zip_package_file_path) # 将源文件复制到 MSPCManagerHelper 临时目录

            # 解压文件
            pc_manager_package_unpacked_file_path = mspcmanagerhelper_temp_dir / pc_manager_package_file_path.stem # 解压后的文件路径
            self.textbox(self.translator.translate("install_from_appxmanifest_unzipping_files"))
            shutil.unpack_archive(pc_manager_zip_package_file_path, pc_manager_package_unpacked_file_path)  # 解压文件

            # 检测解压后的文件夹内是否还有 .msix/.appx 文件
            pc_manager_msix_files = [f.name for f in pc_manager_package_unpacked_file_path.iterdir() if f.suffix == '.msix']
            pc_manager_appx_files = [f.name for f in pc_manager_package_unpacked_file_path.iterdir() if f.suffix == '.appx']
            if not pc_manager_msix_files and not pc_manager_appx_files:
                pass
            else:
                # 检查文件名中是否带有 x64 或 arm64
                x64_file = next((f for f in pc_manager_msix_files if 'x64' in f), None)
                arm64_file = next((f for f in pc_manager_msix_files if 'arm64' in f), None)
                if not x64_file and not arm64_file:
                    # 清理 MSPCManagerHelper 临时目录下的文件
                    for temporary_files in mspcmanagerhelper_temp_dir.iterdir():  # 遍历 MSPCManagerHelper 临时目录下的文件
                        self.textbox(self.translator.translate("install_from_appxmanifest_cleaning_up"))
                        if temporary_files.is_file():  # 如果是文件就删除
                            temporary_files.unlink()
                        elif temporary_files.is_dir():  # 如果是目录就删除
                            shutil.rmtree(temporary_files)
                    return self.translator.translate("install_from_appxmanifest_no_match_pc_manager_architecture")

                # 读取 PROCESSOR_ARCHITECTURE 的值以确定包
                processor_architecture = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"), "PROCESSOR_ARCHITECTURE"
                )[0]

                if processor_architecture == "AMD64" and x64_file:
                    pc_manager_zip_package_file_path = mspcmanagerhelper_temp_dir / (x64_file + ".zip")  # 将包文件名去掉后缀添加 .zip
                    shutil.copyfile(pc_manager_package_unpacked_file_path / x64_file, pc_manager_zip_package_file_path)    # 复制文件到 MSPCManagerHelper 临时目录
                    self.textbox(self.translator.translate("install_from_appxmanifest_copying_files"))
                    unpacked_dir = mspcmanagerhelper_temp_dir / Path(x64_file).stem
                    shutil.unpack_archive(pc_manager_zip_package_file_path, unpacked_dir)    # 解压文件
                    self.textbox(self.translator.translate("install_from_appxmanifest_unzipping_files") + '\n')
                    pc_manager_package_unpacked_file_path = unpacked_dir   # 解压后的文件路径
                elif processor_architecture == "ARM64" and arm64_file:
                    pc_manager_zip_package_file_path = mspcmanagerhelper_temp_dir / (arm64_file + ".zip")    # 将包文件名去掉后缀添加 .zip
                    shutil.copyfile(pc_manager_package_unpacked_file_path / arm64_file, pc_manager_zip_package_file_path)  # 复制文件到 MSPCManagerHelper 临时目录
                    self.textbox(self.translator.translate("install_from_appxmanifest_copying_files"))
                    unpacked_dir = mspcmanagerhelper_temp_dir / Path(arm64_file).stem
                    shutil.unpack_archive(pc_manager_zip_package_file_path, unpacked_dir)  # 解压文件
                    self.textbox(self.translator.translate("install_from_appxmanifest_unzipping_files") + '\n')
                    pc_manager_package_unpacked_file_path = unpacked_dir   # 解压后的文件路径
                else:
                    # 清理 MSPCManagerHelper 临时目录下的文件
                    for temporary_files in mspcmanagerhelper_temp_dir.iterdir():  # 遍历 MSPCManagerHelper 临时目录下的文件
                        self.textbox(self.translator.translate("install_from_appxmanifest_cleaning_up"))
                        if temporary_files.is_file():  # 如果是文件就删除
                            temporary_files.unlink()
                        elif temporary_files.is_dir():  # 如果是目录就删除
                            shutil.rmtree(temporary_files)
                    return self.translator.translate("install_from_appxmanifest_no_match_architecture")

            # 将最后解压的文件夹复制到 %ProgramFiles% 下
            pc_manager_program_files_path = Path(os.environ['ProgramFiles']) / pc_manager_package_unpacked_file_path.name   # Microsoft PC Manager 安装路径
            if not pc_manager_program_files_path.exists():
                os.makedirs(pc_manager_program_files_path)
            self.textbox(self.translator.translate("install_from_appxmanifest_copying_files") + '\n')
            subprocess.run(["Robocopy.exe", str(pc_manager_package_unpacked_file_path), str(pc_manager_program_files_path),   # 复制文件夹
                "/E",  # 复制所有子目录，包括空目录
                "/XD", "AppxMetadata",  # 排除目录
                "/XF", "[Content_Types].xml", "AppxBlockMap.xml", "AppxSignature.p7x"  # 排除文件
            ], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # 修改 AppxManifest.xml 文件
            appxmanifest_path = pc_manager_program_files_path / "AppxManifest.xml" # AppxManifest.xml 文件路径
            self.textbox(self.translator.translate("install_from_appxmanifest_modifying_appxmanifest") + '\n')
            with open(appxmanifest_path, 'r', encoding='utf-8') as file:    # 读取 AppxManifest.xml 文件
                lines = file.readlines()    # 读取文件内容

            with open(appxmanifest_path, 'w', encoding='utf-8') as file:    # 写入 AppxManifest.xml 文件
                for line in lines:  # 遍历文件内容
                    if '<TargetDeviceFamily' in line and not line.strip().startswith('<!--'):   # 如果找到 <TargetDeviceFamily> 标签
                        indent = line[:len(line) - len(line.lstrip())]  # 缩进
                        file.write(f"{indent}<!-- {line.strip()} -->\n")    # 注释原始行
                        file.write(f"{indent}<TargetDeviceFamily Name=\"Windows.Universal\" MinVersion=\"0.0.0.0\" MaxVersionTested=\"0.0.0.0\"/>\n")   # 添加新行
                    else:
                        file.write(line)    # 写入原始行

            # 弹出提示框询问用户是否选择依赖包
            response_for_dependency = messagebox.askyesnocancel(
                self.translator.translate("install_from_appxmanifest_dependency_package_select_notice"),
                self.translator.translate("install_from_appxmanifest_dependency_package_select")
            )

            if response_for_dependency:  # 选择依赖包
                dependency_package_paths = filedialog.askopenfilenames(filetypes=[
                    ("MSIX/MSIXBundle", "*.msix;*.msixbundle"),
                    ("Appx/AppxBundle", "*.appx;*.appxbundle"),
                    ("*", "*")])
                if not dependency_package_paths:    # 如果没有选择文件
                    # 清理 MSPCManagerHelper 临时目录下的文件
                    for temporary_files in mspcmanagerhelper_temp_dir.iterdir():  # 遍历 MSPCManagerHelper 临时目录下的文件
                        self.textbox(self.translator.translate("install_from_appxmanifest_cleaning_up"))
                        if temporary_files.is_file():  # 如果是文件就删除
                            temporary_files.unlink()
                        elif temporary_files.is_dir():  # 如果是目录就删除
                            shutil.rmtree(temporary_files)
                    return self.translator.translate("no_files_selected")

                for dependency_path in dependency_package_paths:
                    self.textbox(self.translator.translate("install_from_appxmanifest_installing_dependency_package") + '\n')
                    subprocess.run(['powershell.exe', '-Command', f'Add-AppxPackage -Path "{dependency_path}"'],
                                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                    )

            # 注册 AppxManifest.xml
            self.textbox(self.translator.translate("install_from_appxmanifest_registering_app") + '\n')
            subprocess.run(['powershell.exe', '-Command', f'Add-AppxPackage -Register "{pc_manager_program_files_path}\\AppxManifest.xml"'],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )

            # 询问是否注册服务
            response_for_service = messagebox.askyesno(
                self.translator.translate("install_from_appxmanifest_register_svc_notice"),
                self.translator.translate("install_from_appxmanifest_register_svc")
            )

            if response_for_service:
                # 检查服务 "PCManager Service Store" 是否存在
                service_store_check = subprocess.run(['powershell.exe', '-Command', 'Get-Service -Name "PCManager Service Store"'],
                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )

                # 检查服务 "PC Manager Service" 是否存在
                service_store_old_check = subprocess.run(['powershell.exe', '-Command', 'Get-Service -Name "PC Manager Service"'],
                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )

                if any(check.returncode == 0 for check in [service_store_check, service_store_old_check]):
                    messagebox.showwarning(
                        self.translator.translate("install_from_appxmanifest_svc_exists_warning"),
                        self.translator.translate("install_from_appxmanifest_svc_exists")
                    )
                else:
                    # 创建服务
                    self.textbox(self.translator.translate("install_from_appxmanifest_registering_svc") + '\n')
                    service_create = subprocess.run(['sc.exe', 'create', 'PCManager Service Store', 'binPath=',
                         f'"{pc_manager_program_files_path}\\PCManager\\MSPCManagerService.exe"', 'DisplayName=', '"MSPCManager Service (Store)"', 'start=', 'auto'],
                        capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                    )

                    if service_create.returncode == 0:
                        # 设置服务描述
                        subprocess.run(['sc.exe', 'description', 'PCManager Service Store', '"Microsoft PCManager Service For Store"'],
                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        # 启动服务
                        subprocess.run(['sc.exe', 'start', 'PCManager Service Store'],
                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                        )

            # 清理 MSPCManagerHelper 临时目录下的文件
            for temporary_files in mspcmanagerhelper_temp_dir.iterdir():  # 遍历 MSPCManagerHelper 临时目录下的文件
                self.textbox(self.translator.translate("install_from_appxmanifest_cleaning_up"))
                if temporary_files.is_file():    # 如果是文件就删除
                    temporary_files.unlink()
                elif temporary_files.is_dir():   # 如果是目录就删除
                    shutil.rmtree(temporary_files)

            return self.translator.translate("install_from_appxmanifest_success")
        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return self.translator.translate("install_from_appxmanifest_error") + f": {str(e)}"

    def install_wv2_runtime(self, program):
        mspcmanagerhelper_temp_dir = Path(tempfile.gettempdir()) / "MSPCManagerHelper"   # MSPCManagerHelper 临时目录
        wv2_installer_temp_path = mspcmanagerhelper_temp_dir / "MicrosoftEdgeWebView2Setup.exe"    # EdgeWebView2 安装程序临时下载路径
        wv2_installer_download_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"    # EdgeWebView2 安装程序下载链接
        edgeupdate_log_source = Path(os.environ['ProgramData']) / 'Microsoft' / 'EdgeUpdate' / 'Log' / 'MicrosoftEdgeUpdate.log'    # EdgeUpdate.exe 日志源目录
        edgeupdate_log_destination = Path(os.environ['UserProfile']) / 'Desktop' / 'MicrosoftEdgeUpdate.log'  # EdgeUpdate.exe 日志输出目录

        try:
            # 检查临时目录是否存在，不存在则创建
            if not mspcmanagerhelper_temp_dir.exists():
                os.makedirs(mspcmanagerhelper_temp_dir, exist_ok=True)

            # 下载文件
            response = requests.get(wv2_installer_download_url)
            if response.status_code == 200:
                with open(wv2_installer_temp_path, 'wb') as file:
                    file.write(response.content)
            else:
                return self.translator.translate("wv2_download_error")

            # 运行安装程序
            program.current_process = subprocess.Popen([str(wv2_installer_temp_path), "/install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = program.current_process.communicate()

            if program.cancelled:
                return self.translator.translate("wv2_installation_cancelled")

            if program.current_process.returncode == 0:
                return self.translator.translate("wv2_runtime_install_success") + '\n' + self.translator.translate("wv2_runtime_installer_download_link")
            # 需要以管理员身份运行
            elif program.current_process.returncode == 2147747880:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {program.current_process.returncode}\n{self.translator.translate('wv2_runtime_already_installed')}"
            # 文件夹需要删除
            elif program.current_process.returncode == 2147747596:
                shutil.copy(edgeupdate_log_source, edgeupdate_log_destination)
                return f"{self.translator.translate('wv2_installer_exit_code')}: {program.current_process.returncode}\n{self.translator.translate('wv2_installer_exit_code_0x8004070c')}\n{self.translator.translate('edgeupdate_log_export_path')}: {edgeupdate_log_destination}\n{self.translator.translate('seek_help_from_system_administrator')}"
            # 无文件夹写入权限
            elif program.current_process.returncode == 2147942583:
                shutil.copy(edgeupdate_log_source, edgeupdate_log_destination)
                return f"{self.translator.translate('wv2_installer_exit_code')}: {program.current_process.returncode}\n{self.translator.translate('wv2_installer_exit_code_0x800700b7')}\n{self.translator.translate('edgeupdate_log_export_path')}: {edgeupdate_log_destination}\n{self.translator.translate('seek_help_from_system_administrator')}"
            # 其他未知报错
            else:
                shutil.copy(edgeupdate_log_source, edgeupdate_log_destination)
                return f"{self.translator.translate('wv2_installer_exit_code')}: {program.current_process.returncode}\n{self.translator.translate('wv2_installer_error')}\n{self.translator.translate('edgeupdate_log_export_path')}: {edgeupdate_log_destination}\n{self.translator.translate('seek_help_from_system_administrator')}"

        except Exception as e:
            return f"{self.translator.translate('wv2_download_error_info')}: {str(e)}"
        finally:
            # 删除临时目录
            if mspcmanagerhelper_temp_dir.exists():
                shutil.rmtree(mspcmanagerhelper_temp_dir)
            program.current_process = None
