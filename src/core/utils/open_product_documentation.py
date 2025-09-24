import ctypes
import webbrowser


class OpenProductDocumentation:

    def __init__(self, translator=None):
        self.translator = translator
        self.error_code = ctypes.get_last_error()
        self.error_message = ctypes.FormatError(self.error_code).strip()   

    def open_product_documentation(self):
        try:
            webbrowser.open("https://mspcmanager.github.io/mspcm-docs")
            return self.translator.translate("product_documentation_opened_successfully")
        except Exception as e:
            self.error_code = ctypes.get_last_error()
            self.error_message = ctypes.FormatError(self.error_code).strip()
            error_info = (f"{self.translator.translate('exception_context')}: {e}\n"
                          f"{self.translator.translate('error_code')}: {self.error_code}\n"
                          f"{self.translator.translate('error_message')}: {self.error_message}")
            return f"{self.translator.translate('an_error_occurred_when_opening_the_documentation')}\n{error_info}"
