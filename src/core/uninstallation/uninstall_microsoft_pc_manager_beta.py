import ctypes
import os
import shutil
import subprocess
import winreg
from pathlib import Path

import psutil


class UninstallMicrosoftPCManagerBeta:
    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def uninstall_microsoft_pc_manager_beta(self, cleanup=False):
        if not self._check_if_installed():
            return self.translator.translate("microsoft_pc_manager_beta_not_installed")

        if not self._start_exe_uninstallation():
            return self.translator.translate("an_error_occurred_when_uninstalling_microsoft_pc_manager_beta")

        result_parts = []
        if cleanup:
            cleanup_result = self._cleanup_after_uninstallation()
            if cleanup_result:
                result_parts.append(cleanup_result)

        result_parts.append(self.translator.translate("uninstallation_process_completed_successfully"))
        return "\n".join(result_parts)

    @staticmethod
    def _check_if_installed():
        microsoft_pc_manager_dir = Path(os.environ['ProgramFiles']) / 'Microsoft PC Manager'
        uninst_exe_path = microsoft_pc_manager_dir / 'Uninst.exe'
        if not microsoft_pc_manager_dir.is_dir() or not uninst_exe_path.is_file():
            return False
        return True

    def _cleanup_after_uninstallation(self):
        results = []
        folders_to_delete = [
                    Path(os.environ['LocalAppData']) / 'PC Manager',
                    Path(os.environ['LocalAppData']) / 'Windows Master',
                    Path(os.environ['ProgramData']) / 'PCMConfigPath',
                    Path(os.environ['ProgramData']) / 'Windows Master',
                    Path(os.environ['ProgramData']) / 'Windows Master Setup',
                    Path(os.environ['ProgramFiles']) / 'Microsoft PC Manager',
                    Path(os.environ['ProgramFiles']) / 'WindowsMaster',
                    Path(os.environ['ProgramFiles']) / 'Windows Master',
                    Path(os.environ['SystemRoot']) / 'System32' / 'config' / 'systemprofile' / 'AppData' / 'Local' / 'Windows Master',
                    Path(os.environ['SystemRoot']) / 'SystemTemp' / 'Windows Master',
                    Path(os.environ['Temp']) / 'Windows Master',
                    Path(os.environ['Temp']) / 'WM Scan Test'
                ]

        for folder in folders_to_delete:
            if folder.exists():
                try:
                    shutil.rmtree(folder)
                    results.append(f"{self.translator.translate('removed_folder')}: {str(folder)}")
                except OSError as e:
                    results.append(f"{self.translator.translate('an_error_occurred_while_removing_a_folder')}\n"
                                   f"{self.translator.translate('folder_name')}: {str(folder)}\n"
                                   f"{self.translator.translate('exception_context')}: {e}")

        registries_to_delete = [
                    # HKCU
                    (winreg.HKEY_CURRENT_USER, r'Software\\WindowsMaster', None),
                    # HKLM
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run', 'WindowsMasterUI'),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 'WindowsMasterUI'),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\MSPCManager', None),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\微软电脑管家', None),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\WOW6432Node\\MSPCManager', None)
                ]

        for hive, key_path, value_name in registries_to_delete:
            try:
                if value_name:
                    with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
                        winreg.DeleteValue(key, value_name)
                        results.append(f"{self.translator.translate('removed_registry_value')}: {key_path}\\{value_name}")
                else:
                    winreg.DeleteKey(hive, key_path)
                    results.append(f"{self.translator.translate('removed_registry_key')}: {key_path}")
            except Exception as e:
                results.append(f"{self.translator.translate('an_error_occurred_while_removing_a_registry_key_or_value')}\n"
                               f"{self.translator.translate('key_or_value_name')}: {key_path}\\{value_name or ''}\n"
                               f"{self.translator.translate('exception_context')}: {e}")
        return "\n".join(results)

    def _start_exe_uninstallation(self):
        uninst_exe_path = Path(os.environ['ProgramFiles']) / 'Microsoft PC Manager' / 'Uninst.exe'
        try:
            uninstaller_process = subprocess.Popen([str(uninst_exe_path)])
            main_process = psutil.Process(uninstaller_process.pid)

            # 等待主进程及其所有子孙进程结束
            descendants = main_process.children(recursive=True)
            all_processes = descendants + [main_process]
            gone, alive = psutil.wait_procs(all_processes, timeout=300)  # 300 秒超时

            if alive:
                # 如果超时后仍有进程存活，尝试强制终止
                for p in alive:
                    try:
                        p.kill()
                    except psutil.NoSuchProcess:
                        pass  # 进程可能在我们尝试终止它之前就已经结束了
                return False, self.translator.translate(
                    "uninstallation_timed_out_and_remaining_processes_were_terminated")

            return True, self.translator.translate("uninstallation_process_completed_successfully")

        except FileNotFoundError:
            return False, f"{self.translator.translate('microsoft_pc_manager_beta_not_installed')}"
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            # 如果在监控过程中进程突然消失或访问被拒绝
            # 此时卸载程序可能已经结束，可以认为成功
            return True, f"{self.translator.translate('microsoft_pc_manager_beta_uninstalled_successfully')}"
        except Exception as e:
            return False, (f"{self.translator.translate('an_error_occurred_during_uninstallation')}\n"
                           f"{self.translator.translate('exception_context')}: {e}")

"""
    def _start_forceful_removal(self):
        try:
            progress_name = [
                "Microsoft.WIC.PCWndManager.Plugin.exe",
                "MSPCManager.exe",
                "MSPCManagerCore.exe",
                "MSPCManagerService.exe",
                "MSPCManagerWidget.exe",
                "MSPCWndManager.exe"
            ]

            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] in progress_name:
                    try:
                        process.kill()
                        print(f"{self.translator.translate('terminated_process')}: {process.info['name']} (PID: {process.info['pid']})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        print(f"{self.translator.translate('could_not_terminate_process')}: {process.info['name']}\n"
                              f"{self.translator.translate('exception_context')}: {e}")

            return True
        except Exception as e:
            print(f"{self.translator.translate('an_error_occurred_during_forceful_removal')}\n"
                  f"{self.translator.translate('exception_context')}: {e}")
            return False
"""
