import subprocess

from handlers.shared.organize_file_paths import OrganizeFilePaths


class InstallViaPowerShellForCurrentUser:

    def __init__(self, logger, app_translator, log_callback, force_quit=False,
                 app_package_path="", dependencies_paths=""):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.force_quit = force_quit
        self.app_package_path = app_package_path
        self.dependencies_paths = dependencies_paths

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

    @staticmethod
    def _get_clean_path(paths):
        cleaned_paths = OrganizeFilePaths.clean_paths(paths)
        if cleaned_paths:
            return cleaned_paths[0]
        paths_text = str(paths).strip()
        return paths_text

    def execute(self):
        self._install_via_powershell()

    def _install_via_powershell(self):
        # Application Package Path
        app_package_path = self._get_clean_path(self.app_package_path)
        if not app_package_path:
            self.logger.error("Application package path is empty. "
                              "Unable to install via Windows PowerShell.")
            self._log(
                self.app_translator.translate("modules.installer.empty_app_package_path")
            )
            return

        # Build Windows PowerShell Command
        powershell_command = f"Add-AppxPackage -Path '{app_package_path}'"

        # Dependencies
        dependencies_paths = OrganizeFilePaths.clean_paths(self.dependencies_paths)
        if dependencies_paths:
            dependency_args = ",".join(f"'{p}'" for p in dependencies_paths)
            powershell_command += f" -DependencyPath {dependency_args}"

        # Force Quit
        if self.force_quit:
            powershell_command += " -ForceApplicationShutdown"

        # Build Full Command
        command = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            powershell_command
        ]

        # Show Cleaned Paths
        cleaned_paths_lines = [
            self.app_translator.translate("modules.installer.cleaned_app_package_path").format(
                path=app_package_path
            )
        ]
        if dependencies_paths:
            cleaned_paths_lines.append(
                self.app_translator.translate("modules.installer.cleaned_dependencies_paths_header")
            )
            for dependency_path in dependencies_paths:
                cleaned_paths_lines.append(f"  - {dependency_path}")
        if self.force_quit:
            cleaned_paths_lines.append(
                self.app_translator.translate("pages.installer.force_quit")
            )
        self._log("\n".join(cleaned_paths_lines))

        self._log(
            self.app_translator.translate("modules.installer.installing_via_windows_powershell")
        )
        self.logger.info("Installing via Windows PowerShell for Current User")
        self.logger.info(
            "Raw Windows PowerShell Inputs:\n"
            f"Force Quit: {self.force_quit}\n"
            f"Application Package Path: {self.app_package_path}\n"
            f"Dependencies Paths: {self.dependencies_paths}"
        )
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
                    "modules.installer.install_via_windows_powershell_error"
                ).format(error=str(e))
            )
            self.logger.error(
                f"An Error Occurred While Installing via Windows PowerShell: {e}"
            )
            return

        if result.returncode == 0 and not result.stderr.strip():
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_via_windows_powershell_successfully"
                )
            )
            self.logger.info(
                "Installed via Windows PowerShell for Current User successfully."
            )
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_via_windows_powershell_error"
                ).format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Installing via Windows PowerShell:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr, use_localized=False, returncode=result.returncode
                )
            )
