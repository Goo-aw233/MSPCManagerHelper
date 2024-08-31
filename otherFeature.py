import json
import os
import subprocess
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
