import sys
import tty
import termios
from web_crawler.admin_shell.keyboard.keys import Key

def read_char():
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        return sys.stdin.read(1)

    finally:
        termios.tcsetattr(
            fd,
            termios.TCSADRAIN,
            old
        )

def unixKeyRead():
    
    ch = read_char()
    
    if ch == '\r' or ch == '\n':
        return (Key.ENTER,)

    elif ch == '\x7f':
        return (Key.BACKSPACE,)
    elif ch == '\t':
        return (Key.TAB,)

    elif ch == '\x03':
        return (Key.CTRL_C,)


    elif ch == '\x1b':

        second = read_char()

        if second != '[':
            return (Key.UNKNOWN,)

        third = read_char()

        match third:

            case 'A':
                return (Key.ARROW_UP,)

            case 'B':
                return (Key.ARROW_DOWN,)

            case 'C':
                return (Key.ARROW_RIGHT,)

            case 'D':
                return (Key.ARROW_LEFT,)

            case 'H':
                return (Key.HOME,)

            case 'F':
                return (Key.END,)

            case '3':
                read_char()  # consume '~'
                return (Key.DELETE,)

            case _:
                return (Key.UNKNOWN,)

    else:
        return (Key.CHAR, ch)