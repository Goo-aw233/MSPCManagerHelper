import winreg

from core.app_metadata import AppMetadata
from core.app_resources import AppResources


class AppUserModelID:
    """Registers the AppUserModelID into the current user's registry before startup.

    Ref:
      - AppUserModelIDs (Win32): https://learn.microsoft.com/windows/win32/shell/appids
    """

    _logger = None

    _REGISTRY_BASE = r"Software\Classes\AppUserModelId"

    @classmethod
    def _get_logger(cls):
        if cls._logger is None:
            from core.app_logger import AppLogger

            cls._logger = AppLogger.get_logger()
        return cls._logger

    @classmethod
    def register(cls, aumid: str | None = None) -> bool:
        """AUMID registration.

        Creates HKEY_CURRENT_USER\\Software\\Classes\\AppUserModelId\\<aumid>
        (or reuses the existing key) and writes DisplayName / IconUri /
        ShowInSettings so Windows can associate toasts with this application.
        """
        logger = cls._get_logger()
        aumid = aumid or AppMetadata.APP_AUMID
        if not aumid:
            logger.warning("AppUserModelID: No AUMID provided, skipping registration.")
            return False

        reg_path = fr"{cls._REGISTRY_BASE}\{aumid}"
        try:
            with winreg.CreateKeyEx(
                winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, AppMetadata.APP_NAME)

                icon_uri = AppResources.app_icon()
                if icon_uri:
                    winreg.SetValueEx(key, "IconUri", 0, winreg.REG_SZ, icon_uri)

                winreg.SetValueEx(key, "ShowInSettings", 0, winreg.REG_DWORD, 1)
        except OSError as exc:
            logger.error(f"AppUserModelID: Failed to Register AUMID '{aumid}': {exc}")
            return False

        logger.info(f"AppUserModelID: Registered AUMID '{aumid}' at HKEY_CURRENT_USER\\{reg_path}")
        return True

    @classmethod
    def unregister(cls, aumid: str | None = None) -> bool:
        """AUMID cleanup.

        Removes HKEY_CURRENT_USER\\Software\\Classes\\AppUserModelId\\<aumid>
        (including any subkeys) so no stale AUMID entry is left behind after exit.
        """
        logger = cls._get_logger()
        aumid = aumid or AppMetadata.APP_AUMID
        if not aumid:
            logger.warning("AppUserModelID: No AUMID provided, skipping cleanup.")
            return False

        reg_path = fr"{cls._REGISTRY_BASE}\{aumid}"

        def _delete_key_tree(root_key, sub_key):
            with winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                while True:
                    try:
                        child_name = winreg.EnumKey(key, 0)
                        _delete_key_tree(root_key, f"{sub_key}\\{child_name}")
                    except OSError:
                        break
            winreg.DeleteKey(root_key, sub_key)

        try:
            _delete_key_tree(winreg.HKEY_CURRENT_USER, reg_path)
        except FileNotFoundError:
            logger.info(f"AppUserModelID: AUMID '{aumid}' not present, nothing to clean up.")
            return True
        except OSError as exc:
            logger.warning(f"AppUserModelID: Failed to Clean Up AUMID '{aumid}': {exc}")
            return False

        logger.info(f"AppUserModelID: Cleaned up AUMID '{aumid}' at HKEY_CURRENT_USER\\{reg_path}.")
        return True
