import os
import subprocess
from pathlib import Path

from core import (
    AppResources,
    PrerequisiteChecks
)
from handlers.shared import (
    FetchResource,
    VerifyFileCertificate
)


class InstallMicrosoftEdgeWebView2Runtime:
    EXPECTED_SIGNER_SUBJECT = (
        "CN=Microsoft Corporation, O=Microsoft Corporation, "
        "L=Redmond, S=Washington, C=US"
    )
    ONLINE_INSTALLER_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
    OFFLINE_INSTALLER_ARM64_URL = "https://go.microsoft.com/fwlink/?LinkId=2099616"
    OFFLINE_INSTALLER_X64_URL = "https://go.microsoft.com/fwlink/?LinkId=2124701"

    def __init__(self, logger, app_translator, log_callback,
                 installer_type="online_install",
                 silent_install=False):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.installer_type = installer_type
        self.silent_install = silent_install

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
        self._install_webview2()

    def _install_webview2(self):
        # Install via EdgeUpdate (no download required)
        if self.installer_type == "via_edgeupdate":
            self._install_via_edgeupdate()
            return

        # Determine Download URL
        if self.installer_type == "offline_install":
            arch = PrerequisiteChecks.check_os_architecture()
            if arch == "ARM64":
                url = self.OFFLINE_INSTALLER_ARM64_URL
            else:
                url = self.OFFLINE_INSTALLER_X64_URL
        else:
            url = self.ONLINE_INSTALLER_URL

        # Determine Installer Type Label
        is_online = self.installer_type == "online_install"
        installer_label = "online" if is_online else "offline"

        filename = self._get_filename()
        download_dir = AppResources.app_temp_dir()
        file_path = Path(download_dir) / filename
        sha256_path = file_path.with_suffix(file_path.suffix + ".sha256")

        # Check If the Downloaded File Can Be Reused
        if self._try_reuse_cached(file_path, sha256_path):
            return

        # Download Installer
        if is_online:
            self._log(self.app_translator.translate("modules.installer.downloading_webview2_online_installer"))
        else:
            self._log(self.app_translator.translate("modules.installer.downloading_webview2_offline_installer"))
        self.logger.info(
            f"Downloading {installer_label} Microsoft Edge WebView2 Runtime Installer from: {url}"
        )

        try:
            downloaded_path = FetchResource.fetch(
                url=url, download_dir=download_dir, filename=filename,
                progress_callback=FetchResource.throttled_progress(self._log),
                save_sha256=True,
            )
        except Exception as e:
            self.logger.error(
                f"An Error Occurred While Downloading the {installer_label} "
                f"Microsoft Edge WebView2 Runtime Installer: {e}"
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.download_webview2_installer_failed"
                ).format(error=e)
            )
            return

        file_path = Path(downloaded_path)

        # Verify Certificate
        self._log(self.app_translator.translate("modules.common.verifying_certificate"))
        self.logger.info(
            f"Verifying Digital Certificate for Downloaded File: {downloaded_path}"
        )

        if not self._verify_certificate(file_path):
            self.logger.error(
                "Certificate verification failed for the Microsoft Edge "
                "WebView2 Runtime Installer."
            )
            self._log(
                self.app_translator.translate(
                    "modules.common.verify_certificate_failed"
                )
            )
            return

        self._launch_installer(file_path)

    def _install_via_edgeupdate(self):
        edgeupdate_path = self._find_edgeupdate_path()
        if not edgeupdate_path:
            self.logger.error(
                "MicrosoftEdgeUpdate.exe not found. Unable to install via EdgeUpdate."
            )
            self._log(
                self.app_translator.translate("modules.installer.edgeupdate_not_found")
            )
            return

        args = [
            str(edgeupdate_path),
            "/installsource", "taggedmi",
            "/install",
            "appguid={F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
            "&appname=Microsoft%20Edge%20Webview2%20Runtime"
            "&needsadmin=prefers",
        ]

        self._log(
            self.app_translator.translate(
                "modules.installer.launching_webview2_installer"
            )
        )
        self.logger.info(
            "Installing Microsoft Edge WebView2 Runtime via EdgeUpdate. "
            f"Command: {' '.join(args)}"
        )

        try:
            result = subprocess.run(
                args,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception as e:
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_error"
                ).format(error=str(e))
            )
            self.logger.error(
                f"An Error Occurred While Installing Microsoft Edge WebView2 Runtime via EdgeUpdate: {e}"
            )
            return

        if result.returncode == 0:
            self.logger.info(
                "Microsoft Edge WebView2 Runtime installed successfully via EdgeUpdate."
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_successfully"
                )
            )
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_error"
                ).format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Installing Microsoft Edge WebView2 Runtime via EdgeUpdate:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr,
                    use_localized=False, returncode=result.returncode
                )
            )

    @staticmethod
    def _find_edgeupdate_path():
        local_app_data = Path(os.getenv("LocalAppData") or Path.home() / "AppData" / "Local")
        program_files_x86 = Path(os.getenv("ProgramFiles(x86)") or r"C:\Program Files (x86)")

        candidates = [
            local_app_data / "Microsoft" / "EdgeUpdate" / "MicrosoftEdgeUpdate.exe",
            program_files_x86 / "Microsoft" / "EdgeUpdate" / "MicrosoftEdgeUpdate.exe",
        ]

        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return None

    @staticmethod
    def is_edgeupdate_available():
        return InstallMicrosoftEdgeWebView2Runtime._find_edgeupdate_path() is not None

    def _try_reuse_cached(self, file_path, sha256_path):
        if not file_path.exists() or not sha256_path.exists():
            if file_path.exists():
                file_path.unlink()
                self.logger.info("Stale cached installer removed, re-downloading...")
            else:
                self.logger.info("No cached installer found, downloading...")
            return False

        saved_sha256 = sha256_path.read_text(encoding="utf-8").strip()
        try:
            current_sha256 = FetchResource.compute_sha256(file_path)
        except Exception as e:
            self.logger.warning(
                f"Unable to Compute SHA256 for Cached File, Re-downloading: {e}"
            )
            return False

        if saved_sha256 != current_sha256:
            self.logger.warning(
                f"SHA256 mismatch for: {file_path} "
                f"(saved={saved_sha256[:16]}..., "
                f"actual={current_sha256[:16]}...), re-downloading..."
            )
            return False

        self.logger.info(
            f"SHA256 Matches, Verifying Certificate for Cached File: {file_path}"
        )
        self._log(self.app_translator.translate("modules.common.verifying_certificate"))
        if not self._verify_certificate(file_path):
            self.logger.warning(
                f"Certificate Verification Failed for Cached File: {file_path}, "
                "Re-downloading..."
            )
            return False

        self.logger.info(
            f"Certificate Verified, Reusing Cached Installer: {file_path}"
        )
        self._launch_installer(file_path)
        return True

    def _launch_installer(self, file_path):
        # Build Arguments
        args = [str(file_path), "/install"]
        if self.silent_install:
            args.append("/silent")

        install_args = " ".join(args[1:])
        self._log(
            self.app_translator.translate(
                "modules.installer.launching_webview2_installer"
            )
        )
        self.logger.info(
            f"Launching Microsoft Edge WebView2 Runtime Installer. Arguments: {install_args}"
        )

        try:
            result = subprocess.run(
                args,
                check=False,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception as e:
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_error"
                ).format(error=str(e))
            )
            self.logger.error(
                f"An Error Occurred While Installing Microsoft Edge WebView2 Runtime: {e}"
            )
            return

        if result.returncode == 0:
            self.logger.info(
                "Microsoft Edge WebView2 Runtime installed successfully."
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_successfully"
                )
            )
        else:
            error_output = self._format_error_output(
                self.app_translator, result.stdout, result.stderr, returncode=result.returncode
            )
            self._log(
                self.app_translator.translate(
                    "modules.installer.install_webview2_error"
                ).format(error=error_output)
            )
            self.logger.error(
                "An Error Occurred While Installing Microsoft Edge WebView2 Runtime:\n"
                + self._format_error_output(
                    self.app_translator, result.stdout, result.stderr,
                    use_localized=False, returncode=result.returncode
                )
            )

    def _get_filename(self):
        if self.installer_type == "online_install":
            return "MicrosoftEdgeWebview2Setup.exe"

        arch = PrerequisiteChecks.check_os_architecture()
        if arch == "ARM64":
            return "MicrosoftEdgeWebView2RuntimeInstallerARM64.exe"

        return "MicrosoftEdgeWebView2RuntimeInstallerX64.exe"

    def _verify_certificate(self, file_path):
        return VerifyFileCertificate.verify(
            file_path=str(file_path),
            signer_subject=self.EXPECTED_SIGNER_SUBJECT,
            enable_crl_check=True,
        )
