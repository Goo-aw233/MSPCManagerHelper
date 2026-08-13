import subprocess

from core import WindowsUtilities
from handlers.shared.organize_file_paths import OrganizeFilePaths


class InstallViaDISM:
    def __init__(self, logger, app_translator, log_callback, image_type="online_image",
                 offline_image_path="", app_package_path="", license_path="", dependencies_paths=""):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.image_type = image_type
        self.offline_image_path = offline_image_path
        self.app_package_path = app_package_path
        self.license_path = license_path
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
        self._install_via_dism()

    def _install_via_dism(self):
        # Determine Image Type
        if self.image_type == "offline_image":
            image_status = f"/Image:{self._get_clean_path(self.offline_image_path)}"
        else:
            image_status = "/Online"

        # Application Package Path
        app_package_path = self._get_clean_path(self.app_package_path)
        if not app_package_path:
            self.logger.error("Application package path is empty. Unable to install via DISM.")
            self._log(
                self.app_translator.translate("modules.installer.empty_app_package_path")
            )
            return

        # Build Command
        command = [
            str(WindowsUtilities.dism()),
            image_status,
            "/Add-ProvisionedAppxPackage",
            f"/PackagePath:{app_package_path}"
        ]

        # License
        license_path = self._get_clean_path(self.license_path)
        if license_path:
            command.append(f"/LicensePath:{license_path}")
        else:
            command.append("/SkipLicense")

        # Dependencies
        dependencies_paths = OrganizeFilePaths.clean_paths(self.dependencies_paths)
        for dependency_path in dependencies_paths:
            command.append(f"/DependencyPackagePath:{dependency_path}")

        # Show Cleaned Paths
        cleaned_paths_lines = []
        if self.image_type == "offline_image":
            cleaned_offline_image_path = self._get_clean_path(self.offline_image_path)
            cleaned_paths_lines.append(
                self.app_translator.translate("modules.installer.cleaned_offline_image_path").format(
                    path=cleaned_offline_image_path
                )
            )
        cleaned_paths_lines.append(
            self.app_translator.translate("modules.installer.cleaned_app_package_path").format(
                path=app_package_path
            )
        )
        if license_path:
            cleaned_paths_lines.append(
                self.app_translator.translate("modules.installer.cleaned_license_path").format(
                    path=license_path
                )
            )
        if dependencies_paths:
            cleaned_paths_lines.append(
                self.app_translator.translate("modules.installer.cleaned_dependencies_paths_header")
            )
            for dependency_path in dependencies_paths:
                cleaned_paths_lines.append(f"  - {dependency_path}")
        self._log("\n".join(cleaned_paths_lines))

        self._log(
            self.app_translator.translate("modules.installer.installing_via_dism")
        )
        self.logger.info(f"Installing Provisioned Package via DISM ({image_status})")
        self.logger.info(
            "Raw DISM Inputs:\n"
            f"Image Type: {self.image_type}\n"
            f"Offline Image Path: {self.offline_image_path}\n"
            f"Application Package Path: {self.app_package_path}\n"
            f"License Path: {self.license_path}\n"
            f"Dependencies Paths: {self.dependencies_paths}"
        )
        self.logger.info(f"DISM Command: {' '.join(command)}")

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
                self.app_translator.translate("modules.installer.install_via_dism_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Installing via DISM: {e}")
            return

        if result.returncode == 0 and not result.stderr.strip():
            self._log(
                self.app_translator.translate("modules.installer.install_via_dism_successfully")
            )
            self.logger.info("Installed Provisioned Package via DISM successfully.")
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate("modules.installer.install_via_dism_error").format(
                    error=error_output
                )
            )
            self.logger.error(
                "An Error Occurred While Installing via DISM:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr, use_localized=False, returncode=result.returncode
                )
            )
