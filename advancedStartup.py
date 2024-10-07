import ctypes
import sys

class AdvancedStartup:
    @staticmethod
    def is_devmode():
        devmode_args = ['/devmode', '-devmode']
        return any(arg.lower() in devmode_args for arg in sys.argv)

    @staticmethod
    def is_debugdevmode():
        debugdevmode_args = ['/debugdevmode', '-debugdevmode']
        return any(arg.lower() in debugdevmode_args for arg in sys.argv)

    @staticmethod
    # 获取用户是否以管理员身份运行
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return 0

    @staticmethod
    # 重新启动并请求管理员权限
    def run_as_admin(params):
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 0)
        if result > 32:
            sys.exit()
