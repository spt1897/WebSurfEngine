
def keyHandleFlush():
    try:#windows flush input buffer
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getwch()
    except ImportError: # else unix flush input buffer
        import sys, termios
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)