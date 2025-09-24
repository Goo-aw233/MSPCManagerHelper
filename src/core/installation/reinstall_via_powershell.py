import ctypes
import subprocess


class ReinstallViaPowerShell:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def reinstall_via_powershell(self):
        commands = {
            "old_all_users": (
                'powershell.exe -Command '
                'Get-AppxPackage -AllUsers *Microsoft.PCManager* | '
                'Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppxManifest.xml"}'
            ),
            "old_current_user": (
                'powershell.exe -Command '
                'Get-AppxPackage *Microsoft.PCManager* | '
                'Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppxManifest.xml"}'
            ),
            "all_users": (
                'powershell.exe -Command '
                'Get-AppxPackage -AllUsers *Microsoft.MicrosoftPCManager* | '
                'Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppxManifest.xml"}'
            ),
            "current_user": (
                'powershell.exe -Command '
                'Get-AppxPackage *Microsoft.MicrosoftPCManager* | '
                'Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppxManifest.xml"}'
            ),
        }
        # 此处需要修改以联动多个复选框
        command = 
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                # Resources are Being Used
                if "0x80073D02" in result.stderr:
                    print("an_error_occurred_while_reinstalling_microsoft_pc_manager")
                    return print(f"{result.stdout}\n"
                                 f"{result.stderr}")
                return print("microsoft_pc_manager_installed_successfully")
            # Need to Run as Administrator
            elif result.returncode == 1:
                print("an_error_occurred_while_reinstalling_microsoft_pc_manager")
                return print(f"{result.stdout}\n"
                             f"{result.stderr}")
            # AppxManifest.xml Damage
            elif result.returncode == 2:
                print("an_error_occurred_while_reinstalling_microsoft_pc_manager")
                return print(f"{result.stdout}\n"
                             f"{result.stderr}")
            else:
                print("an_error_occurred_while_reinstalling_microsoft_pc_manager")
                return print(f"{result.stdout}\n"
                             f"{result.stderr}")
        except Exception as e:
            print("an_error_occurred_while_reinstalling_microsoft_pc_manager")
            return print(f"exception_context: {e}\n"
                         f"error_code: {self.error_code}\nerror_message: {self.error_message}")
