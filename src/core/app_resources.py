import sys
import tempfile
from pathlib import Path

from core.path_resolver import PathResolver


class ResourceLocator:
    """Data resource locator not associated with packaging/compilation methods.

    Probing-based Localization:
    1. Collect a batch of candidate roots that may contain resources (common packer placement points, the ancestor chain of the real path of __file__);
    2. Try each "<candidate root>/<relative path>" one by one, and if it physically exists on the disk, it is considered a hit;
    3. If all attempts fail, return None and let the caller degrade (fall back to default resources), without letting the localization logic throw an exception.

    According to Official Nuitka Documentation:
        - standalone: Data files are in the distribution directory and can be located using a relative path from __file__.
        - onefile: The main module's __file__ points to the temporary directory where the bootstrap is unpacked, and the data files included in the onefile are also there;
          this locator includes the original parent of the current module and the main module's __file__ as well as the resolved ancestor chain as candidates to cover.
    """

    _logger = None

    @classmethod
    def _get_logger(cls):
        if cls._logger is None:
            from core.app_logger import AppLogger
            cls._logger = AppLogger.get_logger()
        return cls._logger

    @classmethod
    def _candidate_roots(cls):
        roots = []  # (source_label, Path)
        seen = set()

        def add(label, p):
            try:
                p = p.resolve()
            except OSError:
                return
            if p not in seen:
                seen.add(p)
                roots.append((label, p))

        # 1) PyInstaller: Both onefile and onedir expose through sys._MEIPASS.
        meipass = getattr(sys, "_MEIPASS", None)
        if isinstance(meipass, str) and meipass:
            add("PyInstaller._MEIPASS", Path(meipass))

        # 2) cx_Freeze / Nuitka standalone / py2exe / other generic frozen:
        #    When the application is frozen, sys.frozen is True, but no _MEIPASS.
        #    resources and executable files are in the same directory.
        is_bundled = bool(getattr(sys, "frozen", False)) or (
            getattr(sys.modules.get("__main__", None), "__compiled__", None) is not None
        )
        if is_bundled:
            add("EXE_dir", Path(sys.executable).parent)
            add("argv0_dir", Path(sys.argv[0]).parent)

        # 3) Trace back to the parent directory of __file__, compatible with source code/onedir/standalone/onefile:
        #    Prefer using the __file__ path of __main__ (under onefile the __file__ of submodules is a pseudo path),
        #    otherwise use the __file__ path of the current module (__name__).
        for module in (sys.modules.get("__main__", None), sys.modules.get(__name__, None)):
            if module is None:
                continue

            # Get the source file path corresponding to the module (may be None for built-in modules).
            module_file = getattr(module, "__file__", None)
            if not isinstance(module_file, str):
                continue

            module_path = Path(module_file)
            add("__file__.parent", module_path.parent)

            resolved = module_path.resolve()
            # If the parsed path actually exists, then traverse all its ancestor directories.
            if resolved.exists():
                for ancestor in resolved.parents:
                    add("__file__.ancestor", ancestor)
                    # If the root directory has been reached, stop traversing upward.
                    if ancestor == resolved.anchor:
                        break

        # 4) Fallback working directory.
        add("cwd", Path.cwd())

        return roots

    @classmethod
    def locate_asset(cls, *parts):
        """Return the first actually existing <candidate root>/<relative>, return None if all are missing."""
        rel = Path("assets", *parts)
        logger = cls._get_logger()
        for source, root in cls._candidate_roots():
            candidate = root / rel
            if candidate.is_file():
                logger.debug(f"Resource Located via [{source}] -> {candidate}")
                return candidate
            # Adapt the source code tree (assets are in <root>/src/assets/...).
            nested = root / "src" / rel
            if nested.is_file():
                logger.debug(f"Resource Located via [{source}]/src -> {nested}")
                return nested
        logger.debug(f"Resource Not Found: {rel}")
        return None

    @classmethod
    def describe_runtime(cls):
        if hasattr(sys, "_MEIPASS"):
            return f"PyInstaller Bundle (Extraction Path: {sys._MEIPASS})"
        if getattr(sys.modules.get("__main__", None), "__compiled__", None) is not None:
            return "Nuitka Bundle"
        if getattr(sys, "frozen", False):
            return "Generic Frozen Bundle (sys.frozen)"
        return "Source Tree (Unbundled)"


class AppResources:
    @staticmethod
    def app_temp_dir():
        for candidate in (
            Path(tempfile.gettempdir()) / "MSPCManagerHelper",
            PathResolver.system_root() / "Temp" / "MSPCManagerHelper",
            Path.home() / ".cache" / "MSPCManagerHelper",
        ):
            try:
                candidate.mkdir(parents=True, exist_ok=True)
                return str(candidate)
            except OSError:
                continue
        # Current working directory as the last resort.
        final = Path.cwd() / "MSPCManagerHelper"
        final.mkdir(parents=True, exist_ok=True)
        return str(final)

    @staticmethod
    def app_icon():
        icon_path = ResourceLocator.locate_asset("icons", "MSPCManagerHelper.ico")
        return str(icon_path) if icon_path else None

    @staticmethod
    def fluent_icons_font_path():
        font_path = ResourceLocator.locate_asset("fonts", "FluentSystemIcons-Regular.ttf")
        return str(font_path) if font_path else None

    @staticmethod
    def _get_binary_path(tool_folder, x64_binary, arm64_binary):
        from core.system_checks import PrerequisiteChecks
        arch_key = PrerequisiteChecks.check_os_architecture()

        if arch_key == "ARM64":
            arm64_path = ResourceLocator.locate_asset("tools", tool_folder, arm64_binary)
            if arm64_path:
                return str(arm64_path)

        # Compatible with ARM64 when using x64.
        x64_path = ResourceLocator.locate_asset("tools", tool_folder, x64_binary)
        return str(x64_path) if x64_path else None

    @staticmethod
    def nsudo_path():
        return AppResources._get_binary_path("NSudo", "NSudoLC_x64.exe", "NSudoLC_ARM64.exe")
