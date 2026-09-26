from datetime import datetime


class AppMetadata:

    # Properties
    APP_AUMID = "GuCATs.MSPCManagerHelper"
    APP_AUTHOR = "GuCATs"
    APP_COPYRIGHT = f"\u00a9 2024 - {datetime.now().year} {APP_AUTHOR} All rights reserved."
    APP_GITHUB_REPOSITORY_URL = "https://github.com/Goo-aw233/MSPCManagerHelper"
    APP_LICENSE_URL = "https://github.com/Goo-aw233/MSPCManagerHelper/blob/main/LICENSE"
    APP_NAME = "MSPCManagerHelper"
    APP_VERSION_LABEL = "Beta"
    APP_VERSION_TUPLE: tuple[int, int, int, int] = (0, 3, 1, 0)
    APP_VERSION = f"{APP_VERSION_LABEL} v{'.'.join(map(str, APP_VERSION_TUPLE))}".strip()
    APP_VERSION_WITHOUT_SPACES = APP_VERSION.replace(" ", "_")

    # Contributors
    APP_CONTRIBUTORS = {
        "ArcticFoxPro": "https://github.com/ArcticFoxPro",
        "Goo-aw233": "https://github.com/Goo-aw233",
        "LuYang114": "https://github.com/LuYang114",
        "zwJimRaynor": "https://github.com/zwJimRaynor",
    }

    # Original URLs
    APP_UPDATE_1DRV_URL = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EtKwa-2la71HmG2RxkB5lngBvvRt9CFOYsyJG_HOwYIzNA"
    MICROSOFT_PC_MANAGER_URL = "https://pcmanager.microsoft.com"
    MSPCM_APP_PACKAGE_1DRV_URL = "https://gbcs6-my.sharepoint.com/:f:/g/personal/gucats_gbcs6_onmicrosoft_com/EoscJOQ9taJFtx9LZLPiBM0BEmVm7wsLuJOuHnwmo9EQ5w"
    MSPCM_ZHCN_DOC_URL = "https://docs.qq.com/doc/DR2FrVkJmT0NuZ0Zx"
    MSPCM_DOC_URL = "https://mspcmanager.github.io/mspcm-docs"

    # Redirected URLs
    APP_UPDATE_1DRV_DIR_URL = "https://go.gucats.com/MSPCManagerHelperOD"
    MSPCM_APP_PACKAGE_1DRV_DIR_URL = "https://go.gucats.com/MSPCMAppOD"
    MSPCM_ZHCN_DOC_DIR_URL = "https://go.gucats.com/MSPCMDocZH-CN"
    MSPCM_DOC_DIR_URL = "https://go.gucats.com/MSPCMDoc"
