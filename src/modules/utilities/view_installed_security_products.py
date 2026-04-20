import json
import subprocess

from core import (
    AppSettings,
    PrerequisiteChecks
)


class ViewInstalledSecurityProducts:
    def __init__(self, logger, app_translator, log_callback, selected_security_product, output_as_raw_data=False):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_security_product = selected_security_product
        self.output_as_raw_data = output_as_raw_data

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        self.logger.debug(f"Selected Security Product: {self.selected_security_product}")
        if "antivirus" in self.selected_security_product:
            self._antivirus_products()

        if "antispyware" in self.selected_security_product:
            self._antispyware_products()

        if "firewall" in self.selected_security_product:
            self._firewall_products()

    @staticmethod
    def _get_display_width(text):
        return sum(2 if ord(c) > 127 else 1 for c in text)

    def _get_security_products(self, class_name, category_key):
        base_cmd_for_client = (
            r"Get-CimInstance -Namespace root/SecurityCenter2 -ClassName {class_name} |"
            r"Select-Object displayName, instanceGuid, pathToSignedProductExe,"
            r"pathToSignedReportingExe, productState, timeStamp, PSComputerName"
        )
        base_cmd_for_client_legacy = (
            r"Get-WmiObject -Namespace root\SecurityCenter2 -Class {class_name} |"
            r"Select-Object displayName, instanceGuid, pathToSignedProductExe,"
            r"pathToSignedReportingExe, productState, timeStamp, PSComputerName"
        )
        base_cmd_for_server = (
            r"Get-CimInstance -Namespace root/Microsoft/Windows/Defender -ClassName MSFT_MpComputerStatus"
        )

        is_server = False
        # Server
        if class_name == "AntiVirusProduct" and PrerequisiteChecks.check_windows_server_levels(check_type="is_windows_server"):
            final_command = base_cmd_for_server
            is_server = True
        # Client
        else:
            command = base_cmd_for_client_legacy if AppSettings.is_compatibility_mode_enabled() else base_cmd_for_client
            final_command = command.format(class_name=class_name)

        if not self.output_as_raw_data and not is_server:
            final_command += " | ConvertTo-Json -Compress"

        category_name = self.app_translator.translate(category_key)
        self._log(f"===== {category_name} =====")

        try:
            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-Command",
                    final_command
                ],
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                # Raw
                if self.output_as_raw_data or is_server:
                    self._log(result.stdout)
                    self.logger.info(result.stdout)
                # Formatted
                else:
                    self._process_formatted_output(result.stdout)
            else:
                self._log(self.app_translator.translate("an_error_occurred_while_querying_security_products").format(stderr=result.stderr))
                self.logger.error("An Error Occurred While Querying Security Products:\n" + result.stderr)
        except Exception as e:
            self._log(str(e))
            self.logger.error(f"Exception While Executing Security Products Query: {e}")

    def _process_formatted_output(self, json_output):
        if not json_output or not json_output.strip():
            self._log(self.app_translator.translate("no_security_products_found") + "\n")
            self.logger.info("No installed security products registered to Windows Security were found.\n")
            return

        try:
            data = json.loads(json_output)
            if isinstance(data, dict):
                data = [data]

            if not data:
                self._log(self.app_translator.translate("no_security_products_found") + "\n")
                self.logger.info("No installed security products registered to Windows Security were found.\n")
                return

            output_lines = []

            ordered_keys = [
                "displayName", "instanceGuid", "pathToSignedProductExe", 
                "pathToSignedReportingExe", "productState", "PSComputerName"
            ]

            key_map = {
                "displayName": "security_product_displayName",
                "instanceGuid": "security_product_instanceGuid",
                "pathToSignedProductExe": "security_product_pathToSignedProductExe",
                "pathToSignedReportingExe": "security_product_pathToSignedReportingExe",
                "productState": "security_product_productState",
                "PSComputerName": "security_product_PSComputerName",
            }

            translated_labels = {}
            max_width = 0

            for k in ordered_keys:
                translation_key = key_map.get(k, k)
                label = self.app_translator.translate(translation_key)
                translated_labels[k] = label
                max_width = max(max_width, self._get_display_width(label))

            for item in data:
                for k in ordered_keys:
                    val = item.get(k)
                    if val is None:
                        continue

                    label = translated_labels[k]
                    padding = " " * (max_width - self._get_display_width(label))
                    output_lines.append(f"{label}{padding} : {val}")
                output_lines.append("") # Separator Between Items

            self._log("\n".join(output_lines))
            self.logger.info("\n" + "\n".join(output_lines))

        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON from security products query.")
            self._log(json_output) # Fallback to Raw Output
            self.logger.info(json_output)
        except Exception as e:
            self._log(str(e))
            self.logger.error(f"Error Processing Security Products Output: {e}")

    def _antivirus_products(self):
        self._get_security_products("AntiVirusProduct", "security_product_category_antivirus")

    def _antispyware_products(self):
        self._get_security_products("AntiSpywareProduct", "security_product_category_antispyware")

    def _firewall_products(self):
        self._get_security_products("FirewallProduct", "security_product_category_firewall")
