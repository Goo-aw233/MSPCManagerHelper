from .install_microsoft_edge_webview2_runtime import InstallMicrosoftEdgeWebView2Runtime
from .install_via_appxmanifest import InstallViaAppxManifest
from .install_via_dism_for_all_users import InstallViaDISMForAllUsers
from .install_via_microsoft_store import InstallViaMicrosoftStore
from .install_via_powershell_for_current_user import InstallViaPowerShellForCurrentUser
from .install_via_winget import InstallViaWinGet
# from .reinstall_via_powershell import ReinstallViaPowerShell
from .update_via_application_package import UpdateViaApplicationPackage

__all__ = [
    "InstallMicrosoftEdgeWebView2Runtime",
    "InstallViaAppxManifest",
    "InstallViaDISMForAllUsers",
    "InstallViaMicrosoftStore",
    "InstallViaPowerShellForCurrentUser",
    "InstallViaWinGet",
    # "ReinstallViaPowerShell",
    "UpdateViaApplicationPackage"
]
