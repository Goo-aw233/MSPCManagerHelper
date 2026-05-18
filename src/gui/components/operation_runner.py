import threading


class OperationRunner:
    @staticmethod
    def run(page_instance, operation_func, operation_name_key, on_completion=None):
        page_instance.tabview.set(page_instance.events_tab_name)
        operation_name = page_instance.app_translator.translate(operation_name_key)
        message = (
            page_instance.app_translator.translate("pages.common.executing_operation").format(operation_name=operation_name) + "\n" +
            page_instance.app_translator.translate("pages.common.executing_operation_prompt") + "\n"
        )
        page_instance.logger.info(f"Executing Operation: {operation_name}")

        # Reset Events Textbox on Main Thread
        page_instance.events_textbox.clear_events()

        # Append Initial Message Directly or via log_to_events
        page_instance.events_textbox.log_to_events(message)

        def _thread_target():
            try:
                operation_func()
                page_instance.events_textbox.log_to_events(
                    page_instance.app_translator.translate("pages.common.completed_operation").format(operation_name=operation_name))
                page_instance.logger.info(f"Completed Operation: {operation_name}")
            except Exception as e:
                page_instance.logger.error(f"Error Executing {operation_name}: {e}")
                page_instance.events_textbox.log_to_events(f"Error: {e}")
            finally:
                if on_completion:
                    page_instance.after(0, on_completion)

        threading.Thread(target=_thread_target, daemon=True).start()
