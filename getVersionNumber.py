import winreg

class GetPCManagerVersion:
    def __init__(self):
        super().__init__()
        self.get_current_pc_manager_version = self._get_current_pc_manager_version
        self.get_current_pc_manager_beta_version = self._get_current_pc_manager_beta_version

    def _get_current_pc_manager_version(self):
        # Microsoft PC Manager
        version = None
        if version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications") as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if "Microsoft.MicrosoftPCManager_" in subkey_name:
                            version = subkey_name.split('_')[1]
                            break
            except FileNotFoundError:
                pass

            if version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                        r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\\Schemas") as key:
                        package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                        version = package_full_name.split('_')[1]
                except FileNotFoundError:
                    pass

                if version is None:
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager Store") as key:
                            version = winreg.QueryValueEx(key, "ProductVersion")[0]
                    except FileNotFoundError:
                        pass
        return version

    def _get_current_pc_manager_beta_version(self):
        # Microsoft PC Manager Beta
        beta_version = None
        if beta_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager") as key:
                    beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
            except FileNotFoundError:
                pass

            if beta_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MSPCManager") as key:
                        beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                except FileNotFoundError:
                    pass
        return beta_version

    def refresh_version(self):
        return self.get_current_pc_manager_version(), self.get_current_pc_manager_beta_version()
