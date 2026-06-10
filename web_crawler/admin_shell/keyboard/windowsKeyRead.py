import msvcrt
from web_crawler.admin_shell.keyboard.keys import Key


def windowsKeyRead()->tuple:
    char = msvcrt.getwch()

    if char == '\r':
        return (Key.ENTER,)

    elif char== '\b':
        return (Key.BACKSPACE,)

    elif char == '\t':
        return (Key.TAB,)

    elif char == '\x03':
        return (Key.CTRL_C,)

    elif char in ['\x00', '\xe0']:
        special_char = msvcrt.getwch()

        match special_char:
            case 'H':
                return (Key.ARROW_UP,)

            case 'P':
                return (Key.ARROW_DOWN,)

            case 'K':
                return (Key.ARROW_LEFT,)

            case 'M':
                return (Key.ARROW_RIGHT,)

            case 'G':
                return (Key.HOME,)

            case 'O':
                return (Key.END,)

            case 'S':
                return (Key.DELETE,)

            case _:
                return (Key.UNKNOWN,)

    else:
        return (Key.CHAR, char)