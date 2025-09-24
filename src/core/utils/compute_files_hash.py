import ctypes
import hashlib
from tkinter import filedialog


class ComputeFilesHash:

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()

    def _select_the_files_to_compute(self):
        return filedialog.askopenfilenames(title=self.translator.translate("select_the_files_to_compute"), filetypes=[(self.translator.translate("all_file_types"), "*.*")])

    def compute_files_hash(self, selected_algorithms):
        files_to_compute = self._select_the_files_to_compute()
        if not files_to_compute:
            return self.translator.translate("user_has_canceled_the_task")

        if not any(selected_algorithms.values()):
            return self.translator.translate("no_files_selected")

        all_results = []
        for file_path in files_to_compute:
            try:
                with open(file_path, "rb") as f:
                    data = f.read()

                computation_result = [f"{self.translator.translate("file_path")}: {file_path}"]
                
                hash_functions = {
                    'md5': lambda d: hashlib.md5(d).hexdigest(),
                    'sha1': lambda d: hashlib.sha1(d).hexdigest(),
                    'sha224': lambda d: hashlib.sha224(d).hexdigest(),
                    'sha256': lambda d: hashlib.sha256(d).hexdigest(),
                    'sha384': lambda d: hashlib.sha384(d).hexdigest(),
                    'sha512': lambda d: hashlib.sha512(d).hexdigest(),
                    'blake2b': lambda d: hashlib.blake2b(d).hexdigest(),
                    'blake2s': lambda d: hashlib.blake2s(d).hexdigest(),
                    'sha3_224': lambda d: hashlib.sha3_224(d).hexdigest(),
                    'sha3_256': lambda d: hashlib.sha3_256(d).hexdigest(),
                    'sha3_384': lambda d: hashlib.sha3_384(d).hexdigest(),
                    'sha3_512': lambda d: hashlib.sha3_512(d).hexdigest(),
                    'shake_128': lambda d: hashlib.shake_128(d).hexdigest(32),
                    'shake_256': lambda d: hashlib.shake_256(d).hexdigest(64)
                }

                for algo_key, is_selected in selected_algorithms.items():
                    if is_selected:
                        algo_name = algo_key.upper().replace("_", "-")
                        hash_value = hash_functions[algo_key](data)
                        computation_result.append(f"{algo_name}: {hash_value}")
                
                all_results.append("\n".join(computation_result))

            except Exception as e:
                all_results.append(f"{self.translator.translate('failed_to_compute_hash_for')}: {file_path}\n"
                                   f"{self.translator.translate('exception_context')}: {e}")

        all_results.append(f"\n{self.translator.translate('all_file_hashes_have_been_computed')}")
        return "\n\n".join(all_results)
