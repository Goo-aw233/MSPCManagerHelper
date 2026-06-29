import re
from pathlib import Path
from urllib.parse import unquote

import requests

from core.app_resources import AppResources


class FetchResource:
    """
    USAGE EXAMPLE:
    fetch("https://example.com/file.zip", download_dir=r"C:\Downloads", filename="custom_name.zip")
    ARGS:
        url: URL to Fetch
        download_dir: Directory to Download the File (Optional)
        filename: Filename to Save As (Optional)
        timeout: Connect/Read Timeout in Seconds (Optional, Default: (15, 60))
    """
    @staticmethod
    def fetch(url, download_dir=None, filename=None, timeout=(15, 60)):
        if download_dir is None:
            download_dir = AppResources.app_temp_dir()

        download_path = Path(download_dir)
        download_path.mkdir(parents=True, exist_ok=True)

        resp = requests.get(url, stream=True, timeout=timeout)
        resp.raise_for_status()

        is_default_name = False

        # Determine filename from Content-Disposition header if not provided.
        if filename is None:
            cd = resp.headers.get("Content-Disposition")
            if cd:
                # Handle RFC 5987 encoded filename* format.
                rfc_match = re.search(
                    r"filename\*=(?:[^;]+)''([^;\s]+)",
                    cd,
                    re.IGNORECASE,
                )
                if rfc_match:
                    filename = unquote(rfc_match.group(1).strip())
                else:
                    # Fallback to standard filename format.
                    fallback_match = re.search(
                        r"""filename\s*=\s*["']?([^"';]+)["']?""",
                        cd,
                        re.IGNORECASE,
                    )
                    if fallback_match:
                        filename = fallback_match.group(1).strip()

            # Use default cache filename if no filename could be determined.
            if filename is None:
                is_default_name = True
                num = 1
                while True:
                    candidate = f"CacheFile_{num}"
                    if not (download_path / candidate).exists():
                        filename = candidate
                        break
                    num += 1

        # Filter out illegal characters in Windows filenames.
        filename = FetchResource._sanitize_filename(filename)

        file_path = download_path / filename

        # File already exists, automatically handle naming conflicts.
        if file_path.exists():
            if is_default_name:
                # Default filename continues to increment numbering.
                stem = file_path.stem
                match = re.match(r"CacheFile_(\d+)", stem)
                if match:
                    num = int(match.group(1)) + 1
                    while True:
                        candidate = f"CacheFile_{num}"
                        if not (download_path / candidate).exists():
                            file_path = download_path / candidate
                            break
                        num += 1
            else:
                # Other filenames have (num) added before the extension.
                stem = file_path.stem
                suffix = file_path.suffix
                num = 1
                while True:
                    new_name = f"{stem}({num}){suffix}"
                    new_path = download_path / new_name
                    if not new_path.exists():
                        file_path = new_path
                        break
                    num += 1

        # Stream write file.
        with open(file_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return str(file_path)

    @staticmethod
    def _sanitize_filename(name):
        # Filter out illegal characters in Windows filenames
        # and replace them with underscores.
        illegal_chars = set(r"\/:*?\"<>|")
        return "".join(c if c not in illegal_chars else "_" for c in name)
