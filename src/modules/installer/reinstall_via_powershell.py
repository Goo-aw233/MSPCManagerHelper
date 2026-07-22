import subprocess


class ReinstallViaPowerShell:

    def __init__(self, logger, app_translator, log_callback, action, user_scope, force_quit=False):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.action = action
        self.user_scope = user_scope
        self.force_quit = force_quit

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    @staticmethod
    def _format_error_output(app_translator, stdout_text, stderr_text, use_localized=True, returncode=None):
        stdout_label = app_translator.translate(
            "common.stdout") if use_localized else "Stdout"
        stderr_label = app_translator.translate(
            "common.stderr") if use_localized else "Stderr"
        return_code_label = app_translator.translate(
            "common.return_code") if use_localized else "Return Code"
        parts = []
        if returncode is not None:
            parts.append(f"{return_code_label}: {returncode}")
        if stdout_text:
            parts.append(f"{stdout_label}:\n{stdout_text}")
        if stderr_text:
            if parts:
                parts.append("---")
            parts.append(f"{stderr_label}:\n{stderr_text}")
        return "\n".join(parts)

    def execute(self):
        if self.action == "reset":
            self._reset_via_powershell()
        else:
            self._reinstall_via_powershell(self.user_scope)

    def _reinstall_via_powershell(self, user_scope):
        force_quit_arg = " -ForceApplicationShutdown" if self.force_quit else ""

        if user_scope == "all_users":
            powershell_command = (
                r"Get-AppxPackage -AllUsers | "
                r"Where-Object { $_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$' } | "
                r"ForEach-Object { Add-AppxPackage -DisableDevelopmentMode -Register"
                + force_quit_arg
                + r' "$($_.InstallLocation)\AppxManifest.xml" }'
            )
        else:
            powershell_command = (
                r"Get-AppxPackage | "
                r"Where-Object { $_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$' } | "
                r"ForEach-Object { Add-AppxPackage -DisableDevelopmentMode -Register"
                + force_quit_arg
                + r' "$($_.InstallLocation)\AppxManifest.xml" }'
            )

        command = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            powershell_command
        ]

        scope_label = (self.app_translator.translate("pages.installer.all_users")
                       if user_scope == "all_users"
                       else self.app_translator.translate("pages.installer.current_user"))

        self._log(
            self.app_translator.translate("modules.installer.reinstalling_via_windows_powershell")
        )
        self.logger.info(f"Reinstalling via Windows PowerShell ({scope_label})")
        if self.force_quit:
            self._log(self.app_translator.translate("pages.installer.force_quit"))
            self.logger.info(f"Force Quit: {self.force_quit}")
        self.logger.info(f"Windows PowerShell Command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(
                self.app_translator.translate(
                    "modules.installer.reinstall_via_windows_powershell_error"
                ).format(error=str(e))
            )
            self.logger.error(
                f"An Error Occurred While Reinstalling via Windows PowerShell: {e}"
            )
            return

        if result.returncode == 0 and not result.stderr.strip():
            self._log(
                self.app_translator.translate(
                    "modules.installer.reinstall_via_windows_powershell_successfully"
                )
            )
            self.logger.info("Reinstalled via Windows PowerShell successfully.")
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.reinstall_via_windows_powershell_error"
                ).format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Reinstalling via Windows PowerShell:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr, use_localized=False, returncode=result.returncode
                )
            )

    def _reset_via_powershell(self):
        powershell_command = (
            r"Get-AppxPackage | "
            r"Where-Object { $_.Name -match '^Microsoft\.(MicrosoftPCManager|PCManager)$' } | "
            r"Reset-AppxPackage"
        )

        command = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            powershell_command
        ]

        self._log(
            self.app_translator.translate("modules.installer.resetting_via_windows_powershell")
        )
        self.logger.info("Resetting via Windows PowerShell")
        self.logger.info(f"Windows PowerShell Command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(
                self.app_translator.translate(
                    "modules.installer.reset_via_windows_powershell_error"
                ).format(error=str(e))
            )
            self.logger.error(
                f"An Error Occurred While Resetting via Windows PowerShell: {e}"
            )
            return

        if result.returncode == 0 and not result.stderr.strip():
            self._log(
                self.app_translator.translate(
                    "modules.installer.reset_via_windows_powershell_successfully"
                )
            )
            self.logger.info("Reset via Windows PowerShell successfully.")
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.reset_via_windows_powershell_error"
                ).format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Resetting via Windows PowerShell:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr, use_localized=False, returncode=result.returncode
                )
            )
