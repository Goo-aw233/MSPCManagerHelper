import os
import winreg


class GetProgramResources:
    @staticmethod
    def get_program_icon():
        # Get Root Directory
        program_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        program_icon_path = os.path.join(program_base_dir, 'assets', 'icons', 'MSPCManagerHelper.ico')
        if os.path.exists(program_icon_path):
            return program_icon_path
        else:
            return None

    @staticmethod
    def get_nsudo_path():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment') as key:
                processor_architecture, _ = winreg.QueryValueEx(key, 'PROCESSOR_ARCHITECTURE')
        except (FileNotFoundError, OSError):
            return None

        program_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        arch_map = {
            'AMD64': os.path.join(program_base_dir, 'assets', 'NSudo', 'NSudoLC_x64.exe'),
            'ARM64': os.path.join(program_base_dir, 'assets', 'NSudo', 'NSudoLC_ARM64.exe')
        }
        nsudo_path = arch_map.get(processor_architecture)
        return nsudo_path if nsudo_path and os.path.exists(nsudo_path) else None

    @staticmethod
    def get_procdump_path():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment') as key:
                processor_architecture, _ = winreg.QueryValueEx(key, 'PROCESSOR_ARCHITECTURE')
        except (FileNotFoundError, OSError):
            return None

        program_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        arch_map = {
            'AMD64': os.path.join(program_base_dir, 'assets', 'ProcDump', 'procdump64.exe'),
            'ARM64': os.path.join(program_base_dir, 'assets', 'ProcDump', 'procdump64a.exe')
        }
        procdump_path = arch_map.get(processor_architecture)
        return procdump_path if procdump_path and os.path.exists(procdump_path) else None
