import sys

def keyHit():
    try:
        import msvcrt
        # Windows: returns True if a keypress is waiting in the console buffer
        return msvcrt.kbhit()
    except ImportError:
        import select #Unix : checks if key is being pressed to read
        r, _, _ = select.select([sys.stdin], [], [], 0.0)
        return bool(r)