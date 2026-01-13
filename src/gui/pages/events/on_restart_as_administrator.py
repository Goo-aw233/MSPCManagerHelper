import ctypes
import sys
from pathlib import Path
from tkinter import messagebox


class OnRestartAsAdministrator:

    @staticmethod
    def on_restart_as_administrator(AdvancedStartup=None, logger=None, app_translator=None, log_file_path=None):
        boot_file_path = str(Path(sys.argv[0]).resolve())

        original_args = AdvancedStartup.get_runtime_arguments()
        formatted_original_args = [
            f'"{arg}"' if " " in arg else arg for arg in original_args
        ]

        args_list = [f'"{boot_file_path}"'] + formatted_original_args
        args_str = " ".join(args_list)
        logger.info(f"Attempting to restart as administrator... Executable: {boot_file_path}; Args: {args_str}")

        try:
            result = AdvancedStartup.run_as_administrator(args_str)
            # ShellExecuteW returns > 32 on success. If result <= 32, it's an error code.
            # 1223 = ERROR_CANCELLED (User canceled the UAC prompt).
            if not result or result <= 32:
                failed_code = ctypes.get_last_error()
                failed_msg = ctypes.FormatError(failed_code).strip()

                msg = f"Failed to request elevation (ShellExecute returned {result}). [WinError {failed_code}: {failed_msg}]"

                logger.error(msg)
                
                messagebox.showerror(
                    app_translator.translate("error"),
                    app_translator.translate("failed_to_run_as_administrator").format(log_file_path=log_file_path)
                )
            else:
                logger.info("Elevation request succeeded (process elevated or ShellExecute triggered).")
        except Exception as e:
            logger.exception("Exception while attempting to restart as administrator.")
            # Try to get more info from WinError if possible.
            failed_code = ctypes.get_last_error()
            failed_msg = ctypes.FormatError(failed_code).strip()
            logger.error(f"Exception details: {e} [WinError {failed_code}: {failed_msg}]")

            messagebox.showerror(
                app_translator.translate("error"),
                app_translator.translate("failed_to_run_as_administrator").format(log_file_path=log_file_path)
            )
