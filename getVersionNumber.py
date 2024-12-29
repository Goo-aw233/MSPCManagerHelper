import winreg

class GetPCManagerVersion:
    def __init__(self):
        super().__init__()
        self.get_current_pc_manager_version = self._get_current_pc_manager_version
        self.get_current_pc_manager_beta_version = self._get_current_pc_manager_beta_version

    def _get_current_pc_manager_version(self):
        # Microsoft PC Manager
        pc_manager_version = None

        # 新版
        if pc_manager_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications") as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if "Microsoft.MicrosoftPCManager_" in subkey_name:
                            pc_manager_version = subkey_name.split('_')[1]
                            break
            except FileNotFoundError:
                pass

            # 旧版
            if pc_manager_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Applications") as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            subkey_name = winreg.EnumKey(key, i)
                            if "Microsoft.PCManager_" in subkey_name:
                                pc_manager_version = subkey_name.split('_')[1]
                                break
                except FileNotFoundError:
                    pass

                # 新版
                if pc_manager_version is None:
                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                            r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.PCManager_8wekyb3d8bbwe\\Schemas") as key:
                            package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                            pc_manager_version = package_full_name.split('_')[1]
                    except FileNotFoundError:
                        pass

                    # 旧版
                    if pc_manager_version is None:
                        try:
                            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\\Schemas") as key:
                                package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
                                pc_manager_version = package_full_name.split('_')[1]
                        except FileNotFoundError:
                            pass

                        # 使用 EXE 安装的版本
                        if pc_manager_version is None:
                            try:
                                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager Store") as key:
                                    pc_manager_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                            except FileNotFoundError:
                                pass
        return pc_manager_version

    def _get_current_pc_manager_beta_version(self):
        # Microsoft PC Manager Beta
        pc_manager_beta_version = None

        # Beta EXE 安装器写入路径
        if pc_manager_beta_version is None:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager") as key:
                    pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
            except FileNotFoundError:
                pass

            # Beta 卸载程序路径
            if pc_manager_beta_version is None:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MSPCManager") as key:
                        pc_manager_beta_version = winreg.QueryValueEx(key, "ProductVersion")[0]
                except FileNotFoundError:
                    pass
        return pc_manager_beta_version

    def refresh_version(self):
        return self.get_current_pc_manager_version(), self.get_current_pc_manager_beta_version()
