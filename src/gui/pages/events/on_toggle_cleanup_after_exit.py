def on_toggle_cleanup_after_exit(ProgramSettings, cleanup_after_exit_var, logger):
    try:
        new_state = cleanup_after_exit_var.get()
        ProgramSettings.set_cleanup_after_exit_enabled(new_state)
        logger.info(f"Cleanup After Exit Setting Set to: {new_state}")
    except Exception as e:
        logger.exception(f"Failed to Set Cleanup After Exit: {e}")
