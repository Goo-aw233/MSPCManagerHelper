import re
from pathlib import Path


class OrganizeFilePaths:
    @staticmethod
    def split_paths(paths):
        # Empty
        if not paths:
            return []

        # Split Paths By Delimiter
        if isinstance(paths, (list, tuple, set)):
            raw_paths = list(paths)
        else:
            raw_paths = str(paths).split("|")

        result = []
        for path in raw_paths:
            stripped = str(path).strip()
            if stripped:
                result.append(stripped)

        return result

    @staticmethod
    def _strip_invisible_chars(text):
        """
        Naming Files, Paths, and Namespaces:
        https://learn.microsoft.com/windows/win32/fileio/naming-a-file
        """
        return re.sub(r"[\x00-\x1F]", "", text)

    @staticmethod
    def clean_paths(paths):
        cleaned_paths = []
        for path in OrganizeFilePaths.split_paths(paths):
            # Remove Leading & Trailing Spaces & Quotes
            cleaned_path = Path(
                path.strip().strip('"').strip("'")
            )

            # If path does NOT exist, strip control characters.
            # (\\x00-\\x1F) forbidden by Windows in file names.
            if not cleaned_path.exists():
                cleaned_path = Path(
                    OrganizeFilePaths._strip_invisible_chars(
                        str(cleaned_path)
                    ).strip()
                )

            # Convert to Absolute Path
            if str(cleaned_path).strip():
                cleaned_paths.append(str(cleaned_path.resolve()))

        return cleaned_paths
