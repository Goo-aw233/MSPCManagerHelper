import re
import subprocess
from pathlib import Path

from core import PathResolver


class UninstallEdgeComponents:
    _COMPONENTS = {
        "edge": {
            "dir_name": "Edge",
            "msedge_switch": "--msedge",
            "component_label": "Microsoft Edge",
            "key_prefix": "edge",
        },
        "webview2": {
            "dir_name": "EdgeWebView",
            "msedge_switch": "--msedgewebview",
            "component_label": "Microsoft Edge WebView2 Runtime",
            "key_prefix": "webview2",
        },
    }

    @staticmethod
    def _version_key(version_dir_name):
        return [int(p) for p in re.findall(r"\d+", version_dir_name)]

    @staticmethod
    def _find_latest_setup(base_dir):
        app_dir = Path(base_dir) / "Application"
        if not app_dir.is_dir():
            return None, []
        # Only treat folders whose name contains a version as version dirs.
        version_dirs = [d for d in app_dir.iterdir()
                        if d.is_dir() and UninstallEdgeComponents._version_key(d.name)]
        if not version_dirs:
            return None, []
        latest = max(version_dirs, key=lambda d: UninstallEdgeComponents._version_key(d.name))
        setup_exe = latest / "Installer" / "setup.exe"
        return (str(setup_exe) if setup_exe.is_file() else None), version_dirs

    @staticmethod
    def _find_latest_setup_exe(base_dir):
        setup_exe, _ = UninstallEdgeComponents._find_latest_setup(base_dir)
        return setup_exe

    @staticmethod
    def is_edge_available():
        base = PathResolver.program_files_x86() / "Microsoft" / "Edge"
        return UninstallEdgeComponents._find_latest_setup_exe(base) is not None

    @staticmethod
    def is_webview2_available():
        base = PathResolver.program_files_x86() / "Microsoft" / "EdgeWebView"
        return UninstallEdgeComponents._find_latest_setup_exe(base) is not None

    @staticmethod
    def _find_edgeupdate_path():
        local_app_data = PathResolver.local_app_data()
        candidates = [
            local_app_data / "Microsoft" / "EdgeUpdate" / "MicrosoftEdgeUpdate.exe",
            PathResolver.program_files_x86() / "Microsoft" / "EdgeUpdate" / "MicrosoftEdgeUpdate.exe",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return None

    @staticmethod
    def is_edgeupdate_available():
        return UninstallEdgeComponents._find_edgeupdate_path() is not None

    def __init__(self, logger, app_translator, log_callback, force_uninstall=False, uninstall_edge=False,
                 uninstall_webview2=False, uninstall_edgeupdate=False):
        self.logger = logger
        self.app_translator = app_translator
        self.log_callback = log_callback
        self.force_uninstall = force_uninstall
        self.uninstall_edge = uninstall_edge
        self.uninstall_webview2 = uninstall_webview2
        self.uninstall_edgeupdate = uninstall_edgeupdate

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    @staticmethod
    def _format_error_output(app_translator, stdout_text, stderr_text, use_localized=True, returncode=None):
        stdout_label = app_translator.translate(
            "common.stdout") if use_localized else "Stdout"
        stderr_label = app_translator.translate(
            "common.stderr") if use_localized else "Stderr"
        return_code_label = app_translator.translate(
            "common.return_code") if use_localized else "Return Code"
        parts = []
        if returncode is not None:
            parts.append(f"{return_code_label}: {returncode}")
        if stdout_text:
            parts.append(f"{stdout_label}:\n{stdout_text}")
        if stderr_text:
            if parts:
                parts.append("---")
            parts.append(f"{stderr_label}:\n{stderr_text}")
        return "\n".join(parts)

    def execute(self):
        self.logger.debug(
            f"Uninstall Edge Components Options - Force Uninstall: {self.force_uninstall}, Edge: {self.uninstall_edge}, "
            f"WebView2: {self.uninstall_webview2}, EdgeUpdate: {self.uninstall_edgeupdate}")
        if self.uninstall_edge:
            self._uninstall_edge()
        if self.uninstall_webview2:
            self._uninstall_webview2()
        if self.uninstall_edgeupdate:
            self._uninstall_edgeupdate()

    def _uninstall_edge(self):
        # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{56EB18F8-B008-4CBD-B6D2-8C97FE7E9062}
        # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge
        self._uninstall_component("edge")

    def _uninstall_webview2(self):
        # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}
        # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft EdgeWebView
        self._uninstall_component("webview2")

    def _uninstall_edgeupdate(self):
        # HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate
        edgeupdate_path = UninstallEdgeComponents._find_edgeupdate_path()
        if edgeupdate_path is None:
            self._log(self.app_translator.translate("modules.uninstaller.edgeupdate_not_found"))
            self.logger.warning("MicrosoftEdgeUpdate.exe was not found.")
            return

        self._log(self.app_translator.translate("modules.uninstaller.uninstalling_edgeupdate"))
        cmd = [str(edgeupdate_path), "/uninstall"]
        self.logger.info(
            f"Running Microsoft EdgeUpdate. "
            f"Command: {' '.join(cmd)}"
        )
        try:
            result = subprocess.run(
                cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(self.app_translator.translate("modules.uninstaller.edgeupdate_uninstall_error").format(
                error=str(e)))
            self.logger.error(f"An Error Occurred While Uninstalling Microsoft EdgeUpdate: {e}")
            return

        if result.returncode == 0:
            self._log(self.app_translator.translate("modules.uninstaller.edgeupdate_uninstall_successfully"))
            return

        error_output = self._format_error_output(
            self.app_translator, result.stdout, result.stderr, returncode=result.returncode)
        self._log(self.app_translator.translate("modules.uninstaller.edgeupdate_uninstall_error").format(
            error=error_output))
        self.logger.error(
            f"An Error Occurred While Uninstalling Microsoft EdgeUpdate:\n"
            + self._format_error_output(
                self.app_translator, result.stdout, result.stderr,
                use_localized=False, returncode=result.returncode))

    def _uninstall_component(self, component):
        cfg = UninstallEdgeComponents._COMPONENTS[component]
        key_prefix = cfg["key_prefix"]

        base_dir = PathResolver.program_files_x86() / "Microsoft" / cfg["dir_name"]
        setup_exe, version_dirs = UninstallEdgeComponents._find_latest_setup(base_dir)
        if setup_exe is None:
            self._log(self.app_translator.translate(f"modules.uninstaller.{key_prefix}_not_found"))
            self.logger.warning(f"{cfg['component_label']} setup.exe was not found.")
            return

        # If multiple versions exist, first delete the old versions and wait for
        # the operation to complete, then uninstall the latest version.
        if len(version_dirs) > 1:
            self._log(self.app_translator.translate(f"modules.uninstaller.removing_old_{key_prefix}_versions"))
            # Only log the found versions when there are multiple; a single
            # version is the normal case and needs no announcement.
            versions = ", ".join(
                d.name for d in sorted(version_dirs, key=lambda d: UninstallEdgeComponents._version_key(d.name)))
            self.logger.info(f"Multiple {cfg['component_label']} Versions Found: {versions}")
            self._run_setup_exe(
                setup_exe,
                [cfg["msedge_switch"], "--delete-old-versions", "--system-level", "--verbose-logging"],
                cfg["component_label"],
                f"modules.uninstaller.{key_prefix}_uninstall_error",
            )

        self._log(self.app_translator.translate(f"modules.uninstaller.uninstalling_{key_prefix}"))
        uninstall_args = ["--uninstall", cfg["msedge_switch"], "--system-level", "--verbose-logging"]
        if self.force_uninstall:
            uninstall_args.insert(0, "--force-uninstall")
        if self._run_setup_exe(
                setup_exe, uninstall_args,
                cfg["component_label"],
                f"modules.uninstaller.{key_prefix}_uninstall_error"):
            self._log(self.app_translator.translate(f"modules.uninstaller.{key_prefix}_uninstall_successfully"))

    def _run_setup_exe(self, setup_exe, args, component_label, uninstall_error_key):
        cmd = [str(setup_exe), *args]
        self.logger.info(
            f"Running {component_label} Setup. "
            f"Command: {' '.join(cmd)}"
        )
        try:
            result = subprocess.run(
                cmd,
                check=False,
                shell=False,
                text=True,
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            self._log(self.app_translator.translate(uninstall_error_key).format(
                error=str(e)))
            self.logger.error(f"An Error Occurred While Uninstalling {component_label}: {e}")
            return False

        # 0 = success. 19 = uninstall completed, but setup.exe itself could not
        # delete its own file because it was still running (a reboot is needed
        # to finish cleanup); treat it as a successful uninstall.
        if result.returncode in (0, 19):
            if result.returncode == 19:
                self.logger.info(
                    f"{component_label} uninstall completed; a reboot may be required to finish cleanup.")
            return True

        self._log(
            self.app_translator.translate(uninstall_error_key).format(
                error=self._format_error_output(
                    self.app_translator, result.stdout, result.stderr, returncode=result.returncode
                )
            )
        )
        self.logger.error(
            f"An Error Occurred While Uninstalling {component_label}:\n"
            + self._format_error_output(
                self.app_translator, result.stdout, result.stderr,
                use_localized=False, returncode=result.returncode
            )
        )
        return False
