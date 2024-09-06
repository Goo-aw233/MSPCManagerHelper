import json
import os
import shutil
import subprocess
import requests
import tempfile
import webbrowser
import winreg


class OtherFeature:
    def __init__(self, translator):
        self.translator = translator

    def view_installed_antivirus(self):
        try:
            # 设置隐藏窗口的标志
            creationflags = subprocess.CREATE_NO_WINDOW

            # 执行 PowerShell 命令
            result = subprocess.run(
                ["powershell", "-Command",
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

    def install_wv2_runtime(self, app):
        temp_dir = os.path.join(tempfile.gettempdir(), "MSPCManagerHelper")
        installer_path = os.path.join(temp_dir, "MicrosoftEdgeWebView2Setup.exe")
        download_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"

        try:
            # 检查临时目录是否存在
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)  # 删除临时目录

            # 创建临时目录
            os.makedirs(temp_dir, exist_ok=True)

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
            else:
                return f"{self.translator.translate('wv2_installer_exit_code')}: {app.current_process.returncode}\n{self.translator.translate('wv2_installer_error')}"
        except Exception as e:
            return f"{self.translator.translate('wv2_download_error_info')}: {str(e)}"
        finally:
            # 删除临时目录
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            app.current_process = None

    def join_preview_program(self):
        try:
            # 打开指定的 URL
            webbrowser.open("https://forms.office.com/r/v1LX7SKWTs")
            return self.translator.translate("pc_manager_faq_opened")
        except Exception as e:
            return f"{self.translator.translate('pc_manager_faq_error')}: {str(e)}"

    def restart_pc_manager_service(self):
        try:
            # 设置隐藏窗口的标志
            creationflags = subprocess.CREATE_NO_WINDOW

            # 停止服务
            stop_result = subprocess.run(
                ["sc.exe", "stop", "PCManager Service Store"],
                capture_output=True, text=True, creationflags=creationflags
            )
            if stop_result.returncode != 0:
                if stop_result.returncode == 5:
                    return f"{self.translator.translate('pc_manager_service_error_code_5')}\n{self.translator.translate('stop_pc_manager_service_error')}"
                else:
                    return f"{self.translator.translate('stop_pc_manager_service_error')}\n{self.translator.translate('pc_manager_service_error_code')}: {stop_result.returncode}"
            print(self.translator.translate("stopping_pc_manager_service"))

            # 启动服务
            start_result = subprocess.run(
                ["sc.exe", "start", "PCManager Service Store"],
                capture_output=True, text=True, creationflags=creationflags
            )
            if start_result.returncode != 0:
                if start_result.returncode == 5:
                    return f"{self.translator.translate('pc_manager_service_error_code_5')}\n{self.translator.translate('start_pc_manager_service_error')}"
                else:
                    return f"{self.translator.translate('start_pc_manager_service_error')}\n{self.translator.translate('pc_manager_service_error_code')}: {start_result.returncode}"
            print(self.translator.translate("starting_pc_manager_service"))

            return self.translator.translate("service_restarted_successfully")
        except Exception as e:
            return f"{self.translator.translate('service_restart_error')}: {str(e)}\n{self.translator.translate('pc_manager_service_error_code')}: {e.errno if hasattr(e, 'errno') else 'N/A'}"

    def switch_region_to_cn(self):
        try:
            reg_path = r"SOFTWARE\WOW6432Node\MSPCManager Store"
            value_name = "InstallRegionCode"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    winreg.DeleteValue(key, value_name)
                except FileNotFoundError:
                    pass  # 如果值不存在，忽略错误

                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, "CN")

            message = self.translator.translate("switch_region_to_cn_completed")
        except OSError as e:
            message = f"{self.translator.translate('switch_region_to_cn_error')}: {str(e)}"

        # 读取 InstallRegionCode 的值
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
                region_code = winreg.QueryValueEx(key, value_name)[0]
                message += f"\n{self.translator.translate('current_pcm_region')}: {region_code}"
        except OSError as e:
            message += f"\n{self.translator.translate('current_pcm_region_error')}: {str(e)}"

        return message

# 示例 Translator 类
class Translator:
    def __init__(self, locale):
        self.locale = locale
        self.translations = self.load_translations()

    def load_translations(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, 'locales', f'{self.locale}.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def translate(self, key):
        return self.translations.get(key, key)
