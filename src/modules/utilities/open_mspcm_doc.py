from core import (
    AppMetadata,
    AppSettings,
    AppTranslator
)
from handlers.shared.launch_uri import URILauncher


class OpenMSPCMDoc:
    @staticmethod
    def open_mspcm_doc(logger=None, log_file_path=None, app_translator=None):
        # Use detected system language if no translator is provided.
        locale = app_translator.locale if app_translator else AppTranslator.detect_system_language()
        logger.info(f"Detected System Locale: {locale}")
        mspcm_doc_url = (
            # Original URLs
            (
                AppMetadata.MSPCM_ZHCN_DOC_URL
                if locale == "zh-cn"
                else AppMetadata.MSPCM_DOC_URL
            )
            if AppSettings.is_original_links_enabled()
            # Redirected URLs
            else (
                AppMetadata.MSPCM_ZHCN_DOC_DIR_URL
                if locale == "zh-cn"
                else AppMetadata.MSPCM_DOC_DIR_URL
            )
        )

        URILauncher.launch_url(
            url=mspcm_doc_url,
            target_name="Microsoft PC Manager Help Documentation",
            messagebox_error_message="handlers.open_mspcm_doc_error",
            logger=logger,
            log_file_path=log_file_path,
            app_translator=app_translator,
            mspcm_doc_url=mspcm_doc_url
        )
