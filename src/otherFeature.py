import iso3166
import os
import subprocess
import sys
import tkinter as tk
import webbrowser
import win32api
import win32service
import win32serviceutil
import winreg
from tkinter import filedialog, messagebox, ttk

class OtherFeature:
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

    def view_installed_antivirus(self):
        try:
            # 查询注册表中的 InstallationType 值
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                installation_type = winreg.QueryValueEx(key, "InstallationType")[0]
                if installation_type == "Server":
                    return self.translator.translate("Windows_Server_does_not_support_this_feature")

            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell.exe", "-Command", "Get-CimInstance -Namespace ROOT\SecurityCenter2 -ClassName AntiVirusProduct"],
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
                    f"{self.translator.translate('display_name')}: "
                    f"{details.get('displayName', '')}\n"
                    f"{self.translator.translate('instance_GUID')}: "
                    f"{details.get('instanceGuid', '')}\n"
                    f"{self.translator.translate('path_to_signed_product_exe')}: "
                    f"{details.get('pathToSignedProductExe', '')}\n"
                    f"{self.translator.translate('path_to_signed_reporting_exe')}: "
                    f"{details.get('pathToSignedReportingExe', '')}\n"
                    f"{self.translator.translate('product_status')}: "
                    f"{details.get('productState', '')}\n"
                    f"{self.translator.translate('product_timestamp')}: "
                    f"{details.get('timestamp', '')}\n\n"
                )
            self.textbox(self.translator.translate("only_products_registered_to_Windows_Security_are_supported") + "\n")
            return formatted_result.strip()
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('powershell_error')}: {e.stderr.strip()}"
        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"

    def developer_options(self):
        try:
            # 打开开发者选项页
            subprocess.run(["start", "ms-settings:developers"],
                           check=True, shell=True)
            return self.translator.translate("developer_options_opened")
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('developer_options_error')}: {str(e)}"

    def repair_edge_wv2_setup(self):
        try:
            nsudolc_path = self.get_nsudolc_path()
            if not nsudolc_path:
                return "\n.join(messages)"

            msedgewebview2_key_name = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\MicrosoftEdgeUpdate.exe"

            # 删除注册表项
            result = subprocess.run(
                [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "reg.exe", "delete", msedgewebview2_key_name, "/f"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode != 0:
                return f"{self.translator.translate('repair_edge_wv2_setup_error')}: {result.stderr.strip()}"

            # 新建注册表项
            result = subprocess.run(
                [nsudolc_path, "-U:T", "-P:E", "-ShowWindowMode:Hide", "reg.exe", "add", msedgewebview2_key_name, "/v",
                 "DisableExceptionChainValidation", "/t", "REG_DWORD", "/d", "0", "/f"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode != 0:
                return f"{self.translator.translate('repair_edge_wv2_setup_error')}: {result.stderr.strip()}"            

            return self.translator.translate("repair_edge_wv2_setup_completed")
        except Exception as e:
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
            # 此处错误类型需要修改
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
            try:
                subprocess.run(["start", "ms-settings:regionformatting"], check=True, shell=True)
                return self.translator.translate("how_to_switch_pc_manager_region")
            except subprocess.CalledProcessError as e:
                return f"{self.translator.translate('error_opening_ms-settings')}: {str(e)}"

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

        label = ttk.Label(root, text=self.translator.translate("type_to_switch_pc_manager_region"))
        entry = ttk.Entry(root)  # 创建提示和输入框

        submit_button = ttk.Button(root, text=self.translator.translate("main_execute_button"), command=region)
        cancel_button = ttk.Button(root, text=self.translator.translate("main_cancel_button"), command=lambda: root.destroy())  # 按钮功能与样式

        label.pack(pady=10)
        entry.pack(pady=5)
        submit_button.pack(side=tk.LEFT, padx=95)
        cancel_button.pack(side=tk.LEFT)

        root.grab_set()  # 设置为模态窗口
        root.wait_window(root)

        if self.cancel:
            return self.translator.translate("user_canceled")

        # 写入 InstallRegionCode 的值
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pc_manager_registry_path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    winreg.DeleteValue(key, pc_manager_region_value_name)
                except FileNotFoundError:
                    pass  # 如果值不存在，忽略错误

                winreg.SetValueEx(key, pc_manager_region_value_name, 0, winreg.REG_SZ, self.region_code.upper())

            self.textbox(self.translator.translate("switch_region_completed"))
            self.textbox(self.translator.translate("restart_pc_manager_to_apply_changes"))
        except Exception as e:
            self.textbox(f"\n{self.translator.translate('switch_region_error')}: {str(e)}")

        # 读取 InstallRegionCode 的值
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pc_manager_registry_path, 0, winreg.KEY_READ) as key:
                pc_manager_region_code = winreg.QueryValueEx(key, pc_manager_region_value_name)[0]
                return f"\n{self.translator.translate('current_pc_manager_region')}: {pc_manager_region_code}"
        except FileNotFoundError:
            return f"\n{self.translator.translate('launch_pc_manager_to_continue')}"
        except Exception as e:
            return f"\n{self.translator.translate('current_pc_manager_region_error')}: {str(e)}"

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
        except FileNotFoundError as e:
            return f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}"
        except Exception as e:
            return f"{self.translator.translate('compute_files_hash_error')}: {str(e)}"

    def get_msedge_webview2_version(self):
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
            self.textbox(f"{self.translator.translate('system_msedge_webview2_version')}:\n{system_msedge_webview2_version}")
        except subprocess.CalledProcessError as e:
            self.textbox(f"{self.translator.translate('get_msedge_webview2_version_powershell_error')}: {e.stderr.strip()}")
        except FileNotFoundError as e:
            self.textbox(f"{self.translator.translate('powershell_not_found')}\n{str(e)}: {e.filename}")
        except Exception as e:
            self.textbox(f"{self.translator.translate('get_msedge_webview2_version_powershell_error')}: {str(e)}")

        try:
            # 读取注册表中的版本号
            msedge_webview2_reg_path = r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, msedge_webview2_reg_path) as key:
                user_msedge_webview2_version = winreg.QueryValueEx(key, "pv")[0]
                return f"{self.translator.translate('user_msedge_webview2_version')}:\n{user_msedge_webview2_version}"
        except FileNotFoundError:
            return self.translator.translate("msedge_webview2_version_registry_key_not_found")
        except Exception as e:
            return f"{self.translator.translate('get_msedge_webview2_version_registry_error')}: {str(e)}"
