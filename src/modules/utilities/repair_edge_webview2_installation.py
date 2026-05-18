import os
import shutil
import subprocess
import winreg
from pathlib import Path
from tkinter import messagebox

import psutil

from core import (
    AppResources,
    AppSettings
)


class RepairEdgeWebView2Installation:
    def __init__(self, logger, app_translator, log_callback, selected_edge_webview2_repair_options):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_edge_webview2_repair_options = selected_edge_webview2_repair_options
        self.nsudo_path = AppResources.nsudo_path()

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        self.logger.debug(f"Selected Microsoft Edge WebView2 Repair Options: {self.selected_edge_webview2_repair_options}")
        use_ownership = AppSettings.is_take_ownership_enabled()
        if use_ownership:
            self.logger.debug(f"NSudo Path: {self.nsudo_path}")

        for option, enabled in self.selected_edge_webview2_repair_options.items():
            if not enabled:
                continue

            if option == "restore_ifeo_registry":
                if use_ownership:
                    self._restore_ifeo_reg_key_with_ownership()
                else:
                    self._restore_ifeo_reg_key()

            elif option == "remove_edgeupdate_registry":
                if use_ownership:
                    self._remove_edgeupdate_reg_key_with_ownership()
                else:
                    self._remove_edgeupdate_reg_key()

            elif option == "remove_webview2_dir":
                if self.selected_edge_webview2_repair_options.get("end_related_processes"):
                    if use_ownership:
                        self._end_related_processes_with_ownership()
                    else:
                        self._end_related_processes()
                if use_ownership:
                    self._remove_webview2_dir_with_ownership()
                else:
                    self._remove_webview2_dir()

            elif option == "remove_edge_components_dir":
                if self.selected_edge_webview2_repair_options.get("end_related_processes"):
                    if use_ownership:
                        self._end_related_processes_with_ownership()
                    else:
                        self._end_related_processes()
                if use_ownership:
                    self._remove_edge_components_dir_with_ownership()
                else:
                    self._remove_edge_components_dir()

    def _restore_ifeo_reg_key(self):
        msedgeupdate_ifeo_key = (
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
            r"\MicrosoftEdgeUpdate.exe"
        )

        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, msedgeupdate_ifeo_key)
            self._log(self.app_translator.translate("modules.utilities.remove_ifeo_registry_key_successfully"))
            self.logger.info("Old IFEO registry key removed Successfully.")
        except FileNotFoundError:
            pass
        except PermissionError:
            self._log(self.app_translator.translate("modules.utilities.remove_ifeo_registry_key_permission_error"))
            self.logger.warning("Permission Denied While Removing IFEO Registry Key. Please run the application as administrator and try again.")
            return
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.remove_ifeo_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Removing IFEO Registry Key: {e}")
            return

        try:
            key = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE,
                msedgeupdate_ifeo_key,
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(key, "DisableExceptionChainValidation", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            self._log(self.app_translator.translate("modules.utilities.create_ifeo_registry_key_successfully"))
            self.logger.info("IFEO registry key created Successfully.")
        except PermissionError:
            self._log(self.app_translator.translate("modules.utilities.create_ifeo_registry_key_permission_error"))
            self.logger.warning("Permission Denied While Creating IFEO Registry Key. Please run the application as administrator and try again.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.create_ifeo_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Creating IFEO Registry Key: {e}")

    def _restore_ifeo_reg_key_with_ownership(self):
        msedgeupdate_ifeo_key = (
            r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            r"\Image File Execution Options\MicrosoftEdgeUpdate.exe"
        )

        try:
            del_cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                "reg.exe",
                "delete",
                msedgeupdate_ifeo_key,
                "/f"
            ]
            result = subprocess.run(
                del_cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # NSudo Error Dealing
            if result.returncode != 0:
                if result.stdout:
                    self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                    self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                    self.logger.error(f"NSudo Error Code: {result.returncode}")
                    self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                raise Exception(f"NSudo Error Code: {result.returncode}")

            # reg.exe Error Dealing
            if result.stderr:
                self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                raise Exception(f"An Error Occurred While Removing IFEO Registry Key:\n{result.stderr}")

            # Success
            self._log(self.app_translator.translate("modules.utilities.remove_ifeo_registry_key_successfully"))
            self.logger.info("IFEO registry key removed Successfully.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.remove_ifeo_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Removing IFEO Registry Key: {e}")
            return

        try:
            add_cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                "reg.exe",
                "add",
                msedgeupdate_ifeo_key,
                "/v",
                "DisableExceptionChainValidation",
                "/t",
                "REG_DWORD",
                "/d",
                "0",
                "/f"
            ]
            result = subprocess.run(
                add_cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # NSudo Error Dealing
            if result.returncode != 0:
                if result.stdout:
                    self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                    self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                    self.logger.error(f"NSudo Error Code: {result.returncode}")
                    self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                raise Exception(f"NSudo Error Code: {result.returncode}")

            # reg.exe Error Dealing
            if result.stderr:
                self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                raise Exception(f"An Error Occurred While Creating IFEO Registry Key:\n{result.stderr}")

            # Success
            self._log(self.app_translator.translate("modules.utilities.create_ifeo_registry_key_successfully"))
            self.logger.info("IFEO registry key created Successfully.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.create_ifeo_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Creating IFEO Registry Key: {e}")

    def _remove_edgeupdate_reg_key(self):
        edgeupdate_reg_key = r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate"

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
            _delete_key_tree(winreg.HKEY_LOCAL_MACHINE, edgeupdate_reg_key)
            self._log(self.app_translator.translate("modules.utilities.remove_edgeupdate_registry_key_successfully"))
            self.logger.info("EdgeUpdate registry key removed successfully.")
        except FileNotFoundError:
            pass
        except PermissionError:
            self._log(self.app_translator.translate("modules.utilities.remove_edgeupdate_registry_key_permission_error"))
            self.logger.warning("Permission Denied While Removing EdgeUpdate.exe Registry Key. Please run the application as administrator and try again.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.remove_edgeupdate_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Removing EdgeUpdate.exe Registry Key: {e}")

    def _remove_edgeupdate_reg_key_with_ownership(self):
        edgeupdate_reg_key = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate"

        try:
            del_cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                "reg.exe",
                "delete",
                edgeupdate_reg_key,
                "/f"
            ]
            result = subprocess.run(
                del_cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # NSudo Error Dealing
            if result.returncode != 0:
                if result.stdout:
                    self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                    self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                    self.logger.error(f"NSudo Error Code: {result.returncode}")
                    self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                raise Exception(f"NSudo Error Code: {result.returncode}")

            # reg.exe Error Dealing
            if result.stderr:
                self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                raise Exception(f"An Error Occurred While Removing EdgeUpdate Registry Key:\n{result.stderr}")

            # Success
            self._log(self.app_translator.translate("modules.utilities.remove_edgeupdate_registry_key_successfully"))
            self.logger.info("EdgeUpdate registry key removed successfully.")
        except Exception as e:
            self._log(
                self.app_translator.translate("modules.utilities.remove_edgeupdate_registry_key_error").format(
                    error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Removing EdgeUpdate.exe Registry Key: {e}")

    def _remove_webview2_dir(self):
        webview2_dir_path = Path(os.getenv("ProgramFiles(x86)")) / "Microsoft" / "EdgeWebView"

        if not webview2_dir_path.exists():
            self._log(self.app_translator.translate("modules.utilities.webview2_dir_not_exist"))
            self.logger.info("Microsoft Edge WebView2 directory does not exist.")
            return
        if any(webview2_dir_path.iterdir()):
            self.logger.warning("Microsoft Edge WebView2 directory is not empty.")
            result = messagebox.askyesno(
                self.app_translator.translate("modules.utilities.confirm_remove_webview2_dir_title"),
                self.app_translator.translate("modules.utilities.confirm_remove_webview2_dir_message")
            )
            if not result:
                self._log(self.app_translator.translate("pages.common.canceled_operation"))
                self.logger.info("The operation was canceled by the user.")
                return

        while True:
            try:
                shutil.rmtree(webview2_dir_path)
                self._log(self.app_translator.translate("modules.utilities.remove_webview2_dir_successfully"))
                self.logger.info("Microsoft Edge WebView2 directory removed successfully.")
                break
            except Exception as e:
                self.logger.error(f"An Error Occurred While Removing Microsoft Edge WebView2 Directory: {e}")
                if not messagebox.askretrycancel(
                    self.app_translator.translate("common.error"),
                    self.app_translator.translate("modules.utilities.remove_webview2_dir_error").format(
                        error=str(e)
                    )
                ):
                    self._log(
                        self.app_translator.translate("modules.utilities.remove_webview2_dir_error").format(
                            error=str(e)
                        )
                    )
                    break

    def _remove_webview2_dir_with_ownership(self):
        webview2_dir_path = Path(os.getenv("ProgramFiles(x86)")) / "Microsoft" / "EdgeWebView"

        if not webview2_dir_path.exists():
            self._log(self.app_translator.translate("modules.utilities.webview2_dir_not_exist"))
            self.logger.info("Microsoft Edge WebView2 directory does not exist.")
            return
        if any(webview2_dir_path.iterdir()):
            self.logger.warning("Microsoft Edge WebView2 directory is not empty.")
            result = messagebox.askyesno(
                self.app_translator.translate("modules.utilities.confirm_remove_webview2_dir_title"),
                self.app_translator.translate("modules.utilities.confirm_remove_webview2_dir_message")
            )
            if not result:
                self._log(self.app_translator.translate("pages.common.canceled_operation"))
                self.logger.info("User canceled the removal of Microsoft Edge WebView2 directory.")
                return

        while True:
            try:
                remove_cmd = [
                    self.nsudo_path,
                    "-U:T",
                    "-P:E",
                    "-ShowWindowMode:Hide",
                    "-UseCurrentConsole",
                    "cmd.exe",
                    "/C",
                    "RMDIR",
                    "/S",
                    "/Q",
                    str(webview2_dir_path)
                ]
                result = subprocess.run(
                    remove_cmd,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                # NSudo Error Dealing
                if result.returncode != 0:
                    if result.stdout:
                        self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                        self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                        self.logger.error(f"NSudo Error Code: {result.returncode}")
                        self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                    raise Exception(f"NSudo Error Code: {result.returncode}")

                # CMD Error Dealing
                if webview2_dir_path.exists():
                    if result.stderr:
                        self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                        self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                    raise Exception("Directory still exists.")

                # Success
                self._log(self.app_translator.translate("modules.utilities.remove_webview2_dir_successfully"))
                self.logger.info("Microsoft Edge WebView2 directory removed successfully.")
                break
            except Exception as e:
                self.logger.error(f"An Error Occurred While Removing Microsoft Edge WebView2 Directory: {e}")
                if not messagebox.askretrycancel(
                    self.app_translator.translate("common.error"),
                    self.app_translator.translate("modules.utilities.remove_webview2_dir_error").format(
                        error=str(e)
                    )
                ):
                    self._log(
                        self.app_translator.translate("modules.utilities.remove_webview2_dir_error").format(
                            error=str(e)
                        )
                    )
                    break

    def _remove_edge_components_dir(self):
        edge_components_dir_path = Path(os.getenv("ProgramFiles(x86)")) / "Microsoft"

        if not edge_components_dir_path.exists():
            self._log(self.app_translator.translate("modules.utilities.edge_components_dir_not_exist"))
            self.logger.info("Microsoft Edge components directory does not exist.")
            return
        if any(edge_components_dir_path.iterdir()):
            self.logger.warning("Microsoft Edge components directory is not empty.")
            result = messagebox.askyesno(
                self.app_translator.translate("modules.utilities.confirm_remove_edge_components_dir_title"),
                self.app_translator.translate("modules.utilities.confirm_remove_edge_components_dir_message")
            )
            if not result:
                self._log(self.app_translator.translate("pages.common.canceled_operation"))
                self.logger.info("The operation was canceled by the user.")
                return
        while True:
            try:
                shutil.rmtree(edge_components_dir_path)
                self._log(self.app_translator.translate("modules.utilities.remove_edge_components_dir_successfully"))
                self.logger.info("Microsoft Edge components directory removed successfully.")
                break
            except Exception as e:
                self.logger.error(f"An Error Occurred While Removing Microsoft Edge Components Directory: {e}")
                if not messagebox.askretrycancel(
                    self.app_translator.translate("common.error"),
                    self.app_translator.translate("modules.utilities.remove_edge_components_dir_error").format(
                        error=str(e)
                    )
                ):
                    self._log(
                        self.app_translator.translate("modules.utilities.remove_edge_components_dir_error").format(
                            error=str(e)
                        )
                    )
                    break

    def _remove_edge_components_dir_with_ownership(self):
        edge_components_dir_path = Path(os.getenv("ProgramFiles(x86)")) / "Microsoft"

        if not edge_components_dir_path.exists():
            self._log(self.app_translator.translate("modules.utilities.edge_components_dir_not_exist"))
            self.logger.info("Microsoft Edge components directory does not exist.")
            return
        if any(edge_components_dir_path.iterdir()):
            self.logger.warning("Microsoft Edge components directory is not empty.")
            result = messagebox.askyesno(
                self.app_translator.translate("modules.utilities.confirm_remove_edge_components_dir_title"),
                self.app_translator.translate("modules.utilities.confirm_remove_edge_components_dir_message")
            )
            if not result:
                self._log(self.app_translator.translate("pages.common.canceled_operation"))
                self.logger.info("The operation was canceled by the user.")
                return

        while True:
            try:
                remove_cmd = [
                    self.nsudo_path,
                    "-U:T",
                    "-P:E",
                    "-ShowWindowMode:Hide",
                    "-UseCurrentConsole",
                    "cmd.exe",
                    "/C",
                    "RMDIR",
                    "/S",
                    "/Q",
                    str(edge_components_dir_path)
                ]
                result = subprocess.run(
                    remove_cmd,
                    shell=False,
                    text=True,
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                # NSudo Error Dealing
                if result.returncode != 0:
                    if result.stdout:
                        self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                        self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                        self.logger.error(f"NSudo Error Code: {result.returncode}")
                        self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                    raise Exception(f"NSudo Error Code: {result.returncode}")
                
                # CMD Error Dealing
                if edge_components_dir_path.exists():
                    if result.stderr:
                        self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                        self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                    raise Exception("Directory still exists.")

                # Success
                self._log(self.app_translator.translate("modules.utilities.remove_edge_components_dir_successfully"))
                self.logger.info("Microsoft Edge components directory removed successfully.")
                break
            except Exception as e:
                self.logger.error(f"An Error Occurred While Removing Microsoft Edge Components Directory: {e}")
                if not messagebox.askretrycancel(
                    self.app_translator.translate("common.error"),
                    self.app_translator.translate("modules.utilities.remove_edge_components_dir_error").format(
                        error=str(e)
                    )
                ):
                    self._log(
                        self.app_translator.translate("modules.utilities.remove_edge_components_dir_error").format(
                            error=str(e)
                        )
                    )
                    break

    def _end_related_processes(self):
        processes_list = [
            "CopilotUpdate.exe",
            "MicrosoftEdgeUpdate.exe",
            "mscopilot.exe",
            "msedge.exe",
            "msedgewebview2.exe"
        ]
        found_processes = set()

        for proc in psutil.process_iter([ "name" ]):
            try:
                proc_name = proc.info["name"]
                if proc_name in processes_list:
                    found_processes.add(proc_name)
                    proc.kill()
                    self._log(
                        self.app_translator.translate("modules.utilities.ended_process").format(
                            proc_name=proc_name
                        )
                    )
                    self.logger.info(f"Ended Process: {proc_name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                self._log(f"{self.app_translator.translate('modules.utilities.end_process_error')}: {proc.info.get('name', 'Unknown')} - {e}")
                self.logger.error(f"An Error Occurred While Ending Process: {proc.info.get('name', 'Unknown')} - {e}")

        for process_name in processes_list:
            if process_name not in found_processes:
                self._log(
                    self.app_translator.translate("modules.utilities.skipped_not_running_process_message").format(
                        process_name=process_name
                    )
                )
                self.logger.info(f"The process {process_name} is not running, skipped.")

    def _end_related_processes_with_ownership(self):
        processes_list = [
            "CopilotUpdate.exe",
            "MicrosoftEdgeUpdate.exe",
            "mscopilot.exe",
            "msedge.exe",
            "msedgewebview2.exe"
        ]

        for process_name in processes_list:
            cmd = [
                self.nsudo_path,
                "-U:T",
                "-P:E",
                "-ShowWindowMode:Hide",
                "-UseCurrentConsole",
                "taskkill.exe",
                "/F",
                "/IM",
                process_name
            ]
            try:
                result = subprocess.run(
                    cmd,
                    shell=False,
                    text=True,
                    capture_output=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                # NSudo Error Dealing
                if result.returncode != 0:
                    self._log(
                        f"{self.app_translator.translate('modules.utilities.end_process_error')}: {process_name}"
                    )
                    self.logger.error(f"An Error Occurred While Ending Process: {process_name}")
                    if result.stdout:
                        self._log(f"NSudo {self.app_translator.translate('common.error_code')}: {result.returncode}")
                        self._log(f"===== {self.app_translator.translate('common.stdout')}: =====\n{result.stdout}")
                        self.logger.error(f"NSudo Error Code: {result.returncode}")
                        self.logger.error(f"===== Stdout: =====\n{result.stdout}")
                    continue

                # taskkill.exe Error Dealing
                if result.stderr:
                    self._log(f"{self.app_translator.translate('modules.utilities.end_process_error')}: {process_name}")
                    self.logger.error(f"An Error Occurred While Ending Process: {process_name}")
                    self._log(f"===== {self.app_translator.translate('common.stderr')}: =====\n{result.stderr}")
                    self.logger.error(f"===== Stderr: =====\n{result.stderr}")
                    continue

                # Success
                self._log(f"{self.app_translator.translate('modules.utilities.ended_process')}: {process_name}")
                self.logger.info(f"Ended Process: {process_name}")
            except Exception as e:
                self._log(
                    f"{self.app_translator.translate('modules.utilities.end_process_error')}: {process_name} - {e}"
                )
                self.logger.error(f"An Error Occurred While Ending Process: {process_name} - {e}")
