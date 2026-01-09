def get_localization_translators(translator):
    translations = getattr(translator, "translations", {})
    if not isinstance(translations, dict):
        return []

    keys = list(translations.keys())
    try:
        start_index = keys.index("__localization_translator_list__") + 1
        end_index = keys.index("__localization_translator_list_end__")
    except ValueError:
        return []

    translator_list_result = []
    for key in keys[start_index:end_index]:
        if key.startswith("__"):
            continue
        display_name = translations.get(key, key)
        translator_list_result.append((key, display_name))
    return translator_list_result
