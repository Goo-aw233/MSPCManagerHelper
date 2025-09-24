import ctypes
import subprocess
import winreg


class GetMicrosoftEdgeWebView2RuntimeVersion:

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def get_microsoft_edge_webview2_runtime_version(self, selected_versions):
        results = []

        if selected_versions.get('global'):
            results.append(self._get_global_microsoft_edge_webview2_version())
        
        if selected_versions.get('system'):
            results.append(self._get_system_microsoft_edge_webview2_version())
        
        return "\n".join(filter(None, results))

    def _get_global_microsoft_edge_webview2_version(self):
        _GLOBAL_MICROSOFT_EDGE_WEBVIEW2_RUNTIME_KEY = r"SOFTWARE\\WOW6432Node\\Microsoft\\EdgeUpdate\\Clients\\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _GLOBAL_MICROSOFT_EDGE_WEBVIEW2_RUNTIME_KEY, 0, winreg.KEY_READ) as key:
                global_microsoft_edge_webview2_runtime_version, regtype = winreg.QueryValueEx(key, "pv")
                return f"{self.translator.translate('global_microsoft_edge_webview2_runtime_version')}: {global_microsoft_edge_webview2_runtime_version}"
        except FileNotFoundError:
            return self.translator.translate("global_microsoft_edge_webview2_runtime_version_not_found")
        except Exception as e:
            return (f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")

    def _get_system_microsoft_edge_webview2_version(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ) as key:
                current_build_number, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
                if int(current_build_number) < 26100:
                    return self.translator.translate("system_microsoft_edge_webview2_runtime_not_supported")
        except Exception as e:
            return (f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")

        _SYSTEM_MICROSOFT_EDGE_WEBVIEW2_RUNTIME_PATH = r"$Env:SystemRoot\\System32\\Microsoft-Edge-WebView\\msedgewebview2.exe"
        try:
            command = [
                "powershell.exe",
                "-Command",
                f'(Get-Item "{_SYSTEM_MICROSOFT_EDGE_WEBVIEW2_RUNTIME_PATH}").VersionInfo.ProductVersion'
            ]
            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True)
            if result.stderr:
                 return f"{self.translator.translate('system_microsoft_edge_webview2_runtime_version_not_found')}\n{result.stderr.strip()}"
            system_microsoft_edge_webview2_runtime_version = result.stdout.strip()
            return f"{self.translator.translate('system_microsoft_edge_webview2_runtime_version')}: {system_microsoft_edge_webview2_runtime_version}"
        except (FileNotFoundError, subprocess.CalledProcessError):
            return self.translator.translate("system_microsoft_edge_webview2_runtime_version_not_found")
        except Exception as e:
            return (f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")
