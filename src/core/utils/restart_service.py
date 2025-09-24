import ctypes
import subprocess
import time
import win32service
import win32serviceutil


class RestartService:

    _MICROSOFT_PC_MANAGER_SERVICE_NAME = "PCManager Service Store"
    _MICROSOFT_PC_MANAGER_BETA_SERVICE_NAME = "PCManager Service"

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def restart_service(self):
        return self._query_microsoft_pc_manager_service()

    def _query_microsoft_pc_manager_service(self):
        services = {
            "stable": self._MICROSOFT_PC_MANAGER_SERVICE_NAME,
            "beta": self._MICROSOFT_PC_MANAGER_BETA_SERVICE_NAME
        }
        exists = {}
        results = []

        for key, name in services.items():
            try:
                win32serviceutil.QueryServiceStatus(name)
                exists[key] = True
            except Exception:
                exists[key] = False

        # Both Services Exist
        if exists["stable"] and exists["beta"]:
            results.append(self._restart_microsoft_pc_manager_service())
            results.append(self._restart_microsoft_pc_manager_service_beta())
        # Only Stable Service Exists
        elif exists["stable"]:
            results.append(self._restart_microsoft_pc_manager_service())
        # Only Beta Service Exists
        elif exists["beta"]:
            results.append(self._restart_microsoft_pc_manager_service_beta())
        # Neither Service Exists
        else:
            results.append(self._microsoft_pc_manager_service_not_exist())

        return "\n".join(filter(None, results))

    def _restart_microsoft_pc_manager_service(self):
        service_name = self._MICROSOFT_PC_MANAGER_SERVICE_NAME
        results = [f"--- {service_name} ---"]
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            # Service is Running
            if status == win32service.SERVICE_RUNNING:
                stop_svc_cmd = ["sc.exe", "stop", service_name]
                start_svc_cmd = ["sc.exe", "start", service_name]
                stop_result = subprocess.run(stop_svc_cmd, capture_output=True, text=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
                # Error Occurred While Stopping the Service
                if stop_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {stop_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {stop_result.stderr}")
                # Wait for the Service to Stop
                for _ in range(30):  # Wait Up to 30 Seconds
                    time.sleep(1)
                    status = win32serviceutil.QueryServiceStatus(service_name)[1]
                    if status == win32service.SERVICE_STOPPED:
                        results.append(self.translator.translate("microsoft_pc_manager_service_has_been_stopped"))
                        break
                else:
                    return self.translator.translate("microsoft_pc_manager_service_stop_timeout")
                start_result = subprocess.run(start_svc_cmd, capture_output=True, text=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
                results.append(self.translator.translate("microsoft_pc_manager_service_has_been_restarted"))
                # Error Occurred While Starting the Service
                if start_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {stop_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {stop_result.stderr}")
            # Service is Stopped
            elif status == win32service.SERVICE_STOPPED:
                start_svc_cmd = ["sc.exe", "start", service_name]
                start_result = subprocess.run(start_svc_cmd, capture_output=True, text=True, check=False)
                results.append(self.translator.translate("microsoft_pc_manager_service_has_been_started"))
                # Error Occurred While Starting the Service
                if start_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {start_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {start_result.stderr}")
            # Service is in an Unknown State
            else:
                results.append(f"{self.translator.translate('the_current_state_of_the_service')}: {status}")
        except Exception as e:
            return (f"{self.translator.translate('exception_context')}: {e}\n"
                    f"error_code: {self.error_code}\n"
                    f"error_message: {self.error_message}")
        return "\n".join(results)

    def _restart_microsoft_pc_manager_service_beta(self):
        service_name = self._MICROSOFT_PC_MANAGER_BETA_SERVICE_NAME
        results = [f"--- {service_name} ---"]
        try:
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            # Service is Running
            if status == win32service.SERVICE_RUNNING:
                stop_svc_cmd = ["sc.exe", "stop", service_name]
                start_svc_cmd = ["sc.exe", "start", service_name]
                stop_result = subprocess.run(stop_svc_cmd, capture_output=True, text=True, check=False)
                # Error Occurred While Stopping the Service
                if stop_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {stop_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {stop_result.stderr}")
                # Wait for the Service to Stop
                for _ in range(30):  # Wait Up to 30 Seconds
                    time.sleep(1)
                    status = win32serviceutil.QueryServiceStatus(service_name)[1]
                    if status == win32service.SERVICE_STOPPED:
                        results.append(self.translator.translate("microsoft_pc_manager_beta_service_has_been_stopped"))
                        break
                else:
                    return self.translator.translate("microsoft_pc_manager_beta_service_stop_timeout")
                start_result = subprocess.run(start_svc_cmd, capture_output=True, text=True, check=False)
                results.append(self.translator.translate("microsoft_pc_manager_beta_service_has_been_started"))
                # Error Occurred While Starting the Service
                if start_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {stop_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {stop_result.stderr}")
            # Service is Stopped
            elif status == win32service.SERVICE_STOPPED:
                start_svc_cmd = ["sc.exe", "start", service_name]
                start_result = subprocess.run(start_svc_cmd, capture_output=True, text=True, check=False)
                results.append(self.translator.translate("microsoft_pc_manager_beta_service_has_been_restarted"))
                # Error Occurred While Starting the Service
                if start_result.returncode != 0:
                    return (f"{self.translator.translate('an_error_occurred_when_operating_the_service')}\n"
                            f"{self.translator.translate('stdout')}: {start_result.stdout}\n"
                            f"{self.translator.translate('stderr')}: {start_result.stderr}")
            # Service is in an Unknown State
            else:
                results.append(f"{self.translator.translate('the_current_state_of_the_service')}: {status}")
        except Exception as e:
            return (f"{self.translator.translate('exception_context')}: {e}\n"
                    f"error_code: {self.error_code}\n"
                    f"error_message: {self.error_message}")
        return "\n".join(results)

    def _microsoft_pc_manager_service_not_exist(self):
        return self.translator.translate("microsoft_pc_manager_service_is_not_installed")
