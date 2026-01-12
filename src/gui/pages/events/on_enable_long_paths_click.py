import winreg
import subprocess
from tkinter import messagebox


class OnEnableLongPathsClick:
    @staticmethod
    def enable_long_paths(logger=None, log_file_path=None, app_translator=None):
        reg_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"
        value_name = "LongPathsEnabled"

        def enable_with_winreg():
            logger.info("Enabling long paths via winreg.")
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
                    try:
                        winreg.QueryValueEx(key, value_name)
                        logger.info(f"{value_name} exists, set to 1.")
                    except FileNotFoundError:
                        logger.info(f"{value_name} does not exist, will create.")
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 1)
            except Exception as e:
                logger.error(f"Failed to Open or Set Registry Value: {e}")
                raise

        def enable_with_reg_exe():
            logger.info("Enabling long paths via reg.exe.")
            check_cmd = [
                "reg.exe", "query",
                f"HKEY_LOCAL_MACHINE\\{reg_path}",
                "/v", value_name
            ]
            result = subprocess.run(check_cmd, capture_output=True, text=True, shell=False)
            if result.returncode == 0:
                logger.info(f"{value_name} exists, will set to 1.")
            else:
                logger.info(f"{value_name} does not exist, will create.")
            set_cmd = [
                "reg.exe", "add",
                f"HKEY_LOCAL_MACHINE\\{reg_path}",
                "/v", value_name,
                "/t", "REG_DWORD",
                "/d", "1",
                "/f"
            ]
            subprocess.run(set_cmd, check=True, shell=False)

        methods = [
            enable_with_winreg,
            enable_with_reg_exe
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully enabled long paths via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Enable Long Paths: {e}")
                continue
        logger.error("All methods failed to enable long paths.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_enable_long_paths").format(log_file_path=log_file_path)
        )
