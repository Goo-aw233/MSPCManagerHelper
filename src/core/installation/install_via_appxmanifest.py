import ctypes
import subprocess
from tkinter import filedialog


class InstallViaAppxManifest:

    def __init__(self):
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()
