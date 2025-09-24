import ctypes
import shutil
import subprocess
from tkinter import messagebox

class InstallViaWinGet:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def check_if_winget_is_installed(self):
        try:
            if shutil.which("winget.exe"):
                self.install_via_winget()
            else:
                self._winget_not_installed()
        except Exception as e:
            print(f"an_error_occurred_while_checking_if_winget_was_installed")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    def install_via_winget(self):
        response = messagebox.askyesnocancel(
                "winget_msstore_source_agreement",
                "whether_agree_with_the_msstore_source_agreement"
        )
        if response is None:
            return print("user_has_canceled_the_task")
        elif not response:
            return print("disagree_with_winget_msstore_source_agreement")
        else:
            return self.search_for_microsoft_pc_manager()

    def search_for_microsoft_pc_manager(self):
        search_command = (
            "winget.exe",
            "search",
            "9PM860492SZD",
            "--source", "msstore",
            "--accept-source-agreements"
        )
        try:
            result = subprocess.run(
                search_command,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                self.install_microsoft_pc_manager()
            # No Internet Connection
            elif result.returncode == 2316632067:
                print("winget_not_internet_connection")
                return print(f"return_code: {result.returncode}"
                             f"stdout: {result.stdout.strip()}"
                             f"stderr: {result.stderr.strip()}")
            # Not Result Found
            elif result.returncode == 2316632084:
                print("winget_no_results_found")
                return print(f"return_code: {result.returncode}"
                             f"stdout: {result.stdout.strip()}"
                             f"stderr: {result.stderr.strip()}")
            # Requires Resetting the msstore Source or No Internet Connection
            elif result.returncode == 2316632139:
                print("winget_source_reset_needed")
                return print(f"return_code: {result.returncode}"
                             f"stdout: {result.stdout.strip()}"
                             f"stderr: {result.stderr.strip()}")
            # Other Errors
            else:
                print(f"an_error_occurred_while_searching_for_microsoft_pc_manager")
                return print(f"return_code: {result.returncode}"
                             f"stdout: {result.stdout.strip()}"
                             f"stderr: {result.stderr.strip()}")
        except Exception as e:
            print(f"an_error_occurred_while_searching_for_microsoft_pc_manager")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    def install_microsoft_pc_manager(self):
        install_command = (
            "winget.exe",
            "install",
            "9PM860492SZD",
            "--source", "msstore",
            "--accept-source-agreements",
            "--accept-package-agreements"
        )
        print("downloading_from_winget")
        try:
            result = subprocess.run(
                install_command,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                return print("microsoft_pc_manager_installed_successfully")
            # Microsoft PC Manager Already Installed
            elif result.returncode == 2316632107:
                return print("already_installed_microsoft_pc_manager_from_winget")
            # Other Errors
            else:
                print(f"an_error_occurred_while_searching_for_microsoft_pc_manager")
                return print(f"return_code: {result.returncode}"
                             f"stdout: {result.stdout.strip()}"
                             f"stderr: {result.stderr.strip()}")
        except Exception as e:
            print(f"an_error_occurred_while_installing_microsoft_pc_manager")
            return (f"exception_context: {e}\n"
                    f"error_code: {self.error_code}\nerror_message: {self.error_message}")

    @staticmethod
    def _winget_not_installed():
        print("winget_is_not_installed")
