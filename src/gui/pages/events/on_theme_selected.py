def on_theme_selected(theme_var, theme_mode_map, logger, winfo_toplevel):
    selected = theme_var.get()
    mode = theme_mode_map.get(selected, "auto")

    try:
        from core.program_settings import ProgramSettings
        ProgramSettings.set_theme_mode(mode)
        ProgramSettings.apply_theme()
        logger.info(f"Theme Mode Switched to: {mode}")
        # Refresh the main window UI to apply the new theme.
        main_window = winfo_toplevel()
        if hasattr(main_window, "refresh_ui"):
            main_window.refresh_ui()
    except Exception as e:
        logger.exception(f"Failed to Switch Theme: {e}")
