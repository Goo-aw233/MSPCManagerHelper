import ctypes
import iso3166
import subprocess
import winreg


class SwitchRegions:

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def execute_switch(self, is_old_version, region_code=None):
        if is_old_version:
            return self._switch_regions_old(region_code)
        else:
            return self._switch_regions_new()

    def _switch_regions_old(self, region_code):
        output = []
        # Validate region_code
        user_input = region_code.strip().upper()
        if user_input not in iso3166.countries_by_alpha2:
            return f"{self.translator.translate('unknown_region_code')}: {user_input}"

        output.append(f"{self.translator.translate('the_region_code_that_is_currently_entered')}: {user_input}")

        _MICROSOFT_PC_MANAGER_REG_PATH = r"SOFTWARE\\WOW6432Node\\MSPCManager Store"
        _MICROSOFT_PC_MANAGER_REGION_VALUE_NAME = "InstallRegionCode"
        
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                _MICROSOFT_PC_MANAGER_REG_PATH,
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE | winreg.KEY_CREATE_SUB_KEY
            ) as reg_key:
                try:
                    # Query If the Registry Value Exists and Delete If It Exists
                    winreg.QueryValueEx(reg_key, _MICROSOFT_PC_MANAGER_REGION_VALUE_NAME)
                    winreg.DeleteValue(reg_key, _MICROSOFT_PC_MANAGER_REGION_VALUE_NAME)
                    output.append(self.translator.translate("existing_region_code_deleted"))
                except FileNotFoundError:
                    pass  # Value doesn't exist, which is fine.
                
                # Create & Write
                winreg.SetValueEx(
                    reg_key,
                    _MICROSOFT_PC_MANAGER_REGION_VALUE_NAME,
                    0,
                    winreg.REG_SZ,
                    user_input
                )
                output.append(self.translator.translate("region_code_written_successfully"))

                # Output Microsoft PC Manager Current Region Code
                value, regtype = winreg.QueryValueEx(reg_key, _MICROSOFT_PC_MANAGER_REGION_VALUE_NAME)
                output.append(f"{self.translator.translate('current_microsoft_pc_manager_region')}: {value}")
        except PermissionError:
            output.append(self.translator.translate("permission_denied_when_modifying_registry"))
        except Exception as e:
            output.append(self.translator.translate("an_error_occurred_when_modifying_the_microsoft_pc_manager_region"))
            output.append(f"{self.translator.translate('exception_context')}: {e}")
        
        return "\n".join(output)

    def _switch_regions_new(self):
        open_region_settings = ["cmd.exe", "/C", "start", "ms-settings:regionformatting"]
        try:
            subprocess.run(
                open_region_settings,
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=True
            )
            return self.translator.translate("region_settings_successfully_opened")
        except subprocess.CalledProcessError as e:
            return (f"{self.translator.translate('an_error_occurred_when_opening_settings')}\n"
                    f"{self.translator.translate('exception_context')}: {e}\n"
                    f"{self.translator.translate('error_code')}: {self.error_code}\n"
                    f"{self.translator.translate('error_message')}: {self.error_message}")
        except Exception as e:
            return (f"{self.translator.translate('an_error_occurred_when_opening_settings')}\n"
                    f"{self.translator.translate('exception_context')}: {e}")
