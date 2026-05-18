import win32service
import win32serviceutil


class RestartServices:
    def __init__(self, logger, app_translator, log_callback, selected_services):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.selected_services = selected_services

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        self.logger.debug(f"Selected Services: {self.selected_services}")
        if self.selected_services.get("stable_version"):
            self._pcm_svc_store()

        if self.selected_services.get("beta_version"):
            self._pcm_svc_beta()

        if self.selected_services.get("store_beta_version"):
            self._pcm_svc_store_beta()

    def _manage_service(self, service_name):
        try:
            try:
                status = win32serviceutil.QueryServiceStatus(service_name)[1]
                self._log(
                    self.app_translator.translate("modules.utilities.service_status").format(
                        service_name=service_name,
                        status=(
                            self.app_translator.translate("modules.utilities.running_service")
                            if status == win32service.SERVICE_RUNNING
                            else self.app_translator.translate("modules.utilities.stopped_service")
                        )
                    )
                )
                self.logger.info(
                f"{service_name} Service Status: "
                f"{'Service is running.' if status == win32service.SERVICE_RUNNING else 'Service has stopped.'}"
                )
            except Exception as e:
                self._log(
                    self.app_translator.translate("modules.utilities.service_not_found_or_inaccessible").format(
                        service_name=service_name, error=str(e)
                    )
                )
                self.logger.warning(f"Service {service_name} Not Found or Inaccessible: {e}")
                return

            # Stop Service
            if status == win32service.SERVICE_RUNNING:
                self._log(
                    self.app_translator.translate("modules.utilities.stopping_service").format(
                        service_name=service_name
                    )
                )
                self.logger.info(f"Stopping Service: {service_name}")
                win32serviceutil.StopService(service_name)
                win32serviceutil.WaitForServiceStatus(service_name, win32service.SERVICE_STOPPED, 10)
                self._log(self.app_translator.translate("modules.utilities.stopped_service"))
                self.logger.info("Service has stopped.")

            # Start Service
            self._log(
                self.app_translator.translate("modules.utilities.starting_service").format(
                    service_name=service_name
                )
            )
            self.logger.info(f"Starting Service: {service_name}")
            win32serviceutil.StartService(service_name)
            win32serviceutil.WaitForServiceStatus(service_name, win32service.SERVICE_RUNNING, 10)
            self._log(self.app_translator.translate("modules.utilities.started_service").format(service_name=service_name))
            self.logger.info("Service has started.")

            # Check Final Status
            status = win32serviceutil.QueryServiceStatus(service_name)[1]
            self._log(self.app_translator.translate("modules.utilities.service_status").format(
                service_name=service_name,
                status=(self.app_translator.translate("modules.utilities.running_service")
                        if status == win32service.SERVICE_RUNNING
                        else self.app_translator.translate("modules.utilities.stopped_service")
                    )
                )
            )
            self.logger.info(
                f"{service_name} Service Status: "
                f"{'Service is running.' if status == win32service.SERVICE_RUNNING else 'Service has stopped.'}"
            )
        except Exception as e:
            self._log(self.app_translator.translate("modules.utilities.manage_service_error").format(
                service_name=service_name, error=str(e)
                )
            )
            self.logger.error(f"An Error Occurred While Managing Service {service_name}: {str(e)}")

    def _pcm_svc_store(self):
        self._manage_service("PCManager Service Store")

    def _pcm_svc_beta(self):
        self._manage_service("PCManager Service")

    def _pcm_svc_store_beta(self):
        self._manage_service("PC Manager Service")
