from queue import Queue
import threading
#Controls Terminal state like input buffer, cursor pos, command history, etc

class TerminalState():
    def __init__(self):
        #input
        self.normal_mode=True
        self.input_buffer = ""
        self.inputLine = ""
        self.cur_input_line_on =""
        self.cursor_pos = 0
        self.command_history = []
        self.nav_cmd_hist = 0
        self.input_lock =  threading.Lock()
        #output
        self.msg_queue = Queue()
        self.msg_lock = threading.Lock()
        #render buffer
        self.render_buffer = []
        #shutdown_achived(true when shutdown() function recognises all threads and tasks are complete and shutdown)
        self.shutdown_achieved= False
        self.restart=True
        #needs redraw
        self.needs_redraw = True