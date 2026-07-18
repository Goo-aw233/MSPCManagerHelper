from handlers.shared.launch_uri import URILauncher


class OpenDeveloperSettings:
    @staticmethod
    def open_developer_settings(logger=None, log_file_path=None, app_translator=None):
        URILauncher.launch_uri(
            uri="ms-settings:developers",
            target_name="Developer Settings",
            messagebox_error_message="handlers.open_developer_settings_error",
            logger=logger,
            log_file_path=log_file_path,
            app_translator=app_translator
        )
