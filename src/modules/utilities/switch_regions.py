import os
import subprocess
import winreg

import customtkinter
import iso3166
from customtkinter import CTkInputDialog

from core import (
    AppResources,
    AppSettings
)


class SwitchRegions:
    def __init__(self, logger, app_translator, log_callback, selected_mspcm_version, font_family):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_mspcm_version = selected_mspcm_version
        self.font_family = font_family
        self.nsudo_path = AppResources.nsudo_path()

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        self.logger.debug(f"Selected Microsoft PC Manager Version: {self.selected_mspcm_version}")
        use_ownership = AppSettings.is_take_ownership_enabled()
        if use_ownership:
            self.logger.debug(f"NSudo Path: {self.nsudo_path}")
        if self.selected_mspcm_version == "at_least_v3_14_0_0":
            self._at_least_v3_14_0_0()
        elif self.selected_mspcm_version == "lower_than_v3_14_0_0":
            if use_ownership:
                self._lower_than_v3_14_0_0_with_ownership()
            else:
                self._lower_than_v3_14_0_0()

    def _at_least_v3_14_0_0(self):
        region_settings_uri = "ms-settings:regionformatting"

        def open_with_startfile():
            self.logger.info("Opening Language & Region settings via os.startfile.")
            os.startfile(region_settings_uri)

        def open_with_cmd():
            self.logger.info("Opening Language & Region settings via CMD.")
            subprocess.run(["cmd.exe", "/C", "start", "Region Settings", f"{region_settings_uri}"], check=True,
                           shell=False, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        def open_with_windows_powershell():
            self.logger.info("Opening Language & Region settings via Windows PowerShell.")
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", f"Start-Process '{region_settings_uri}'"],
                           check=True, shell=False, text=True, capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)

        methods = [
            open_with_startfile,
            open_with_cmd,
            open_with_windows_powershell
        ]

        last_error = None
        for method in methods:
            try:
                method()
                self._log(self.app_translator.translate("modules.utilities.open_region_settings_successfully"))
                self.logger.info(f"Successfully opened the Language & Region settings via {method.__name__}.")
                return
            except Exception as e:
                last_error = e
                self.logger.warning(f"{method.__name__} Failed to Open the Language & Region settings: {e}")
                continue

        self._log(
            self.app_translator.translate("modules.utilities.open_region_settings_error").format(
                error=str(last_error)
                )
            )
        self.logger.error("All methods failed to open the Language & Region settings.") 

        if last_error:
            error_details = [f"Exception: {last_error}"]
            if hasattr(last_error, "stdout") and last_error.stdout:
                error_details.append(f"{'=' * 20} Stdout {'=' * 20}\n{last_error.stdout.strip()}")
            if hasattr(last_error, "stderr") and last_error.stderr:
                error_details.append(f"{'=' * 20} Stderr {'=' * 20}\n{last_error.stderr.strip()}")
            self.logger.error("\n".join(error_details))

    def _lower_than_v3_14_0_0(self):
        dialog = CTkInputDialog(
            title=self.app_translator.translate("pages.utilities.switch_regions"),
            text=self.app_translator.translate("modules.utilities.enter_region_code_message"),
            font=customtkinter.CTkFont(family=self.font_family, size=13)
        )

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        self.logger.debug("Dialog Window Geometry Set to: " + f"+{x}+{y}")

        app_icon = AppResources.app_icon()
        if app_icon:
            dialog.after(200, lambda: dialog.iconbitmap(app_icon))

        user_input = dialog.get_input()

        if not user_input:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: No Input Provided")
            return

        user_input = user_input.strip().upper()

        if user_input not in iso3166.countries_by_alpha2:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: Region Code Not Found")
            return

        reg_path = r"SOFTWARE\WOW6432Node\MSPCManager Store"
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                winreg.SetValueEx(key, "InstallRegionCode", 0, winreg.REG_SZ, user_input)
            self._log(
                self.app_translator.translate("modules.utilities.modify_mspcm_region_registry_value_successfully").format(
                    region_code=user_input
                )
            )
            self.logger.info(f"Successfully switched Microsoft PC Manager region setting, region code: {user_input}")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.modify_mspcm_region_registry_value_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Modifying Microsoft PC Manager Region Registry: {e}")

    def _lower_than_v3_14_0_0_with_ownership(self):
        dialog = CTkInputDialog(
            title=self.app_translator.translate("pages.utilities.switch_regions"),
            text=self.app_translator.translate("modules.utilities.enter_region_code_message"),
            font=customtkinter.CTkFont(family=self.font_family, size=13)
        )

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        self.logger.debug("Dialog Window Geometry Set to: " + f"+{x}+{y}")

        app_icon = AppResources.app_icon()
        if app_icon:
            dialog.after(200, lambda: dialog.iconbitmap(app_icon))

        user_input = dialog.get_input()

        if not user_input:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: No Input Provided")
            return

        user_input = user_input.strip().upper()

        if user_input not in iso3166.countries_by_alpha2:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: Region Code Not Found")
            return

        reg_path = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager Store"
        try:
            cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                "reg.exe",
                "add",
                reg_path,
                "/v",
                "InstallRegionCode",
                "/t",
                "REG_SZ",
                "/d",
                user_input,
                "/f"
            ]
            result = subprocess.run(
                cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # NSudo Error Dealing
            if result.returncode != 0:
                if result.stdout:
                    self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                    self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                    self.logger.error(f"NSudo Error Code: {result.returncode}")
                    self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                raise Exception(f"NSudo Error Code: {result.returncode}")

            # reg.exe Error Dealing
            if result.stderr:
                self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                raise Exception(f"An Error Occurred While Modifying Microsoft PC Manager Region Registry: {result.stderr.strip()}")

            # Success
            self._log(
                self.app_translator.translate("modules.utilities.modify_mspcm_region_registry_value_successfully").format(
                    region_code=user_input
                )
            )
            self.logger.info(f"Successfully Switched Microsoft PC Manager Region Setting, Region Code: {user_input}")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.modify_mspcm_region_registry_value_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Modifying Microsoft PC Manager Region Registry: {e}")
