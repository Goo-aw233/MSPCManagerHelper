def on_toggle_support_developer(ProgramSettings, support_developer_var, logger):
    try:
        new_state = support_developer_var.get()
        ProgramSettings.set_support_developer_enabled(new_state)
        logger.info(f"Support Developer Setting Set to: {new_state}")
    except Exception as e:
        logger.exception(f"Failed to Set Support Developer: {e}")
