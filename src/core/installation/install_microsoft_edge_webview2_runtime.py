import ctypes
import subprocess
import os
import tempfile
import urllib.request


class InstallMicrosoftEdgeWebView2Runtime:
    _PROGRAM_TEMP_DIR = os.path.join(tempfile.gettempdir(), "MSPCManagerHelper")
    _MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_PATH = os.path.join(_PROGRAM_TEMP_DIR,
                                                                            "MicrosoftEdgeWebView2Setup.exe")
    _MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()
        if not os.path.exists(self._PROGRAM_TEMP_DIR):
            os.makedirs(self._PROGRAM_TEMP_DIR, exist_ok=True)

    def install_microsoft_edge_webview2_runtime(self):
        self._download_microsoft_edge_webview2_runtime_installer()

    def _download_microsoft_edge_webview2_runtime_installer(self):
        try:
            urllib.request.urlretrieve(
                InstallMicrosoftEdgeWebView2Runtime._MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_URL,
                InstallMicrosoftEdgeWebView2Runtime._MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_PATH
            )
            self._install_microsoft_edge_webview2_runtime_runtime()
        except Exception as e:
            print(f"an_error_occurred_when_downloading_microsoft_edge_webview2_runtime_installer")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    def _install_microsoft_edge_webview2_runtime_runtime(self):
        try:
            result = subprocess.run(
                [InstallMicrosoftEdgeWebView2Runtime._MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_PATH,
                 "/install"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self._cleanup_temporary_files()
                return print("microsoft_edge_webview2_runtime_installed_successfully")
            # User Has Canceled the Task
            elif result.returncode == 2147747856:
                self._cleanup_temporary_files()
                return print("user_has_canceled_the_task")
            # Need to Run as Administrator
            elif result.returncode == 2147747880:
                self._cleanup_temporary_files()
                return print("microsoft_edge_webview2_runtime_installer_needs_to_run_as_administrator")
            else:
                self._cleanup_temporary_files()
                print("an_error_occurred_when_installing_microsoft_edge_webview2_runtime")
                return print(f"return_code: {result.returncode}\n")
        except Exception as e:
            self._cleanup_temporary_files()
            print(f"an_error_occurred_when_installing_microsoft_edge_webview2_runtime")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    def _cleanup_temporary_files(self):
        try:
            if os.path.exists(
                    InstallMicrosoftEdgeWebView2Runtime._MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_PATH):
                os.remove(InstallMicrosoftEdgeWebView2Runtime._MICROSOFT_EDGE_WEBVIEW2_RUNTIME_INSTALLER_DOWNLOAD_PATH)
        except Exception as e:
            print(f"an_error_occurred_when_cleaning_up_temporary_files")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")
