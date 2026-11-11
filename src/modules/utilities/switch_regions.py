import subprocess
import winreg

import iso3166

from core import (
    AppLogger,
    AppResources,
    AppSettings,
    WindowsUtilities
)
from handlers.shared.launch_uri import URILauncher


class SwitchRegions:
    def __init__(self, logger, app_translator, log_callback, selected_mspcm_version, region_code,
                 run_on_ui_thread=None):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_mspcm_version = selected_mspcm_version
        self.region_code = region_code
        self.run_on_ui_thread = run_on_ui_thread
        self.nsudo_path = AppResources.nsudo_path()
        self.log_file_path = AppLogger.get_log_file_path()

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
        URILauncher.launch_uri(
            uri="ms-settings:regionformatting",
            target_name="Language & Region settings",
            messagebox_error_message="handlers.open_region_settings_error",
            logger=self.logger,
            log_file_path=self.log_file_path,
            app_translator=self.app_translator,
            run_on_ui_thread=self.run_on_ui_thread
        )

    def _lower_than_v3_14_0_0(self):
        user_input = self.region_code or ""

        if not user_input:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: No Input Provided")
            return

        user_input = user_input.strip().upper()

        if user_input not in iso3166.countries_by_alpha2:
            self._log(
                self.app_translator.translate("modules.utilities.invalid_region_code_with_input").format(
                    region_code=user_input
                )
            )
            self.logger.error(f"Invalid Region Code: Region Code Not Found: {user_input}")
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
        user_input = self.region_code or ""

        if not user_input:
            self._log(self.app_translator.translate("modules.utilities.invalid_region_code"))
            self.logger.error("Invalid Region Code: No Input Provided")
            return

        user_input = user_input.strip().upper()

        if user_input not in iso3166.countries_by_alpha2:
            self._log(
                self.app_translator.translate("modules.utilities.invalid_region_code_with_input").format(
                    region_code=user_input
                )
            )
            self.logger.error(f"Invalid Region Code: Region Code Not Found: {user_input}")
            return

        reg_path = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MSPCManager Store"
        try:
            cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                str(WindowsUtilities.reg()),
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
                encoding="oem",
                errors="replace",
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # NSudo Error Dealing
            if result.returncode != 0:
                if result.stdout:
                    self._log(f"NSudo {self.app_translator.translate('common.return_code')}: {result.returncode}")
                    self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                    self.logger.error(f"NSudo Return Code: {result.returncode}")
                    self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                raise Exception(f"NSudo Return Code: {result.returncode}")

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
