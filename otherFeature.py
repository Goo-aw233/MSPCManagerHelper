import iso3166
import subprocess
import tkinter as tk
import webbrowser
import winreg
from tkinter import messagebox, filedialog

class OtherFeature:
    def __init__(self, translator):
        self.translator = translator

    def view_installed_antivirus(self):
        try:
            # 设置隐藏窗口的标志
            creationflags = subprocess.CREATE_NO_WINDOW

            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell.exe", "-Command",
                 ("Get-WmiObject -Namespace 'Root\\SecurityCenter2' -Class 'AntivirusProduct' | "
                  "Select-Object displayName, pathToSignedProductExe, pathToSignedReportingExe, productState | "
                  "Format-List")],
                capture_output=True, text=True, check=True, creationflags=creationflags
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

    def pc_manager_faq(self):
        try:
            # 打开指定的 URL
            webbrowser.open("https://docs.qq.com/doc/DR2FrVkJmT0NuZ0Zx")
            return self.translator.translate("pc_manager_faq_opened")
        except Exception as e:
            return f"{self.translator.translate('pc_manager_faq_error')}: {str(e)}"

    # def join_preview_program(self):
    #     try:
    #         # 打开指定的 URL
    #         webbrowser.open("https://forms.office.com/r/v1LX7SKWTs")
    #         return self.translator.translate("join_preview_program_opened")
    #     except Exception as e:
    #         return f"{self.translator.translate('join_preview_program_error')}: {str(e)}"

    def restart_pc_manager_service(self):
        try:
            # 查询服务状态
            query_result = subprocess.run(
                ["sc.exe", "query", "PCManager Service Store"],
                capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "RUNNING" in query_result.stdout:
                # 停止服务
                stop_result = subprocess.run(
                    ["sc.exe", "stop", "PCManager Service Store"],
                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                if stop_result.returncode != 0:
                    error_message = self.translator.translate("stop_pc_manager_service_error")
                    error_code = stop_result.returncode
                    if error_code == 5:
                        error_message += f"\n{self.translator.translate('pc_manager_service_error_code_5')}"
                    elif error_code == 1056:
                        error_message += f"\n{self.translator.translate('pc_manager_service_error_code_1056')}"
                    elif error_code == 1060:
                        error_message += f"\n{self.translator.translate('pc_manager_service_error_code_1060')}"
                    else:
                        error_message += f"\n{self.translator.translate('pc_manager_service_error_code')}: {error_code}"
                    return error_message
                else:
                    print(self.translator.translate("stopping_pc_manager_service"))

            # 启动服务
            start_result = subprocess.run(
                ["sc.exe", "start", "PCManager Service Store"],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if start_result.returncode != 0:
                error_message = self.translator.translate("start_pc_manager_service_error")
                error_code = start_result.returncode
                if error_code == 5:
                    error_message += f"\n{self.translator.translate('pc_manager_service_error_code_5')}"
                elif error_code == 1056:
                    error_message += f"\n{self.translator.translate('pc_manager_service_error_code_1056')}"
                elif error_code == 1060:
                    error_message += f"\n{self.translator.translate('pc_manager_service_error_code_1060')}"
                else:
                    error_message += f"\n{self.translator.translate('pc_manager_service_error_code')}: {error_code}"
                return error_message
            else:
                print(self.translator.translate("starting_pc_manager_service"))

            return self.translator.translate("pc_manager_service_restarted_successfully")
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('start_pc_manager_service_error')}: {str(e)}\n{self.translator.translate('pc_manager_service_error_code')}: {e.returncode}"

    def switch_pc_manager_region(self):
        pcm_reg_path = r"SOFTWARE\WOW6432Node\MSPCManager Store"
        pcm_region_value_name = "InstallRegionCode"

        # 获取 region_code 值
        def region():
            self.region_code = entry.get()
            (messagebox.showerror(self.translator.translate("unknown_pc_manager_region_code"),
                                  self.translator.translate("unknown_pc_manager_region_code_warning"),
                                  parent=root)
            if str(self.region_code).upper() not in iso3166.countries_by_alpha2 else (setattr(self, 'cancel', False) or root.destroy()))

        root, self.cancel = tk.Tk(), True
        root.title(self.translator.translate("switch_pc_manager_region_notice"))
        root.geometry("450x150")
        root.resizable(False, False)

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
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pcm_reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    winreg.DeleteValue(key, pcm_region_value_name)
                except FileNotFoundError:
                    pass  # 如果值不存在，忽略错误

                winreg.SetValueEx(key, pcm_region_value_name, 0, winreg.REG_SZ, self.region_code.upper())

            message = self.translator.translate("switch_region_completed")
            message += f"\n{self.translator.translate('restart_pc_manager_to_apply_changes')}"
        except OSError as e:
            message = f"\n{self.translator.translate('switch_region_to_cn_error')}: {str(e)}"

        # 读取 InstallRegionCode 的值
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, pcm_reg_path, 0, winreg.KEY_READ) as key:
                pcm_region_code = winreg.QueryValueEx(key, pcm_region_value_name)[0]
                message += f"\n{self.translator.translate('current_pc_manager_region')}: {pcm_region_code}"
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

            results = []
            for compute_files_path in paths_to_compute_files:
                sha256_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA256 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha256_hash = sha256_result.stdout.strip()

                sha1_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm SHA1 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                sha1_hash = sha1_result.stdout.strip()

                md5_result = subprocess.run(
                    ["powershell.exe", "-Command",
                     f"Get-FileHash -Path '{compute_files_path}' -Algorithm MD5 | Select-Object -ExpandProperty Hash"],
                    capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
                md5_hash = md5_result.stdout.strip()

                results.append(f"{self.translator.translate('path_to_compute_files')}: {compute_files_path}\n"
                               f"{self.translator.translate('sha256_hash')}: {sha256_hash}\n"
                               f"{self.translator.translate('sha1_hash')}: {sha1_hash}\n"
                               f"{self.translator.translate('md5_hash')}: {md5_hash}")

            return "\n\n".join(results)
        except subprocess.CalledProcessError as e:
            return f"{self.translator.translate('compute_files_hash_error')}: {e.stderr.strip()}"
        except Exception as e:
            return f"{self.translator.translate('compute_files_hash_error')}: {str(e)}"