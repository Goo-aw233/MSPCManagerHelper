import os
import subprocess
import webbrowser
from tkinter import messagebox

from core.app_metadata import AppMetadata
from core.app_settings import AppSettings


class OnOpenURLButtonClick:
    @staticmethod
    def open_official_website(logger=None, log_file_path=None, app_translator=None):
        official_website_url = "https://pcmanager.microsoft.com"

        def open_with_webbrowser():
            logger.info(f"Opening Official Website {official_website_url} via webbrowser.")
            webbrowser.open(official_website_url)

        def open_with_startfile():
            logger.info(f"Opening Official Website {official_website_url} via os.startfile.")
            os.startfile(official_website_url)
        def open_with_cmd():
            logger.info(f"Opening Official Website {official_website_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Official Website", f"{official_website_url}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Official Website {official_website_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{official_website_url}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Official Website {official_website_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the Official Website {official_website_url}: {e}")
                continue
        logger.error(f"All methods failed to open the Official Website {official_website_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_official_website").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_github_repository(logger=None, log_file_path=None, app_translator=None):

        def open_with_webbrowser():
            logger.info(f"Opening GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via webbrowser.")
            webbrowser.open(AppMetadata.APP_GITHUB_REPOSITORY_URL)

        def open_with_startfile():
            logger.info(f"Opening GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via os.startfile.")
            os.startfile(AppMetadata.APP_GITHUB_REPOSITORY_URL)
        def open_with_cmd():
            logger.info(f"Opening GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "GitHub Repository", f"{AppMetadata.APP_GITHUB_REPOSITORY_URL}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{AppMetadata.APP_GITHUB_REPOSITORY_URL}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL}: {e}")
                continue
        logger.error(f"All methods failed to open the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_github_repository").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_license(logger=None, log_file_path=None, app_translator=None):

        def open_with_webbrowser():
            logger.info(f"Opening License {AppMetadata.APP_LICENSE_URL} via webbrowser.")
            webbrowser.open(AppMetadata.APP_LICENSE_URL)

        def open_with_startfile():
            logger.info(f"Opening License {AppMetadata.APP_LICENSE_URL} via os.startfile.")
            os.startfile(AppMetadata.APP_LICENSE_URL)
        def open_with_cmd():
            logger.info(f"Opening License {AppMetadata.APP_LICENSE_URL} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "License", f"{AppMetadata.APP_LICENSE_URL}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening License {AppMetadata.APP_LICENSE_URL} via Windows PowerShell.")
            subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{AppMetadata.APP_LICENSE_URL}'"],
                check=True, shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the License {AppMetadata.APP_LICENSE_URL} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the License {AppMetadata.APP_LICENSE_URL}: {e}")
                continue
        logger.error(f"All methods failed to open the License {AppMetadata.APP_LICENSE_URL}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_license").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_contributors_url(logger=None, log_file_path=None, app_translator=None, contributor_url=None):

        def open_with_webbrowser():
            logger.info(f"Opening Contributor URL: {contributor_url} via webbrowser.")
            webbrowser.open(contributor_url)

        def open_with_startfile():
            logger.info(f"Opening Contributor URL: {contributor_url} via os.startfile.")
            os.startfile(contributor_url)

        def open_with_cmd():
            logger.info(f"Opening Contributor URL: {contributor_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "URL", f"{contributor_url}"], check=True, shell=False, text=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Contributor URL: {contributor_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{contributor_url}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Contributor URL: {contributor_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"{method.__name__} Failed to Open the Contributor URL: {contributor_url}, {e}")
                continue
        logger.error(f"All methods failed to open the Contributor URL: {contributor_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_contributor_url").format(contributor_url=contributor_url,
                                                                              log_file_path=log_file_path)
        )

    @staticmethod
    def open_github_releases_page(logger=None, log_file_path=None, app_translator=None):
        github_releases_url = AppMetadata.APP_GITHUB_REPOSITORY_URL + "/releases"

        def open_with_webbrowser():
            logger.info(f"Opening GitHub Releases Page {github_releases_url} via webbrowser.")
            webbrowser.open(github_releases_url)

        def open_with_startfile():
            logger.info(f"Opening GitHub Releases Page {github_releases_url} via os.startfile.")
            os.startfile(github_releases_url)

        def open_with_cmd():
            logger.info(f"Opening GitHub Releases Page {github_releases_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "GitHub Releases Page", f"{github_releases_url}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening GitHub Releases Page {github_releases_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{github_releases_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the GitHub Releases Page {github_releases_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the GitHub Releases Page {github_releases_url}: {e}")
                continue

        logger.error(f"All methods failed to open the GitHub Releases Page {github_releases_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_github_releases_page").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_1drv_page(logger=None, log_file_path=None, app_translator=None):
        onedrive_url = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA"

        def open_with_webbrowser():
            logger.info(f"Opening OneDrive Page {onedrive_url} via webbrowser.")
            webbrowser.open(onedrive_url)

        def open_with_startfile():
            logger.info(f"Opening OneDrive Page {onedrive_url} via os.startfile.")
            os.startfile(onedrive_url)

        def open_with_cmd():
            logger.info(f"Opening OneDrive Page {onedrive_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "OneDrive Page", f"{onedrive_url}"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening OneDrive Page {onedrive_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{onedrive_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the OneDrive Page {onedrive_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the OneDrive Page {onedrive_url}: {e}")
                continue

        logger.error(f"All methods failed to open the OneDrive Page {onedrive_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_onedrive_page").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_mspcm_app_package_azure_blob_page(logger=None, log_file_path=None, app_translator=None):
        azure_blob_url = "https://kaoz.uk/PCManagerOFL"

        def open_with_webbrowser():
            logger.info(f"Opening Microsoft PC Manager App Package Azure Blob Page {azure_blob_url} via webbrowser.")
            webbrowser.open(azure_blob_url)

        def open_with_startfile():
            logger.info(f"Opening Microsoft PC Manager App Package Azure Blob Page {azure_blob_url} via os.startfile.")
            os.startfile(azure_blob_url)

        def open_with_cmd():
            logger.info(f"Opening Microsoft PC Manager App Package Azure Blob Page {azure_blob_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Microsoft PC Manager App Package Azure Blob Page",
                            f"{azure_blob_url}"], check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Microsoft PC Manager App Package Azure Blob Page {azure_blob_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{azure_blob_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the Microsoft PC Manager App Package Azure Blob Page {azure_blob_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the Microsoft PC Manager App Package Azure Blob Page {azure_blob_url}: {e}")
                continue

        logger.error(f"All methods failed to open the Microsoft PC Manager App Package Azure Blob Page {azure_blob_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_mspcm_app_package_azure_blob_page").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_mspcm_app_package_1drv_page(logger=None, log_file_path=None, app_translator=None):
        onedrive_url = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EoscJOQ9taJFtx9LZLPiBM0BEmVm7wsLuJOuHnwmo9EQ5w"

        def open_with_webbrowser():
            logger.info(f"Opening Microsoft PC Manager App Package OneDrive Page {onedrive_url} via webbrowser.")
            webbrowser.open(onedrive_url)

        def open_with_startfile():
            logger.info(f"Opening Microsoft PC Manager App Package OneDrive Page {onedrive_url} via os.startfile.")
            os.startfile(onedrive_url)

        def open_with_cmd():
            logger.info(f"Opening Microsoft PC Manager App Package OneDrive Page {onedrive_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Microsoft PC Manager App Package OneDrive Page",
                            f"{onedrive_url}"], check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Microsoft PC Manager App Package OneDrive Page {onedrive_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{onedrive_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the Microsoft PC Manager App Package OneDrive Page {onedrive_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the Microsoft PC Manager App Package OneDrive Page {onedrive_url}: {e}")
                continue

        logger.error(f"All methods failed to open the Microsoft PC Manager App Package OneDrive Page {onedrive_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_mspcm_app_package_onedrive_page").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_wv2_rt_download_page(logger=None, log_file_path=None, app_translator=None):
        wv2_rt_download_url = "https://developer.microsoft.com/microsoft-edge/webview2" + AppSettings.get_support_developer_tracking_id()

        def open_with_webbrowser():
            logger.info(f"Opening WebView2 Runtime Download Page {wv2_rt_download_url} via webbrowser.")
            webbrowser.open(wv2_rt_download_url)

        def open_with_startfile():
            logger.info(f"Opening WebView2 Runtime Download Page {wv2_rt_download_url} via os.startfile.")
            os.startfile(wv2_rt_download_url)

        def open_with_cmd():
            logger.info(f"Opening WebView2 Runtime Download Page {wv2_rt_download_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "WebView2 Runtime Download Page",
                            f"{wv2_rt_download_url}"], check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening WebView2 Runtime Download Page {wv2_rt_download_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{wv2_rt_download_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the WebView2 Runtime Download Page {wv2_rt_download_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the WebView2 Runtime Download Page {wv2_rt_download_url}: {e}")
                continue

        logger.error(f"All methods failed to open the WebView2 Runtime Download Page {wv2_rt_download_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_wv2_rt_download_page").format(log_file_path=log_file_path)
        )

    @staticmethod
    def open_war_rt_download_page(logger=None, log_file_path=None, app_translator=None):
        war_rt_download_url = "https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads-archive" + AppSettings.get_support_developer_tracking_id()

        def open_with_webbrowser():
            logger.info(f"Opening Windows App Runtime Download Page {war_rt_download_url} via webbrowser.")
            webbrowser.open(war_rt_download_url)

        def open_with_startfile():
            logger.info(f"Opening Windows App Runtime Download Page {war_rt_download_url} via os.startfile.")
            os.startfile(war_rt_download_url)

        def open_with_cmd():
            logger.info(f"Opening Windows App Runtime Download Page {war_rt_download_url} via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Windows App Runtime Download Page",
                            f"{war_rt_download_url}"], check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Windows App Runtime Download Page {war_rt_download_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command",
                            f"Start-Process '{war_rt_download_url}'"], check=True, shell=False,
                           text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                logger.info(
                    f"Successfully opened the Windows App Runtime Download Page {war_rt_download_url} via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                logger.warning(
                    f"{method.__name__} Failed to Open the Windows App Runtime Download Page {war_rt_download_url}: {e}")
                continue

        logger.error(f"All methods failed to open the Windows App Runtime Download Page {war_rt_download_url}.")
        error_details = [f"Exception: {last_error}"]
        if hasattr(last_error, "stdout") and last_error.stdout:
            error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
        if hasattr(last_error, "stderr") and last_error.stderr:
            error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
        logger.error("\n".join(error_details))
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate("failed_to_open_war_rt_download_page").format(log_file_path=log_file_path)
        )
