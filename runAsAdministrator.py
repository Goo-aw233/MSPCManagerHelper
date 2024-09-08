import ctypes
import sys

class Administrator:
    # 获取用户是否以管理员身份运行
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return 0

    # 重新启动脚本并请求管理员权限
    def run_as_admin(params):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 0)
        sys.exit()
