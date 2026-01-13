import subprocess
import winreg
from tkinter import messagebox


class OnEnableLongPathsClick:
    @staticmethod
    def enable_long_paths(logger=None, log_file_path=None, app_translator=None):
        reg_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"
        value_name = "LongPathsEnabled"

        def enable_with_winreg():
            logger.info("Enabling long paths via winreg.")
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                    winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as key:
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
            result = subprocess.run(check_cmd, check=True, shell=False, text=True, capture_output=True,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
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
            subprocess.run(set_cmd, check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            enable_with_winreg,
            enable_with_reg_exe
        ]

        last_error = None

        for method in methods:
            try:
                method()
                logger.info(f"Successfully enabled long paths via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Enable Long Paths: {e}")
                continue

        logger.error("All methods failed to enable long paths.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")

        logger.error("\n".join(error_details))

        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_enable_long_paths").format(log_file_path=log_file_path)
        )
