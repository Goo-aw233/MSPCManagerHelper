import hashlib
import os
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

import requests

from core import (
    AppMetadata,
    AppResources
)


class FetchResource:
    DEFAULT_USER_AGENT = (
        f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0 "
        f"MSPCManagerHelper/{AppMetadata.APP_VERSION_WITHOUT_SPACES}"
    )
    WINDOWS_INVALID_CHARS = re.compile(r'[<>:"/\\|?*]')

    @staticmethod
    def fetch(
        url,
        download_dir=None,
        filename=None,
        timeout=(15, 60),
        user_agent=DEFAULT_USER_AGENT,
        progress_callback=None,
        save_sha256=False,
    ):
        """
        USAGE EXAMPLE:
        fetch(
            url="https://example.com/file.zip",
            download_dir="C:\\Downloads",
            filename="custom_name.zip",
            timeout=(10, 30),
            user_agent="CustomUserAgent/1.0",
            progress_callback=FetchResource.throttled_progress(self._log),
            save_sha256=True
        )

        ARGS:
            url: URL to Fetch
            download_dir: Directory to Download the File (Optional)
            filename: Filename to Save As (Optional)
            timeout: Connect/Read Timeout in Seconds (Optional, Default: (15, 60))
            user_agent: User-Agent Header Value (Optional, Default: Built-in User-Agent)
            progress_callback: Return Progress Once for Each Chunk Processed (Optional)
            save_sha256: Compute SHA256 & Save to <file>.sha256 (Optional)
        """
        download_dir = FetchResource._get_download_dir(download_dir)
        user_agent = FetchResource._get_user_agent(user_agent)

        response = requests.get(
            url,
            stream=True,
            timeout=timeout,
            headers={"User-Agent": user_agent},
        )
        response.raise_for_status()

        filename = FetchResource._get_filename(filename, response, download_dir)
        file_path = Path(download_dir) / filename
        part_path = Path(str(file_path) + ".part")

        total_bytes = response.headers.get("Content-Length")
        if total_bytes is not None:
            total_bytes = int(total_bytes)

        # Set Filename Attribute for Display if progress_callback is Provided
        if progress_callback is not None:
            progress_callback._filename = filename

        bytes_read = 0
        try:
            with open(part_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bytes_read += len(chunk)
                    if progress_callback:
                        progress_callback(bytes_read, total_bytes)
        except BaseException:
            part_path.unlink(missing_ok=True)
            raise

        os.replace(part_path, file_path)

        if save_sha256:
            sha256_path = Path(str(file_path) + ".sha256")
            sha256_hash = FetchResource.compute_sha256(file_path)
            tmp_sha256_path = Path(str(sha256_path) + ".tmp")
            with open(tmp_sha256_path, "w", encoding="utf-8") as f:
                f.write(sha256_hash)
            os.replace(tmp_sha256_path, sha256_path)

        return file_path

    @staticmethod
    def _get_download_dir(download_dir=None):
        if download_dir:
            return download_dir
        return AppResources.app_temp_dir()

    @staticmethod
    def _get_user_agent(user_agent=None):
        if user_agent:
            return user_agent
        return FetchResource.DEFAULT_USER_AGENT

    @staticmethod
    def _get_filename(filename=None, response=None, download_dir=None):
        if not filename:
            filename = FetchResource._parse_content_disposition(response)
        if not filename:
            # E.g., 1970-01-01T00.00.00 (ISO 8601)
            date_part = datetime.now().replace(microsecond=0).isoformat().replace(':', '.')
            filename = f"download_{date_part}_{time.time_ns()}"

        filename = FetchResource._sanitize_filename(filename)

        if download_dir:
            filename = FetchResource._deduplicate_filename(filename, download_dir)
        return filename

    @staticmethod
    def _parse_content_disposition(response):
        # Extract Filename from Content-Disposition (RFC 5987 / RFC 6266)
        if response is None:
            return None
        header = response.headers.get("Content-Disposition", "")
        if not header:
            return None
        # RFC 5987: filename*=UTF-8''encoded-name
        match = re.search(r"filename\*\s*=\s*(?:UTF-8''|utf-8'')([^;]+)", header, re.IGNORECASE)
        if match:
            return unquote(match.group(1).strip().strip('"'))
        # RFC 6266: filename="name"
        match = re.search(r'filename\s*=\s*"([^"]+)"', header, re.IGNORECASE)
        if match:
            return match.group(1)
        # Bare: filename=name
        match = re.search(r"filename\s*=\s*([^;]+)", header, re.IGNORECASE)
        if match:
            return match.group(1).strip().strip('"')
        return None

    @staticmethod
    def _deduplicate_filename(filename, download_dir):
        filename_path = Path(filename)
        base = filename_path.stem
        ext = filename_path.suffix
        candidate = filename
        counter = 1
        while (Path(download_dir) / candidate).exists():
            candidate = f"{base}_({counter}){ext}"
            counter += 1
        return candidate

    @staticmethod
    def _sanitize_filename(filename):
        # Discard any directory components via `Path.name`, then replace `< > : " / \\ | ? *` with `_`.
        sanitized = Path(filename).name
        sanitized = FetchResource.WINDOWS_INVALID_CHARS.sub("_", str(sanitized))
        return sanitized or "download"

    @staticmethod
    def throttled_progress(log_func):
        # Pre-fetch EventsTextbox instance and CTkTextbox widget (via __self__ chain).
        # Note: This chain depends on the structure of the log_func instance passed by the caller.
        _events_textbox = log_func.__self__.log_callback.__self__
        _textbox_widget = _events_textbox.textbox

        def _update_textbox(text):
            _textbox_widget.configure(state="normal")
            # Search Backward from Last Line for a Line with Existing Progress
            # (Number + Storage Units, E.g. 123.4 MB or 56.7%)
            line_count = int(_textbox_widget.index("end-1c").split(".")[0])
            for ln in range(line_count, 0, -1):
                line_content = _textbox_widget.get(f"{ln}.0", f"{ln}.end")
                if re.search(r'\d+(\.\d+)?\s*(B|KB|MB|GB|%)\s', line_content):
                    _textbox_widget.delete(f"{ln}.0", f"{ln}.end")
                    _textbox_widget.insert(f"{ln}.0", text)
                    break
            else:
                # Append to End if No Existing Progress Line Found
                _textbox_widget.insert("end", text if text.endswith("\n") else text + "\n")
            _textbox_widget.see("end")
            _textbox_widget.configure(state="disabled")

        def _textbox(text):
            # Schedule Update on Main Thread to Avoid Tkinter Threading Issues
            _textbox_widget.after(0, _update_textbox, text)

        def _fmt(b: float) -> str:
            _GB = 1 << 30
            _MB = 1 << 20
            _KB = 1 << 10
            if b >= _GB:
                return f"{b / _GB:.1f} GB"
            if b >= _MB:
                return f"{b / _MB:.1f} MB"
            if b >= _KB:
                return f"{b / _KB:.1f} KB"
            return f"{b} B"

        _state = {"last_pct": -1, "last_at": 0.0, "last_bytes": 0, "interval": 0.5}

        def _tick(now, bytes_read):
            # Record tick time & bytes, return instant speed in bytes/s.
            elapsed = now - _state["last_at"]
            speed_bytes = 0
            if _state["last_at"] > 0 and elapsed > 0:
                speed_bytes = (bytes_read - _state["last_bytes"]) / elapsed
            _state["last_at"] = now
            _state["last_bytes"] = bytes_read
            return speed_bytes

        def _bar(pct):
            w = 20
            filled = w * pct // 100
            return f"[{'█' * filled}{'░' * (w - filled)}]"

        def _cb(bytes_read, total_bytes):
            prefix = f"{_cb._filename}: " if _cb._filename else ""
            now = time.time()

            if total_bytes:
                pct = bytes_read * 100 // total_bytes
                if pct == _state["last_pct"] and now - _state["last_at"] < _state["interval"]:
                    return
                _state["last_pct"] = pct

                speed = _tick(now, bytes_read)
                speed_str = f" @ {_fmt(speed)}/s" if speed > 0 else ""
                _textbox(
                    f"{prefix}{_bar(pct)} {_fmt(bytes_read)} / {_fmt(total_bytes)} ({pct}%){speed_str}"
                )
            else:
                if now - _state["last_at"] < _state["interval"]:
                    return

                speed = _tick(now, bytes_read)
                speed_str = f" @ {_fmt(speed)}/s" if speed > 0 else ""
                _textbox(f"{prefix}{_fmt(bytes_read)}{speed_str}")

        _cb._filename = None
        return _cb

    @staticmethod
    def compute_sha256(file_path):
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
