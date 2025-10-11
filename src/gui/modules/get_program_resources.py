import platform
import winreg
from pathlib import Path


class GetProgramResources:
    @staticmethod
    def get_program_icon():
        # Get Root Directory
        program_base_dir = Path(__file__).resolve().parents[2]  # ..\..\assets\icons
        program_icon_path = program_base_dir / 'assets' / 'icons' / 'MSPCManagerHelper.ico'
        if program_icon_path.exists():
            return str(program_icon_path)
        else:
            return None

    @staticmethod
    def get_nsudo_path():
        program_base_dir = Path(__file__).resolve().parents[2]  # ..\..\assets\NSudo
        arch_map = {
            'AMD64': program_base_dir / 'assets' / 'NSudo' / 'NSudoLC_x64.exe',
            'ARM64': program_base_dir / 'assets' / 'NSudo' / 'NSudoLC_ARM64.exe'
        }

        # Method 1
        try:
            machine = (platform.machine() or '').lower()
            if any(k in machine for k in ('AMD64', 'x86_64', 'x64', 'Intel64')):
                arch_key = 'AMD64'
            elif any(k in machine for k in ('ARM64', 'AArch64')):
                arch_key = 'ARM64'
            else:
                arch_key = None
        except Exception:
            arch_key = None

        if arch_key:
            nsudo_path = arch_map.get(arch_key)
            if nsudo_path and nsudo_path.exists():
                return str(nsudo_path)

        # Method 2
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment') as key:
                processor_architecture, _ = winreg.QueryValueEx(key, 'PROCESSOR_ARCHITECTURE')
        except (FileNotFoundError, OSError):
            return None

        nsudo_path = arch_map.get(processor_architecture)
        return str(nsudo_path) if nsudo_path and nsudo_path.exists() else None

    @staticmethod
    def get_procdump_path():
        program_base_dir = Path(__file__).resolve().parents[2]  # ..\..\assets\ProcDump
        arch_map = {
            'AMD64': program_base_dir / 'assets' / 'ProcDump' / 'procdump64.exe',
            'ARM64': program_base_dir / 'assets' / 'ProcDump' / 'procdump64a.exe'
        }

        # Method 1
        try:
            machine = (platform.machine() or '').lower()
            if any(k in machine for k in ('AMD64', 'x86_64', 'x64', 'Intel64')):
                arch_key = 'AMD64'
            elif any(k in machine for k in ('ARM64', 'AArch64')):
                arch_key = 'ARM64'
            else:
                arch_key = None
        except Exception:
            arch_key = None

        if arch_key:
            procdump_path = arch_map.get(arch_key)
            if procdump_path and procdump_path.exists():
                return str(procdump_path)

        # Method 2
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment') as key:
                processor_architecture, _ = winreg.QueryValueEx(key, 'PROCESSOR_ARCHITECTURE')
        except (FileNotFoundError, OSError):
            return None

        procdump_path = arch_map.get(processor_architecture)
        return str(procdump_path) if procdump_path and procdump_path.exists() else None
