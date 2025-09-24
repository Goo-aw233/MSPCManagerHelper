import ctypes
import subprocess
from tkinter import filedialog


class InstallViaPowerShellForCurrentUser:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    @staticmethod
    def _select_application_package():
        filetypes = [
            ("MSIX", "*.Msix;*.MsixBundle"),
            ("Appx", "*.Appx;*.AppxBundle"),
            ("all_file_types", "*.*"),
        ]
        application_package_file_name = filedialog.askopenfilename(
            title="select_the_microsoft_pc_manager_application_package_file",
            filetypes=filetypes
        )
        return application_package_file_name

    @staticmethod
    def _select_dependencies_package():
        filetypes = [
            ("MSIX", "*.Msix"),
            ("Appx", "*.Appx"),
            ("all_file_types", "*.*"),
        ]
        dependencies_package_file_name = filedialog.askopenfilename(
            title="select_the_microsoft_pc_manager_dependency_package_file",
            filetypes=filetypes
        )
        return dependencies_package_file_name

    @staticmethod
    def _select_dependency_package_folder():
        dependency_package_folder_name = filedialog.askdirectory(
            title="select_the_microsoft_pc_manager_dependency_package_folder"
        )
        return dependency_package_folder_name

    def install_via_powershell_for_current_user(self):
        application_package = self._select_application_package()
        if not application_package:
            return print("no_files_selected")
        dependencies_package = self._select_dependencies_package()
        if not dependencies_package:
            return print("no_files_selected")
        dependency_package_folder = self._select_dependency_package_folder()
        if not dependency_package_folder:
            return print("no_files_selected")
        return None
