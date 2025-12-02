import atexit

import gui
from core.cleanup_after_exit import CleanupAfterExit


def main():
    atexit.register(CleanupAfterExit.cleanup_all)
    program = gui.MSPCManagerHelperMainWindow()
    program.mainloop()


if __name__ == "__main__":
    main()
