def get_localization_translators(translator):
    translations = getattr(translator, "translations", {})
    if not isinstance(translations, dict):
        return []

    metadata = translations.get("metadata")
    translator_list = None
    if isinstance(metadata, dict):
        translator_list = metadata.get("__localization_translator_list__")
        if not isinstance(translator_list, dict):
            translator_list = None

    if translator_list is not None:
        translator_list_result = []
        for key, display_name in translator_list.items():
            if key.startswith("__"):
                continue
            translator_list_result.append((key, display_name))
        return translator_list_result

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
