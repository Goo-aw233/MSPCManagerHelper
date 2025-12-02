import ctypes
import sys
from pathlib import Path
from tkinter import messagebox


def on_restart_as_administrator(AdvancedStartup, logger, translator):
    if AdvancedStartup.is_administrator():
        logger.info("Already running as administrator, no action taken.")
        return

    # Determine the original launch path (exe/script).
    boot_file_path = str(Path(sys.argv[0]).resolve())
    logger.debug(f"Determined Boot File Path: {boot_file_path}")

    original_args = AdvancedStartup.get_runtime_arguments()
    params_list = [f'"{boot_file_path}"'] + [f'"{arg}"' if " " in arg else arg for arg in original_args]

    formatted_original_args = [
        f'"{arg}"' if " " in arg else arg for arg in original_args
    ]

    params_list = [f'"{boot_file_path}"'] + formatted_original_args
    params_str = " ".join(params_list)
    logger.info(f"Attempting to restart as administrator. Executable: {boot_file_path}; Params: {params_str}")
    try:
        result = AdvancedStartup.run_as_administrator(params_str)
        if not result:
            failed_code = ctypes.get_last_error()
            failed_msg = ctypes.FormatError(failed_code).strip()
            logger.error(
                f"Failed to request elevation (ShellExecute returned failure). "
                f"ErrorCode={failed_code}; Message={failed_msg}"
            )
            messagebox.showerror(
                translator.translate("error"),
                f"{translator.translate('failed_to_run_as_administrator')}\n"
                f"{translator.translate('error_code')}: {failed_code}\n"
                f"{translator.translate('error_message')}: {failed_msg}"
            )
        else:
            logger.info("Elevation request succeeded (process elevated or ShellExecute triggered).")
    except Exception as e:
        logger.exception("Exception while attempting to restart as administrator.")
        failed_code = ctypes.get_last_error()
        failed_msg = ctypes.FormatError(failed_code).strip()
        messagebox.showerror(
            translator.translate("error"),
            f"{translator.translate('failed_to_run_as_administrator')}\n"
            f"{translator.translate('error_code')}: {failed_code}\n"
            f"{translator.translate('error_message')}: {failed_msg}"
        )
