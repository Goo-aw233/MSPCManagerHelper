import os
import subprocess
import winreg
from pathlib import Path
from tkinter import messagebox

from core.program_logger import ProgramLogger


class EnableLongPathsHandler:
    def __init__(self, logger, translator):
        self.logger = logger
        self.translator = translator

    def on_enable_long_paths_click(self):
        try:
            self.enable_long_paths_with_winreg()
        except Exception as e_winreg:
            self.logger.error(f"Failed with winreg: {e_winreg}")
            try:
                self.enable_long_paths_with_reg_exe()
            except Exception as e_reg_exe:
                self.logger.error(f"Failed with reg.exe: {e_reg_exe}")
                try:
                    self.enable_long_paths_with_windows_powershell()
                except Exception as e_windows_powershell:
                    self.logger.error(f"Failed with Windows Powershell: {e_windows_powershell}")
                    err_msg = self.translator.translate("check_the_logs_for_more_details").format(
                        log_path=ProgramLogger.get_log_file_path()
                    )
                    if messagebox.showerror(
                        self.translator.translate("error"),
                        err_msg
                    ):
                        log_dir = Path(ProgramLogger.get_log_file_path()).parent
                        os.startfile(log_dir)

    def enable_long_paths_with_winreg(self):
        key_path = r"SYSTEM\\CurrentControlSet\\Control\\FileSystem"
        value_name = "LongPathsEnabled"
        try:
            self.logger.info("Modifying registry via winreg...")
            self.logger.info(f"Log file path: {ProgramLogger.get_log_file_path()}")
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
                try:
                    winreg.QueryValueEx(key, value_name)
                    winreg.DeleteValue(key, value_name)
                    self.logger.info(f"{value_name} deleted successfully.")
                except FileNotFoundError:
                    self.logger.info(f"{value_name} not found, no need to delete.")
                winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 1)
                self.logger.info(f"{value_name} set to 1.")
        except PermissionError:
            self.logger.error("Insufficient permissions to modify the registry. Please run as administrator.")
        except Exception as e:
            self.logger.error(f"Error occurred while modifying the registry: {e}")

    def enable_long_paths_with_reg_exe(self):
        key = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem"
        value = "LongPathsEnabled"
        delete_cmd = ["reg.exe", "delete", key, "/v", value, "/f"]
        set_cmd = ["reg.exe", "add", key, "/v", value, "/t", "REG_DWORD", "/d", "1", "/f"]
        try:
            self.logger.info("Modifying registry via reg.exe...")
            subprocess.run(delete_cmd, check=True, shell=False)
            self.logger.info(f"{value} deleted successfully.")
        except subprocess.CalledProcessError:
            self.logger.info(f"{value} not found, no need to delete.")
        try:
            subprocess.run(set_cmd, check=True, shell=False)
            self.logger.info(f"{value} set to 1.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to set {value}: {e}")

    def enable_long_paths_with_windows_powershell(self):
        delete_cmd = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "Remove-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem' -Name 'LongPathsEnabled' -ErrorAction SilentlyContinue"
        ]
        set_cmd = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem' -Name 'LongPathsEnabled' -Type DWord -Value 1"
        ]
        try:
            self.logger.info("Modifying registry via Windows Powershell...")
            subprocess.run(delete_cmd, check=True, shell=False)
            self.logger.info("LongPathsEnabled deleted successfully.")
        except subprocess.CalledProcessError:
            self.logger.info("LongPathsEnabled not found, no need to delete.")
        try:
            subprocess.run(set_cmd, check=True, shell=False)
            self.logger.info("LongPathsEnabled set to 1.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to set LongPathsEnabled: {e}")
