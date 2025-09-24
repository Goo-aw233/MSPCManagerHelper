import ctypes
import subprocess


class ViewInstalledAntiVirusProducts:
    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def view_in_compatibility_mode(self):
        try:
            command = [
                "powershell.exe",
                "-Command",
                (
                    "Get-WmiObject -Namespace ROOT\\SecurityCenter2 -Class AntiVirusProduct | "
                    "Select-Object displayName, instanceGuid, pathToSignedProductExe, pathToSignedReportingExe, "
                    "productState, timestamp, PSComputerName"
                )
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                return f"{self.translator.translate('powershell_command_failed')}:\n{result.stderr}"
            return self._format_output(result.stdout)
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_while_getting_all_installed_antivirus_products')}\n"
                    f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")

    def view_in_normal_mode(self):
        try:
            command = [
                "powershell.exe",
                "-Command",
                (
                    "Get-CimInstance -Namespace ROOT\\SecurityCenter2 -ClassName AntiVirusProduct | "
                    "Select-Object displayName, instanceGuid, pathToSignedProductExe, pathToSignedReportingExe, "
                    "productState, timestamp, PSComputerName"
                )
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                return f"{self.translator.translate('powershell_command_failed')}:\n{result.stderr}"
            return self._format_output(result.stdout)
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_while_getting_all_installed_antivirus_products')}\n"
                    f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")

    def _format_output(self, output):
        if not output.strip():
            return self.translator.translate("no_antivirus_products_found")

        formatted_result = []
        products = output.strip().split('\n\n')
        
        for product_info in products:
            details = {}
            for item in product_info.split("\n"):
                if ":" in item:
                    key, value = item.split(":", 1)
                    details[key.strip()] = value.strip()
            
            product_details = [
                f"{self.translator.translate('display_name')}: {details.get('displayName', '')}",
                f"{self.translator.translate('instance_guid')}: {details.get('instanceGuid', '')}",
                f"{self.translator.translate('path_to_signed_product_exe')}: {details.get('pathToSignedProductExe', '')}",
                f"{self.translator.translate('path_to_signed_reporting_exe')}: {details.get('pathToSignedReportingExe', '')}",
                f"{self.translator.translate('product_state')}: {details.get('productState', '')}",
                f"{self.translator.translate('timestamp')}: {details.get('timestamp', '')}",
                f"{self.translator.translate('ps_computer_name')}: {details.get('PSComputerName', '')}"
            ]
            formatted_result.append("\n".join(product_details))
            
        return "\n\n".join(formatted_result)
