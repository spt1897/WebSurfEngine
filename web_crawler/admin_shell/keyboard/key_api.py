
import platform
if platform.system() == "Windows":
    from web_crawler.admin_shell.keyboard.windowsKeyRead import windowsKeyRead
else:
    from web_crawler.admin_shell.keyboard.unixKeyRead import unixKeyRead

def read_key():
    os = platform.system()
    if os == "Windows":
        return windowsKeyRead()

    elif os == "Linux" or os == "Darwin":
        return unixKeyRead()