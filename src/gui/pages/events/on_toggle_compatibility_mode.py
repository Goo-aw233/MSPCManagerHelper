def on_toggle_compatibility_mode(ProgramSettings, compatibility_mode_var, logger):
    try:
        new_state = compatibility_mode_var.get()
        ProgramSettings.set_compatibility_mode_enabled(new_state)
        logger.info(f"Compatibility Mode Setting Set to: {new_state}")
    except Exception as e:
        logger.exception(f"Failed to Set Compatibility Mode: {e}")
