import zipfile
from pathlib import Path

from core import (
    AppResources,
    PrerequisiteChecks
)
from handlers.shared import (
    FetchResource,
    OrganizeFilePaths,
    VerifyFileCertificate
)


class CollectMSPCMLogs:
    EXPECTED_SIGNER_SUBJECT = (
        "CN=Microsoft Corporation, O=Microsoft Corporation, "
        "L=Redmond, S=Washington, C=US"
    )
    PROCDUMP_DOWNLOAD_URL = "https://download.sysinternals.com/files/Procdump.zip"
    PROCDUMP_FILENAME = "Procdump.zip"

    def __init__(self, logger, app_translator, log_callback,
                 procdump_source="online_download",
                 local_procdump_path=""):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.procdump_source = procdump_source
        self.local_procdump_path = local_procdump_path

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
        self._collect_mspcm_logs()

    def _collect_mspcm_logs(self):
        procdump_path = self._get_procdump()
        if not procdump_path:
            return

    def _get_procdump(self):
        # Online Download
        if self.procdump_source == "online_download":
            arch = PrerequisiteChecks.check_os_architecture()
            if arch == "ARM64":
                exe_name = "procdump64a.exe"
            else:
                exe_name = "procdump64.exe"

            download_dir = AppResources.app_temp_dir()
            zip_path = Path(download_dir) / self.PROCDUMP_FILENAME
            sha256_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
            exe_path = Path(download_dir) / exe_name

            # Check if Downloaded ZIP and Extracted EXE Can Be Reused
            if self._try_reuse_cached(zip_path, sha256_path, exe_path):
                return str(exe_path)

            # Download ProcDump ZIP
            self._log(
                self.app_translator.translate("modules.maintenance.downloading_procdump")
            )
            self.logger.info(
                f"Downloading ProcDump from: {self.PROCDUMP_DOWNLOAD_URL}"
            )

            try:
                downloaded_path = FetchResource.fetch(
                    url=self.PROCDUMP_DOWNLOAD_URL,
                    download_dir=download_dir,
                    filename=self.PROCDUMP_FILENAME,
                    progress_callback=FetchResource.throttled_progress(self._log),
                    save_sha256=True,
                )
            except Exception as e:
                self.logger.error(
                    f"An Error Occurred While Downloading ProcDump: {e}"
                )
                self._log(
                    self.app_translator.translate(
                        "modules.maintenance.downloading_procdump_error"
                    ).format(error=e)
                )
                return None

            zip_path = Path(downloaded_path)

            # Extract ZIP
            self._log(
                self.app_translator.translate(
                    "modules.maintenance.extracting_procdump"
                ).format(exe_name=exe_name)
            )
            self.logger.info(
                f"Extracting {exe_name} from: {zip_path}"
            )

            try:
                with zipfile.ZipFile(str(zip_path), "r") as zf:
                    zf.extract(exe_name, download_dir)
            except Exception as e:
                self.logger.error(
                    f"An Error Occurred While Extracting ProcDump: {e}"
                )
                self._log(
                    self.app_translator.translate(
                        "modules.maintenance.extracting_procdump_error"
                    ).format(error=e)
                )
                return None

            # Verify Certificate of ProcDump EXE
            self._log(
                self.app_translator.translate("modules.common.verifying_certificate")
            )
            self.logger.info(
                f"Verifying Digital Certificate for: {exe_path}"
            )

            if not self._verify_certificate(exe_path):
                self.logger.error(
                    "Certificate verification failed for ProcDump EXE."
                )
                self._log(
                    self.app_translator.translate(
                        "modules.common.verify_certificate_failed"
                    )
                )
                return None

            self.logger.info(
                f"ProcDump EXE Verified Successfully: {exe_path}"
            )
            return str(exe_path)

        # Local File
        elif self.procdump_source == "local_file":
            if not self.local_procdump_path or not Path(self.local_procdump_path).exists():
                self.logger.error(
                    f"Local ProcDump EXE Not Found: {self.local_procdump_path}"
                )
                self._log(
                    self.app_translator.translate(
                        "modules.maintenance.local_file_not_found"
                    )
                )
                return None

            file_path = Path(self.local_procdump_path)

            self._log(
                self.app_translator.translate("modules.common.verifying_certificate")
            )
            self.logger.info(
                f"Verifying Digital Certificate for: {file_path}"
            )

            if not self._verify_certificate(file_path):
                self.logger.error(
                    "Certificate verification failed for the local ProcDump EXE."
                )
                self._log(
                    self.app_translator.translate(
                        "modules.common.verify_certificate_failed"
                    )
                )
                return None

            self.logger.info(
                f"Local ProcDump EXE Verified Successfully: {file_path}"
            )
            return str(file_path)

        return None

    def _try_reuse_cached(self, zip_path, sha256_path, exe_path):
        if not exe_path.exists():
            self.logger.info("No cached ProcDump EXE found, downloading...")
            return False

        if not zip_path.exists() or not sha256_path.exists():
            if zip_path.exists():
                zip_path.unlink()
                self.logger.info("Stale cached ZIP removed, re-downloading...")
            else:
                self.logger.info("No cached ZIP found, re-downloading...")
            return False

        saved_sha256 = sha256_path.read_text(encoding="utf-8").strip()
        try:
            current_sha256 = FetchResource.compute_sha256(zip_path)
        except Exception as e:
            self.logger.warning(
                f"Unable to Compute SHA256 for Cached ZIP, Re-downloading: {e}"
            )
            return False

        if saved_sha256 != current_sha256:
            self.logger.warning(
                f"SHA256 mismatch for: {zip_path} "
                f"(saved={saved_sha256[:16]}..., "
                f"actual={current_sha256[:16]}...), re-downloading..."
            )
            return False

        self.logger.info(
            f"SHA256 Matches, Verifying Certificate for Cached EXE: {exe_path}"
        )
        self._log(self.app_translator.translate("modules.common.verifying_certificate"))
        if not self._verify_certificate(exe_path):
            self.logger.warning(
                f"Certificate Verification Failed for Cached EXE: {exe_path}, "
                "Re-downloading..."
            )
            return False

        self.logger.info(
            f"Cached ProcDump EXE Verified, Reusing: {exe_path}"
        )
        return True

    def _verify_certificate(self, file_path):
        return VerifyFileCertificate.verify(
            file_path=str(file_path),
            signer_subject=self.EXPECTED_SIGNER_SUBJECT,
            enable_crl_check=True,
        )
