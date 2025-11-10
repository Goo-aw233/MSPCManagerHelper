import os
import re
import winreg
from pathlib import Path


class CheckSystemRequirements:
    translator = None  # 类变量，用于存储 translator 实例

    def __init__(self, translator):
        CheckSystemRequirements.translator = translator  # 设置类变量

    def check_system_requirements(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                current_build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                if int(current_build_number) < 19042:
                    return self.translator.translate("failure_to_meet_system_requirements")
                else:
                    return self.translator.translate("meet_system_requirements")
        except FileNotFoundError:
            return self.translator.translate("cannot_read_version")

    @staticmethod
    def check_system_build_number_and_admin_approval_mode():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                current_build_number = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
                if current_build_number < 26100:     # 出现于 27718/27764, 添加于 26120.4520, br_release 后移除
                    return False

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System") as key:
                admin_approval_mode = int(winreg.QueryValueEx(key, "TypeOfAdminApprovalMode")[0])
                if admin_approval_mode == 2:
                    return True
                elif admin_approval_mode != 2:
                    return False
        except (FileNotFoundError, ValueError, OSError):
            return False

        return False

    @staticmethod
    def check_server_levels():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                installation_type = winreg.QueryValueEx(key, "InstallationType")[0]
                if installation_type != "Server":
                    return False

            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Server") as key:
                    winreg.QueryValueEx(key, "ClientExperienceEnabled")
                    return False
            except FileNotFoundError:
                return True
        except (ValueError, OSError):
            return False

    @staticmethod
    def get_windows_installation_information():
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion") as key:
                display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
                edition_id = winreg.QueryValueEx(key, "EditionID")[0]
                build_lab_ex = winreg.QueryValueEx(key, "BuildLabEx")[0]

                """
                try:
                    lcu_ver = winreg.QueryValueEx(key, "LCUVer")[0]
                    if lcu_ver:
                        return f"Microsoft Windows {display_version} {lcu_ver} {edition_id}\n{build_lab_ex}"
                except OSError:
                    # LCUVer 不存在，读取注册表中的其他版本信息
                    pass
                """

                major_version = winreg.QueryValueEx(key, "CurrentMajorVersionNumber")[0]
                minor_version = winreg.QueryValueEx(key, "CurrentMinorVersionNumber")[0]
                build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                ubr = winreg.QueryValueEx(key, "UBR")[0]
                
                # 读取 Windows Feature Experience Pack 版本
                windows_feature_experience_pack = None
                try:
                    # 使用 os.path.expandvars 处理环境变量（相对路径部分），然后用 PathLib 构建完整路径
                    base_path = Path(os.path.expandvars(r"%SystemRoot%"))
                    manifest_path = base_path / "SystemApps" / "MicrosoftWindows.Client.CBS_cw5n1h2txyewy" / "appxmanifest.xml"
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # 使用正则表达式查找 " Version=\"...\"" 格式，确保前后有空格
                    match = re.search(r' Version="([^"]*)"', content)
                    if match:
                        windows_feature_experience_pack = match.group(1)
                except (FileNotFoundError, OSError):
                    pass
                
                if windows_feature_experience_pack:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}\n{CheckSystemRequirements.translator.translate('windows_feature_experience_pack')}: {windows_feature_experience_pack}"
                else:
                    return f"Microsoft Windows {display_version} {major_version}.{minor_version}.{build_number}.{ubr} {edition_id}\n{build_lab_ex}"
        except (FileNotFoundError, OSError):
            return None
