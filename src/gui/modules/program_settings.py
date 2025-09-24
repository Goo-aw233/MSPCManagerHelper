class ProgramSettings:
    _is_support_developer_enabled: bool = True
    _is_compatibility_mode_enabled: bool = False
    # TIPS: This should have been null, but it was problematic, so the id has been added.
    microsoft_student_ambassadors_cid: str = "?wt.mc_id=studentamb_265231"

    @classmethod
    def is_support_developer_enabled(cls) -> bool:
        return cls._is_support_developer_enabled

    @classmethod
    def toggle_support_developer(cls):
        cls._is_support_developer_enabled = not cls._is_support_developer_enabled

        cls.microsoft_student_ambassadors_cid = ""
        if cls._is_support_developer_enabled:
            cls.microsoft_student_ambassadors_cid = "?wt.mc_id=studentamb_265231"

    @classmethod
    def is_compatibility_mode_enabled(cls) -> bool:
        return cls._is_compatibility_mode_enabled

    @classmethod
    def toggle_compatibility_mode(cls):
        cls._is_compatibility_mode_enabled = not cls._is_compatibility_mode_enabled
