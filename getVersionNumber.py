import winreg

def get_current_pc_manager_version():
    version = None
    pcm_beta_installed = None

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

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\CurrentVersion\\AppModel\\SystemAppData\\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\\Schemas") as key:
            package_full_name = winreg.QueryValueEx(key, "PackageFullName")[0]
            version = package_full_name.split('_')[1]
    except FileNotFoundError:
        pass

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager Store") as key:
            version = winreg.QueryValueEx(key, "ProductVersion")[0]
    except FileNotFoundError:
        pass

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\MSPCManager") as key:
            pcm_beta_installed = winreg.QueryValueEx(key, "ProductVersion")[0]
    except FileNotFoundError:
        pass

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MSPCManager") as key:
            pcm_beta_installed = winreg.QueryValueEx(key, "ProductVersion")[0]
    except FileNotFoundError:
        pass

    return version, pcm_beta_installed
