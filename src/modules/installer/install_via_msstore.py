import shutil
import subprocess
from pathlib import Path

from core import (
    AppLogger,
    AppResources
)
from handlers.shared import (
    FetchResource,
    URILauncher,
    VerifyFileCertificate
)


class InstallViaMicrosoftStore:
    PRODUCT_ID = "9PM860492SZD"
    FIXED_FILENAME = "Microsoft PC Manager Installer.exe"
    EXPECTED_SIGNER_SUBJECT = (
        "CN=Microsoft Corporation, O=Microsoft Corporation, "
        "L=Redmond, S=Washington, C=US"
    )

    def __init__(self, logger, app_translator, log_callback, open_method="open_msstore"):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.open_method = open_method
        self.log_file_path = AppLogger.get_log_file_path()

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        if self.open_method == "open_msstore":
            self._query_msstore_installation()
        elif self.open_method == "open_msstore_web":
            self._log(self.app_translator.translate("modules.installer.opening_msstore_web"))
            self._open_msstore_web()
        elif self.open_method == "download_online_installer":
            self._download_online_installer()
        else:
            self.logger.warning(f"Unknown open_method: '{self.open_method}'. Falling back to query.")
            self._query_msstore_installation()

    def _query_msstore_installation(self):
        store_app = shutil.which("store.exe") or shutil.which("microsoftstore.exe")
        if store_app:
            self._log(self.app_translator.translate("modules.installer.msstore_found"))
            self.logger.info("Microsoft Store is installed, opening the store page...")
            self._open_msstore()
        else:
            self._log(self.app_translator.translate("modules.installer.msstore_not_found"))
            self.logger.info("Microsoft Store is not installed, opening the webpage...")
            self._open_msstore_web()

    def _open_msstore(self):
        URILauncher.launch_uri(
            uri=f"ms-windows-store://pdp/?ProductId={self.PRODUCT_ID}",
            target_name="Microsoft Store",
            messagebox_error_message="modules.installer.launch_msstore_error",
            logger=self.logger,
            log_file_path=self.log_file_path,
            app_translator=self.app_translator,
        )

    def _open_msstore_web(self):
        url = f"https://apps.microsoft.com/detail/{self.PRODUCT_ID}"
        URILauncher.launch_url(
            url=url,
            target_name="Microsoft Store (Web)",
            messagebox_error_message="modules.installer.open_msstore_web_error",
            logger=self.logger,
            log_file_path=self.log_file_path,
            app_translator=self.app_translator,
            msstore_web_url=url,
        )

    def _verify_certificate(self, file_path):
        # Verify the Authenticode signature of the given file.
        # Returns True if valid, False otherwise.
        return VerifyFileCertificate.verify(
            file_path=str(file_path),
            signer_subject=self.EXPECTED_SIGNER_SUBJECT,
            enable_crl_check=True,
        )

    def _launch_installer(self, file_path):
        self.logger.info(f"Launching Installer via Subprocess: {file_path}")
        self._log(self.app_translator.translate("modules.installer.launching_downloaded_installer"))
        subprocess.Popen(
            [str(file_path)],
            shell=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    def _download_online_installer(self):
        url = f"https://get.microsoft.com/installer/download/{self.PRODUCT_ID}"
        download_dir = AppResources.app_temp_dir()
        file_path = Path(download_dir) / self.FIXED_FILENAME
        sha256_path = file_path.with_suffix(file_path.suffix + ".sha256")

        # Check If the Downloaded File Can Be Reused
        if self._try_reuse_cached(file_path, sha256_path):
            return

        # Download Installer
        self._log(self.app_translator.translate("modules.installer.downloading_online_installer"))
        self.logger.info(f"Downloading Online Installer from: {url}")
        try:
            downloaded_path = FetchResource.fetch(
                url=url, download_dir=download_dir, filename=self.FIXED_FILENAME,
                progress_callback=FetchResource.throttled_progress(self._log),
                save_sha256=True,
            )
        except Exception as e:
            self.logger.error(f"An Error Occurred While Downloading the Online Installer: {e}")
            self._log(
                self.app_translator.translate("modules.installer.download_online_installer_failed").format(error=e)
            )
            return

        # Verify Certificate
        self._log(self.app_translator.translate("modules.common.verifying_certificate"))
        self.logger.info(
            f"Verifying Digital Certificate for Downloaded File: {downloaded_path}"
        )
        if not self._verify_certificate(downloaded_path):
            self.logger.error(
                "Certificate verification failed for the Microsoft PC Manager Installer."
            )
            self._log(self.app_translator.translate("modules.common.verify_certificate_failed"))
            return

        # Launch Downloaded Installer
        self.logger.info(f"Certificate Verified, Launching Downloaded Installer: {downloaded_path}")
        self._launch_installer(downloaded_path)

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
            self.logger.warning(f"Unable to Compute SHA256 for Cached File, Re-downloading: {e}")
            return False

        if saved_sha256 != current_sha256:
            self.logger.warning(
                f"SHA256 mismatch for: {file_path} "
                f"(saved={saved_sha256[:16]}..., "
                f"actual={current_sha256[:16]}...), re-downloading..."
            )
            return False

        self.logger.info(f"SHA256 Matches, Verifying Certificate for Cached File: {file_path}")
        self._log(self.app_translator.translate("modules.common.verifying_certificate"))
        if not self._verify_certificate(file_path):
            self.logger.warning(
                f"Certificate Verification Failed for Cached File: {file_path}, "
                "Re-downloading..."
            )
            return False

        self.logger.info(f"Certificate Verified, Reusing Cached Installer: {file_path}")
        self._launch_installer(file_path)
        return True
