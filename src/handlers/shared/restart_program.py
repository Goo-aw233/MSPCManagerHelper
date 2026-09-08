import ctypes
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox


class RestartProgram:
    @staticmethod
    def restart_program(AdvancedStartup=None, logger=None, app_translator=None, log_file_path=None, verb=None, launch_args=None):
        """Restart the application by launching a new instance of the current executable.

        Args:
            AdvancedStartup: The AdvancedStartup class, passed in to avoid a hard import dependency.
            logger: Logger for status messages.
            app_translator: Translator used for error dialogs.
            log_file_path: Path to the log file, shown in error messages.
            verb: ShellExecuteW verb to use - "runas" to restart elevated (UAC prompt),
                or None for a normal restart.
            launch_args: Optional list of command-line arguments to pass to the new
                instance. If None, the current runtime arguments are forwarded.
        """
        boot_file_path = str(Path(sys.argv[0]).resolve())
        executable_path = str(Path(sys.executable).resolve())

        if launch_args is None:
            launch_args = AdvancedStartup.get_runtime_arguments()

        if Path(boot_file_path) == Path(executable_path):
            # Compiled executable (EXE): argv[0] is already the executable
            # itself, so the OS launches it directly. Passing only the real
            # arguments keeps argv[1:] clean; re-passing the exe path would
            # duplicate it into argv[1:] and accumulate on every restart.
            args_list = list(launch_args)
        else:
            # Running from source (.py): sys.executable is the interpreter,
            # which needs argv[0] (the script path) in the command line to
            # know which script to run.
            args_list = [boot_file_path] + list(launch_args)

        # Build the command line with the same quoting rules as the 
        # Microsoft C Runtime, so arguments containing spaces, quotes, or special
        # characters survive the round-trip.
        args_str = subprocess.list2cmdline(args_list)

        is_elevated = verb == "runas"
        restart_label = "as administrator" if is_elevated else "without elevation"
        logger.info(f"Attempting to restart {restart_label}... Executable: {boot_file_path}; Args: {args_str}")

        # Show the correct error hint depending on how we restarted.
        error_key = (
            "handlers.restart_as_administrator_error"
            if is_elevated
            else "handlers.restart_program_error"
        )

        try:
            return_code = AdvancedStartup.execute_restart(args_str, verb=verb)
            # ShellExecuteW returns > 32 on success. If it returns <= 32, it's an error code.
            # 1223 = ERROR_CANCELLED (User canceled the UAC prompt).
            if not return_code or return_code <= 32:
                failed_msg = (
                    ctypes.FormatError(return_code).strip()
                    if return_code
                    else "Unknown Error: Empty Return Code from ShellExecuteW"
                )
                logger.error(f"Failed to restart {restart_label}. [ShellExecuteW Returned {return_code}: {failed_msg}]")
                RestartProgram._show_error(app_translator, error_key, log_file_path)
            else:
                logger.info(f"Restart request succeeded {restart_label}.")
                # A successful restart launches a new instance that takes over,
                # so this process must exit. SystemExit is a BaseException, so
                # it bypasses the except Exception handler below and propagates
                # to the caller, terminating the current process.
                sys.exit(0)
        except Exception as e:
            logger.error(f"An Error Occurred While Attempting to Restart {restart_label}: {e}")
            RestartProgram._show_error(app_translator, error_key, log_file_path)
            return False

        return False

    @staticmethod
    def _show_error(app_translator, error_key, log_file_path):
        messagebox.showerror(
            app_translator.translate("common.error"),
            app_translator.translate(error_key).format(log_file_path=log_file_path)
        )
