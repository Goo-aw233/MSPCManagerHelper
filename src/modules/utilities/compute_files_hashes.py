import hashlib
import tkinter.filedialog


class ComputeFilesHashes:
    def __init__(self, logger, app_translator, log_file_path, log_callback, selected_algos):
        self.logger = logger
        self.app_translator = app_translator
        self.log_file_path = log_file_path
        self.log_callback = log_callback
        self.selected_algos = selected_algos

    def _log(self, message):
        if self.log_callback:
            self.log_callback(message)

    def execute(self):
        files = self.select_files()
        if not files:
            return self._log(self.app_translator.translate("user_has_canceled_the_operation"))
        return self.compute(files)

    def select_files(self):
        return tkinter.filedialog.askopenfilenames(
            title=self.app_translator.translate("select_files"),
            filetypes=[("*", "*.*")]
        )

    def compute(self, files):
        if not self.selected_algos:
            return

        for file_path in files:
            output_lines = [
                "=" * 30,
                f"{self.app_translator.translate('path_to_compute_hashes_file')}:",
                f"  {file_path}",
                "-" * 15
            ]

            for algo in self.selected_algos:
                res = self._compute_hash(file_path, algo)
                # Use tab character which aligns with the configured tab stops in the GUI.
                output_lines.append(f"  [{algo.upper()}]\t {res}")

            output_lines.append("=" * 30)
            output_lines.append("")
            self._log("\n".join(output_lines))

    @staticmethod
    def _compute_hash(file_path, algo_name):
        try:
            if algo_name.startswith("shake_"):
                h = getattr(hashlib, algo_name)()
            else:
                if hasattr(hashlib, algo_name):
                    h = getattr(hashlib, algo_name)()
                else:
                    h = hashlib.new(algo_name)

            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)

            if algo_name.startswith("shake_"):
                return h.hexdigest(32)  # Type: Ignore
            return h.hexdigest()
        except Exception as e:
            return str(e)
