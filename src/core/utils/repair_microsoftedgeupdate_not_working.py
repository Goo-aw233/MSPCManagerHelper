import ctypes
import os
import shutil
import winreg
from pathlib import Path


class RepairMicrosoftEdgeUpdateNotWorking:

    _IFEO = r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options"
    _MICROSOFT_EDGE_PARENT_FOLDER_IN_PROGRAM_FILES_X86 = r"%ProgramFiles(x86)%\\Microsoft"
    _MICROSOFT_EDGE_WEBVIEW2_FOLDER_IN_PROGRAM_FILES_X86 = r"%ProgramFiles(x86)%\\Microsoft\\EdgeWebView"
    _MICROSOFTEDGEUPDATE_EXE_NAME = r"MicrosoftEdgeUpdate.exe"

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def repair_microsoftedgeupdate_not_working(self, repair_options):
        results = []
        if not any(repair_options.values()):
            return self.translator.translate("no_repair_option_selected")

        if repair_options.get('restore_edgeupdate_ifeo_key'):
            results.append(self._delete_microsoftedgeupdate_key_from_ifeo())
            results.append(self._add_ifeo_key_for_microsoftedgeupdate())

        if repair_options.get('remove_edge_parent_folder'):
            results.append(self._remove_microsoft_edge_parent_folder_in_program_files_x86())

        if repair_options.get('remove_webview2_folder'):
            results.append(self._remove_microsoft_edge_webview2_folder_in_program_files_x86())

        results.append(f"\n{self.translator.translate('successfully_repaired_microsoftedgeupdate_exe_not_working')}")
        return "\n".join(filter(None, results))

    def _add_ifeo_key_for_microsoftedgeupdate(self):
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                  fr"{self._IFEO}\{self._MICROSOFTEDGEUPDATE_EXE_NAME}") as key:
                winreg.SetValueEx(key, "DisableExceptionChainValidation", 0, winreg.REG_DWORD, 0)
            return self.translator.translate("successfully_added_ifeo_microsoftedgeupdate_key")
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_when_adding_the_microsoftedgeupdate_registry')}\n"
                    f"{self.translator.translate('exception_context')}: {e}")

    def _delete_microsoftedgeupdate_key_from_ifeo(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self._IFEO, 0, winreg.KEY_SET_VALUE) as parent_key:
                winreg.DeleteKey(parent_key, self._MICROSOFTEDGEUPDATE_EXE_NAME)
            return self.translator.translate("successfully_deleted_ifeo_microsoftedgeupdate_key")
        except FileNotFoundError:
            return self.translator.translate("microsoftedgeupdate_registry_key_not_found_skipping_deletion")
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_when_deleting_the_microsoftedgeupdate_registry')}\n"
                    f"{self.translator.translate('exception_context')}: {e}")

    def _remove_microsoft_edge_parent_folder_in_program_files_x86(self):
        program_files_x86 = os.environ.get('ProgramFiles(x86)')
        if program_files_x86:
            target_dir = Path(program_files_x86) / "Microsoft"
        else:
            target_dir = Path(self._MICROSOFT_EDGE_PARENT_FOLDER_IN_PROGRAM_FILES_X86)
        try:
            if target_dir.is_dir():
                shutil.rmtree(target_dir)
                return f"{self.translator.translate('successfully_removed_directory')}: {target_dir}"
            else:
                return f"{self.translator.translate('directory_not_found_or_is_not_a_directory')}: {target_dir}"
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_when_removing_directory')} {target_dir}\n"
                    f"{self.translator.translate('exception_context')}: {e}")

    def _remove_microsoft_edge_webview2_folder_in_program_files_x86(self):
        program_files_x86 = os.environ.get('ProgramFiles(x86)')
        if program_files_x86:
            target_dir = Path(program_files_x86) / "Microsoft" / "EdgeWebView"
        else:
            target_dir = Path(self._MICROSOFT_EDGE_WEBVIEW2_FOLDER_IN_PROGRAM_FILES_X86)
        try:
            if target_dir.is_dir():
                shutil.rmtree(target_dir)
                return f"{self.translator.translate('successfully_removed_directory')}: {target_dir}"
            else:
                return f"{self.translator.translate('directory_not_found_or_is_not_a_directory')}: {target_dir}"
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_when_removing_directory')} {target_dir}\n"
                    f"{self.translator.translate('exception_context')}: {e}")
