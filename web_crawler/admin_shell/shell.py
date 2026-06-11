from web_crawler.states.appstate import AppState
from web_crawler.states.config import Config
from web_crawler.states.terminal import TerminalState
from web_crawler.states.configure import configure_crawler
from web_crawler.admin_shell.interpreter.interpreterHandler import interpreterHandler
from web_crawler.admin_shell.keyboard.updateInputBuffer import updateInputBuffer
import threading
import sys
import colorama
import time
import shutil
import math
   
    

#appends from msg_queue to render_buffer , things in render_buffer is actually rendered
def append_msg_to_render_buffer(terminal):

    while not terminal.msg_queue.empty():
        with terminal.msg_lock:
            terminal.render_buffer.append(terminal.msg_queue.get_nowait())
            terminal.msg_queue.task_done()
        terminal.needs_redraw=True
        

#Calculates no. of lines due to '\n' no. of lines due to text wrapping and determines cursor position to be redrawn, 
# then renders the msgs in render_buffer and redraws prompt and cursor 
def draw_terminal(terminal,config):
    sys.stdout.write("\033[2J")
    sys.stdout.write("\033[?25l")
    #sys.stdout.write("\r\033[K")
    sys.stdout.write("\033[H")
    sys.stdout.write("\033[3J")
    with terminal.msg_lock:
        msgs = list(terminal.render_buffer)

    col_size,_  = shutil.get_terminal_size()

    rendered_rows = 0
    render_text_total =""
    for msg in msgs:
        text = ""
        if msg[0] == "SUCCESS":
            text = f"[{msg[0]}] [{msg[1]}]: {msg[2]}"
            render_text_total+=f"\033[32m{text}\033[0m\n"
            #sys.stdout.write(f"\033[32m{text}\033[0m\n")

        elif msg[0] =="ERROR":
            text = f"[{msg[0]}] [{msg[1]}]: {msg[2]}"
            render_text_total+=f"\033[31m{text}\033[0m\n"
            #sys.stdout.write(f"\033[31m{text}\033[0m\n")

        elif msg[0] == "INFO":
            text = f"[{msg[0]}] [{msg[1]}]: {msg[2]}"
            render_text_total+=f"\033[34m{text}\033[0m\n"
            #sys.stdout.write(f"\033[34m{text}\033[0m\n")

        elif msg[0] == "WARNING":
            text = f"[{msg[0]}] [{msg[1]}]: {msg[2]}"
            render_text_total+=f"\033[33m{text}\033[0m\n"
            #sys.stdout.write(f"\033[33m{text}\033[0m\n")

        elif msg[0] == "":
            text =f"{msg[2]}"
            render_text_total+=f"{text}\033[0m\n"
            #sys.stdout.write(f"{text}\033[0m\n")

        elif msg[0]=="SUCCESS_NO_WRITE":
            text = f"{msg[2]}"
            render_text_total+=f"\033[32m{text}\033[0m\n"
            #sys.stdout.write(f"\033[32m{text}\033[0m\n")
        
        visual_rows = 0
        for line in text.split('\n'):
            visual_rows += max(1, math.ceil(len(line) / col_size))

        rendered_rows += visual_rows
    
    prompt = f"{config.USER_AGENT}> "
    
    with terminal.input_lock:
        input_buffer =terminal.input_buffer
        cursor_pos = terminal.cursor_pos

    render_text_total +=prompt+input_buffer
   

    absolute_cursor_column = len(prompt) + cursor_pos
    cursor_column=absolute_cursor_column % col_size + 1
    #sys.stdout.write(f"{prompt}{input_buffer}")
    sys.stdout.write(render_text_total)
    cursor_row = rendered_rows+ absolute_cursor_column//col_size + 1
   
    sys.stdout.write("\033[J")
    sys.stdout.write(f"\033[{cursor_row};{cursor_column}H") 
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

    terminal.needs_redraw = False
    





#continously checks for command input , passess it to execute ,
#  sends msg_queues to be stacked into render buffer 
#Redraws when necessary : key hit , new msgs
def shell(config, appstate , terminal):
    colorama.just_fix_windows_console()
    input_handler  = threading.Thread(target = updateInputBuffer, args=(terminal,config),daemon=True)

    input_handler.start()
    terminal.msg_queue.put(("INFO","Admin-REPL","Use command: 'help' or 'h' or 'info' for user guide."))
    while not terminal.shutdown_achieved:
        
        inputLine = None
        with terminal.input_lock:
            if terminal.inputLine:
                inputLine = terminal.inputLine
        
        if inputLine:
            interpreter_handler = threading.Thread(target=interpreterHandler, args= (config,appstate,terminal,inputLine), daemon=True)
            interpreter_handler.start()

        append_msg_to_render_buffer(terminal)

        if terminal.needs_redraw:
            draw_terminal(terminal,config)

        time.sleep(0.01)
