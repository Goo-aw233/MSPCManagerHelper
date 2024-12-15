import iso3166
import os
import subprocess
import tkinter as tk
import webbrowser
import win32api
import win32service
import win32serviceutil
import winreg
from tkinter import messagebox, filedialog

class OtherFeature:
    def __init__(self, translator, result_textbox=None):
        self.translator = translator
        self.result_textbox = result_textbox

    def textbox(self, message):
        self.result_textbox.config(state="normal")
        self.result_textbox.insert(tk.END, message + "\n")
        self.result_textbox.config(state="disable")
        self.result_textbox.update_idletasks()  # 刷新界面

    def refresh_result_textbox(self):
        pass

    def view_installed_antivirus(self):
        try:
            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-WmiObject -Namespace 'Root\\SecurityCenter2' -Class 'AntivirusProduct' | "
                  "Select-Object displayName, pathToSignedProductExe, pathToSignedReportingExe, productState | "
                  "Format-List")],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = result.stdout.strip()
            if not output:
                return self.translator.translate("no_results")

            # 解析输出并格式化
            formatted_result = ""
            for line in output.split("\n\n"):
                details = {}
                for item in line.split("\n"):
                    key, value = item.split(":", 1)
                    details[key.strip()] = value.strip()
                formatted_result += (
                    f"{self.translator.translate('display_name')}: {details.get('displayName', '')}\n"
                    f"{self.translator.translate('path_to_signed_product_exe')}: "
                    f"{details.get('pathToSignedProductExe', '')}\n"
                    f"{self.translator.translate('path_to_signed_reporting_exe')}: "
                    f"{details.get('pathToSignedReportingExe', '')}\n"
                    f"{self.translator.translate('status')}: {details.get('productState', '')}\n\n"
                )
            return formatted_result.strip()
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('powershell_error')}: {e.stderr.strip()}"
        except FileNotFoundError:
            return self.translator.translate("powershell_not_found")

    def developer_options(self):
        try:
            # 打开开发者选项页
            subprocess.run(["start", "ms-settings:developers"], check=True, shell=True)
            return self.translator.translate("developer_options_opened")
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('developer_options_error')}: {str(e)}"

    def repair_edge_wv2_setup(self):
        try:
            # 删除注册表项
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options", 0,
                                winreg.KEY_ALL_ACCESS) as key:
                winreg.DeleteKey(key, "MicrosoftEdgeUpdate.exe")

            # 新建注册表项
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MicrosoftEdgeUpdate.exe") as key:
                winreg.SetValueEx(key, "DisableExceptionChainValidation", 0, winreg.REG_DWORD, 0)

            return self.translator.translate("repair_edge_wv2_setup_completed")
        except OSError as e:
            return f"{self.translator.translate('repair_edge_wv2_setup_error')}: {str(e)}"

    def pc_manager_docs(self):
        try:
            # 根据语言选择 URL
            pc_manager_docs_url = "https://docs.qq.com/doc/DR2FrVkJmT0NuZ0Zx" if self.translator.locale == "zh-cn" else "https://mspcmanager.github.io/mspcm-docs"

            # 打开指定的 URL
            webbrowser.open(pc_manager_docs_url)
            return self.translator.translate("pc_manager_docs_opened")
        except Exception as e:
            return f"{self.translator.translate('pc_manager_docs_error')}: {str(e)}"

    """
    def join_preview_program(self):
        try:
            # 打开指定的 URL
            webbrowser.open("https://forms.office.com/r/v1LX7SKWTs")
            return self.translator.translate("join_preview_program_opened")
        except Exception as e:
            return f"{self.translator.translate('join_preview_program_error')}: {str(e)}"
    """

    def restart_pc_manager_service(self):
        pc_manager_service_name = "PCManager Service Store"
        wait_secs = 5  # 设置等待时间为 5 秒

        try:
            # 检查服务是否存在
            service_status = win32serviceutil.QueryServiceStatus(pc_manager_service_name)
        except win32api.error as e:
            # 需要以管理员身份运行
            if e.winerror == 5:
                return f"{self.translator.translate('pc_manager_service_error_code_5')}\n{str(e)}"
            # 服务已在运行
            elif e.winerror == 1056:
                return f"{self.translator.translate('pc_manager_service_error_code_1056')}\n{str(e)}"
            # 服务未安装
            elif e.winerror == 1060:
                return f"{self.translator.translate('pc_manager_service_error_code_1060')}\n{str(e)}"
            else:
                return f"{self.translator.translate('start_pc_manager_service_error')}: {str(e)}"

        try:
            # 检查服务是否在运行
            if service_status[1] == win32service.SERVICE_RUNNING:
                self.textbox(self.translator.translate("stopping_pc_manager_service") + '\n')
                win32serviceutil.StopService(pc_manager_service_name)  # 停止服务
                win32serviceutil.WaitForServiceStatus(pc_manager_service_name, win32service.SERVICE_STOPPED, waitSecs=wait_secs)   # 等待服务停止
                self.textbox(self.translator.translate("starting_pc_manager_service") + '\n')
                win32serviceutil.StartService(pc_manager_service_name) # 启动服务
                win32serviceutil.WaitForServiceStatus(pc_manager_service_name, win32service.SERVICE_RUNNING, waitSecs=wait_secs)   # 等待服务启动
                return self.translator.translate("pc_manager_service_restarted_successfully")
            else:
                self.textbox(self.translator.translate("starting_pc_manager_service") + '\n')
                win32serviceutil.StartService(pc_manager_service_name) # 启动服务
                win32serviceutil.WaitForServiceStatus(pc_manager_service_name, win32service.SERVICE_RUNNING, waitSecs=wait_secs)   # 等待服务启动
                return self.translator.translate("pc_manager_service_restarted_successfully")
        except win32api.error as e:
            return f"{self.translator.translate('start_pc_manager_service_error')}: {str(e)}"

    def switch_pc_manager_region(self):
        pc_manager_registry_path = r"SOFTWARE\WOW6432Node\MSPCManager Store"
        pc_manager_region_value_name = "InstallRegionCode"

        # 询问版本号是否大于等于 3.14.0.0
        user_response = messagebox.askyesnocancel(
            self.translator.translate("ask_if_version_above_3_14_0_0"),
            self.translator.translate("select_pc_manager_version")
        )

        if user_response is None:
            return self.translator.translate("user_canceled")
        elif user_response:
            subprocess.run(["start", "ms-settings:regionformatting"], check=True, shell=True)
            return self.translator.translate("how_to_switch_pc_manager_region")

        # 获取 region_code 值
        def region():
            self.region_code = entry.get()
            (messagebox.showerror(self.translator.translate("unknown_pc_manager_region_code"),
                                  self.translator.translate("unknown_pc_manager_region_code_warning"),
                                  parent=root)
             if str(self.region_code).upper() not in iso3166.countries_by_alpha2 else (
                        setattr(self, 'cancel', False) or root.destroy()))

        root, self.cancel = tk.Tk(), True
        root.title(self.translator.translate("switch_pc_manager_region_notice"))
        root.geometry("450x150")
        root.resizable(False, False)

        # 设置自定义图标
        switch_region_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'MSPCManagerHelper-256.ico')
        root.iconbitmap(switch_region_icon_path)

        label = tk.Label(root, text=self.translator.translate("type_to_switch_pc_manager_region"))
        entry = tk.Entry(root)  # 创建提示和输入框

        submit_button = tk.Button(root, text=self.translator.translate("main_execute_button"), command=region, width=10,
                                  height=1)
        cancel_button = tk.Button(root, text=self.translator.translate("main_cancel_button"),
                                  command=lambda: root.destroy(), width=10, height=1)  # 按钮功能与样式

        label.pack(pady=10)
        entry.pack(pady=5)
        submit_button.pack(side=tk.LEFT, padx=95)
        cancel_button.pack(side=tk.LEFT)

        root.grab_set()  # 设置为模态窗口
        root.wait_window(root)

        if self.cancel:
            return self.translator.translate("user_canceled")

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pc_manager_registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    winreg.DeleteValue(key, pc_manager_region_value_name)
                except FileNotFoundError:
                    pass  # 如果值不存在，忽略错误

                winreg.SetValueEx(key, pc_manager_region_value_name, 0, winreg.REG_SZ, self.region_code.upper())

            message = self.translator.translate("switch_region_completed")
            message += f"\n{self.translator.translate('restart_pc_manager_to_apply_changes')}"
        except OSError as e:
            message = f"\n{self.translator.translate('switch_region_error')}: {str(e)}"

        # 读取 InstallRegionCode 的值
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pc_manager_registry_path, 0, winreg.KEY_READ) as key:
                pc_manager_region_code = winreg.QueryValueEx(key, pc_manager_region_value_name)[0]
                message += f"\n{self.translator.translate('current_pc_manager_region')}: {pc_manager_region_code}"
        except FileNotFoundError:
            message += f"\n{self.translator.translate('launch_pc_manager_to_continue')}"
        except OSError as e:
            message += f"\n{self.translator.translate('current_pc_manager_region_error')}: {str(e)}"

        return message

    def compute_files_hash(self):
        try:
            paths_to_compute_files = filedialog.askopenfilenames(filetypes=[("*", "*")])
            if not paths_to_compute_files:
                return self.translator.translate("no_compute_files_selected")

            for compute_files_path in paths_to_compute_files:
                self.textbox(f"{self.translator.translate('path_to_compute_files')}: {compute_files_path}")

                sha1_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA1 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha1_hash = sha1_result.stdout.strip()
                self.textbox(f"SHA1:\n{sha1_hash}\n")

                sha256_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA256 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha256_hash = sha256_result.stdout.strip()
                self.textbox(f"SHA256:\n{sha256_hash}\n")

                """
                sha384_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA384 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha384_hash = sha384_result.stdout.strip()
                self.textbox(f"SHA384:\n{sha384_hash}\n")

                sha512_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA512 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha512_hash = sha512_result.stdout.strip()
                self.textbox(f"SHA512:\n{sha512_hash}\n")
                """

                md5_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm MD5 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                md5_hash = md5_result.stdout.strip()
                self.textbox(f"MD5:\n{md5_hash}\n\n")

            return self.translator.translate("compute_files_hash_success")
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('compute_files_hash_error')}: {e.stderr.strip()}"
        except Exception as e:
            return f"{self.translator.translate('compute_files_hash_error')}: {str(e)}"

    def get_msedge_webview2_version(self):
        messages = []

        try:
            # 使用 PowerShell 命令读取 System32 的 msedgewebview2.exe 的版本号
            root_msedge_webview2 = (
                "$SystemMSEdgeWebView2Path = \"$env:SystemRoot\\System32\\Microsoft-Edge-WebView\\msedgewebview2.exe\"; "
                "$SystemMSEdgeWebView2PathVersionInfo = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($SystemMSEdgeWebView2Path); "
                "$SystemMSEdgeWebView2PathVersionInfo.ProductVersion"
            )
            result = subprocess.run(
                ["powershell.exe", "-Command", root_msedge_webview2],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            system_msedge_webview2_version = result.stdout.strip()
            messages.append(f"{self.translator.translate('system_msedge_webview2_version')}: {system_msedge_webview2_version}")
        except subprocess.CalledProcessError as e:
            messages.append(f"{self.translator.translate('get_msedge_webview2_version_powershell_error')}: {e.stderr.strip()}")

        try:
            # 读取注册表中的版本号
            msedge_webview2_reg_path = r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, msedge_webview2_reg_path) as key:
                user_msedge_webview2_version = winreg.QueryValueEx(key, "pv")[0]
                messages.append(f"{self.translator.translate('user_msedge_webview2_version')}: {user_msedge_webview2_version}")
        except FileNotFoundError:
            messages.append(self.translator.translate("msedge_webview2_version_registry_key_not_found"))
        except OSError as e:
            messages.append(f"{self.translator.translate('get_msedge_webview2_version_registry_error')}: {str(e)}")

        return "\n".join(messages)
