import os
import subprocess
import webbrowser
from tkinter import messagebox

from core.app_metadata import AppMetadata


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
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Official Website {official_website_url} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{official_website_url}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Official Website {official_website_url} via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the Official Website {official_website_url}: {e}")
                continue
        logger.error(f"All methods failed to open the Official Website {official_website_url}.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_official_website").format(log_file_path=log_file_path)
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
            subprocess.run(["cmd.exe", "/C", "start", "GitHub Repository", f"{AppMetadata.APP_GITHUB_REPOSITORY_URL}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{AppMetadata.APP_GITHUB_REPOSITORY_URL}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL} via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL}: {e}")
                continue
        logger.error(f"All methods failed to open the GitHub Repository {AppMetadata.APP_GITHUB_REPOSITORY_URL}.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_github_repository").format(log_file_path=log_file_path)
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
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening License {AppMetadata.APP_LICENSE_URL} via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{AppMetadata.APP_LICENSE_URL}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the License {AppMetadata.APP_LICENSE_URL} via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the License {AppMetadata.APP_LICENSE_URL}: {e}")
                continue
        logger.error(f"All methods failed to open the License {AppMetadata.APP_LICENSE_URL}.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_license").format(log_file_path=log_file_path)
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
            subprocess.run(["cmd.exe", "/C", "start", "URL", f"{contributor_url}"], check=True,
                           shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_powershell():
            logger.info(f"Opening Contributor URL: {contributor_url} via powershell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{contributor_url}'"],
                           check=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_webbrowser,
            open_with_startfile,
            open_with_cmd,
            open_with_powershell
        ]

        for method in methods:
            try:
                method()
                logger.info(f"Successfully opened the Contributor URL: {contributor_url} via {method.__name__}.")
                return
            except Exception as e:
                logger.warning(f"{method.__name__} Failed to Open the Contributor URL: {contributor_url}, {e}")
                continue
        logger.error(f"All methods failed to open the Contributor URL: {contributor_url}.")
        messagebox.showerror(
            app_translator.translate("error"),
            app_translator.translate(f"failed_to_open_contributor_url").format(contributor_url=contributor_url, log_file_path=log_file_path)
        )
