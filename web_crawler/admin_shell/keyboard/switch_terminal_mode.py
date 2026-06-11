import time
from web_crawler.admin_shell.keyboard.keyHandleFlush import keyHandleFlush
def switch_terminal_mode(terminal):
    terminal.normal_mode = not terminal.normal_mode
    time.sleep(0.02)
    keyHandleFlush()