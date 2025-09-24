import ctypes
import subprocess
import webbrowser


class InstallViaMicrosoftStore:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def check_if_microsoft_store_is_installed(self):
        check_if_microsoft_store_is_installed_cmd = [
            "powershell.exe",
            "-Command",
            "Get-AppxPackage -Name Microsoft.WindowsStore"
        ]
        try:
            result = subprocess.run(
                check_if_microsoft_store_is_installed_cmd,
                capture_output=True, text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "PackageFamilyName : Microsoft.WindowsStore_8wekyb3d8bbwe" in result.stdout:
                self.microsoft_store_is_installed()
            else:
                self.microsoft_store_is_not_installed()
        except Exception as e:
            self.microsoft_store_is_not_installed()

    def microsoft_store_is_installed(self):
        open_microsoft_store_cmd = [
            "cmd.exe",
            "/C",
            "start",
            "ms-windows-store://pdp/?ProductId=9PM860492SZD"
        ]
        try:
            subprocess.run(
                open_microsoft_store_cmd,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return print("Microsoft Store is opened successfully.")
        except Exception as e:
            print(f"an_error_occurred_when_opening_microsoft_store")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    def microsoft_store_is_not_installed(self):
        try:
            webbrowser.open("https://apps.microsoft.com/detail/9PM860492SZD")
            return print("microsoft_store_page_opened_in_browser")
        except Exception as e:
            print(f"an_error_occurred_when_opening_microsoft_store_page")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")
