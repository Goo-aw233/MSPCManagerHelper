import json
import os
import subprocess
import winreg
from pathlib import Path

import pefile


class GetDependenciesVersion:
    def __init__(self, logger, app_translator, log_callback, selected_dependencies):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_dependencies = selected_dependencies

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        self.logger.debug(f"Selected Dependencies: {self.selected_dependencies}")
        for dependency in self.selected_dependencies:
            if dependency == "system_webview2":
                self._system_webview2_version()
            elif dependency == "global_webview2":
                self._global_webview2_version()
            elif dependency == "windows_app_runtime":
                self._windows_app_runtime_version()

    def _system_webview2_version(self):
        system_webview2_dir = Path(os.getenv("SystemRoot", r"C:\Windows")) / "System32" / "Microsoft-Edge-WebView"

        if system_webview2_dir.exists():
            for exe_path in system_webview2_dir.rglob("msedgewebview2.exe"):
                try:
                    pe = pefile.PE(str(exe_path))
                    if hasattr(pe, "VS_FIXEDFILEINFO"):
                        ver_info = pe.VS_FIXEDFILEINFO[0]
                        ms = ver_info.FileVersionMS
                        ls = ver_info.FileVersionLS
                        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                        self._log(
                            self.app_translator.translate("modules.utilities.system_webview2_version_is").format(
                                version=version
                            )
                        )
                        self.logger.info(f"System Microsoft Edge WebView2 Runtime Version: {version}")
                    pe.close()
                except Exception as e:
                    self._log(
                        self.app_translator.translate("modules.utilities.query_system_webview2_version_error").format(
                            error=str(e)
                        )
                    )
                    self.logger.error(
                        f"An Error Occurred While Querying the System Microsoft Edge WebView2 Runtime Version: {e}\n({exe_path})")
        else:
            self._log(self.app_translator.translate("modules.utilities.system_webview2_version_not_installed"))
            self.logger.info("System Microsoft Edge WebView2 Runtime is not installed.")

    def _global_webview2_version(self):
        global_webview2_reg_key = (
            r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients"
            r"\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        )

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, global_webview2_reg_key) as key:
                pv, _ = winreg.QueryValueEx(key, "pv")
                try:
                    channel, _ = winreg.QueryValueEx(key, "channel")
                except FileNotFoundError:
                    channel = None
                if channel:
                    self._log(
                        self.app_translator.translate("modules.utilities.global_webview2_version_is").format(
                            version=f"{pv} ({channel})"
                        )
                    )
                    self.logger.info(f"Global Microsoft Edge WebView2 Runtime Version: {pv} ({channel})")
                else:
                    self._log(
                        self.app_translator.translate("modules.utilities.global_webview2_version_is").format(version=pv)
                    )
                    self.logger.info(f"Global Microsoft Edge WebView2 Runtime Version: {pv}")
        except FileNotFoundError:
            webview2_base_dir = Path(os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft" / "EdgeWebView" / "Application"

            if webview2_base_dir and webview2_base_dir.exists():
                exe_paths = list(webview2_base_dir.rglob("msedgewebview2.exe"))
                if exe_paths:
                    for exe_path in exe_paths:
                        try:
                            pe = pefile.PE(str(exe_path))
                            if hasattr(pe, "VS_FIXEDFILEINFO"):
                                ver_info = pe.VS_FIXEDFILEINFO[0]
                                ms = ver_info.FileVersionMS
                                ls = ver_info.FileVersionLS
                                version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                                channel = None
                                self._log(
                                    self.app_translator.translate("modules.utilities.global_webview2_version_is").format(
                                        version=version
                                    )
                                    + f"\n{exe_path}"
                                )
                                self.logger.info(
                                    "Global Microsoft Edge WebView2 Runtime Version: "
                                    f"{version} (Path: {exe_path})"
                                )
                            pe.close()
                        except Exception as e:
                            self._log(
                                self.app_translator.translate("modules.utilities.query_global_webview2_version_error").format(
                                    error=str(e)
                                )
                            )
                            self.logger.error(
                                "An Error Occurred While Querying the Global Microsoft Edge WebView2 Runtime Version: " + str(e)
                            )
                    return
            self._log(self.app_translator.translate("modules.utilities.global_webview2_not_installed"))
            self.logger.info("Global Microsoft Edge WebView2 Runtime is not installed.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.query_global_webview2_version_error").format(
                    error=str(e)
                )
            )
            self.logger.error(
                "An Error Occurred While Querying the Global Microsoft Edge WebView2 Runtime Version: " + str(e))

    def _windows_app_runtime_version(self):
        get_windows_app_runtime_versions = (
            "Get-AppxPackage -Name '*WindowsAppRuntime*' |"
            "Select-Object Name, Version, PackageFullName |"
            "Sort-Object Version |"
            "ConvertTo-Json"
        )

        try:
            completed = subprocess.run(
                ["powershell.exe", "-NoProfile","-Command", get_windows_app_runtime_versions],
                check=True, text=True, capture_output=True, shell=False, creationflags=subprocess.CREATE_NO_WINDOW
            )
            raw_output = completed.stdout.strip()
            if raw_output:
                try:
                    data = json.loads(raw_output)
                    if isinstance(data, dict):
                        data = [data]
                    lines = []
                    for idx, item in enumerate(data):
                        lines.append(
                            f"{self.app_translator.translate('modules.utilities.windows_app_runtime_name')}: {item.get('Name', '')}\n"
                            f"{self.app_translator.translate('modules.utilities.windows_app_runtime_version')}: {item.get('Version', '')}\n"
                            f"{self.app_translator.translate('modules.utilities.windows_app_runtime_package_full_name')}: {item.get('PackageFullName', '')}"
                        )
                        if idx != len(data) - 1:
                            lines.append("-" * 30)
                    formatted_output = "\n".join(lines)
                    self._log(
                        self.app_translator.translate("modules.utilities.windows_app_runtime_info_is").format(
                            formatted_output=formatted_output
                            )
                        )
                    self.logger.info("Windows App Runtime Info:\n" + formatted_output)
                except Exception as e:
                    self._log(
                        self.app_translator.translate("modules.utilities.raw_windows_app_runtime_info_is").format(
                            raw_output=raw_output
                            ) + "\n(Formatting Error: " + str(e) + ")"
                        )
                    self.logger.error(f"An Error Occurred While Parsing Windows App Runtime Version JSON Output: {e}")
            else:
                self._log(self.app_translator.translate("modules.utilities.windows_app_runtime_not_found"))
                self.logger.info("Installed Windows App Runtime not found.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.query_windows_app_runtime_version_error").format(
                    error=str(e)
                    )
                )
            self.logger.error(f"An Error Occurred While Querying the Windows App Runtime Version: {e}")
