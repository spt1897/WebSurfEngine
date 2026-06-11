from web_crawler.admin_shell.keyboard.keys import Key
from web_crawler.admin_shell.keyboard.key_api import read_key
from web_crawler.admin_shell.keyboard.keyHit import keyHit
import time


def updateInputBuffer(terminal,config):
    
    while not terminal.shutdown_achieved:
        
        if not terminal.normal_mode:
            time.sleep(0.02)
            continue
        
        if not keyHit():
            time.sleep(0.02)
            continue

        key = read_key()

        with terminal.input_lock:
            if not terminal.inputLine:
                match key[0]:
                    case Key.CHAR:
                        char = key[1]
                        if terminal.cursor_pos == len(terminal.input_buffer):
                            terminal.input_buffer +=char
                        
                        elif terminal.cursor_pos ==0:
                            terminal.input_buffer = char + terminal.input_buffer
                        
                        else:
                            terminal.input_buffer = terminal.input_buffer[:terminal.cursor_pos] + char + terminal.input_buffer[terminal.cursor_pos:]

                        terminal.cursor_pos+=1
                        
                    
                    case Key.HOME:
                        terminal.cursor_pos=0
                        
                    
                    case Key.END:
                        terminal.cursor_pos = len(terminal.input_buffer)
                        

                    case Key.ENTER:
                        
                        if terminal.input_buffer:
                            terminal.inputLine = terminal.input_buffer
                            terminal.input_buffer =""
                            terminal.cursor_pos =0
                            terminal.command_history.append(terminal.inputLine)
                            terminal.nav_cmd_hist=len(terminal.command_history)
                            if not terminal.inputLine.lower().strip() in ["clear","cls","clean","clr"]:
                                terminal.msg_queue.put(("","",f"{config.USER_AGENT}> {terminal.inputLine}"))

                        

                    case Key.BACKSPACE:
                        index = terminal.cursor_pos -1

                        if index >=0 and index <len(terminal.input_buffer):
                            terminal.input_buffer = terminal.input_buffer[:index] +terminal.input_buffer[index+1:]
                            terminal.cursor_pos -=1

                        
                        
                    case Key.DELETE:
                        index = terminal.cursor_pos

                        if index >=0 and index <len(terminal.input_buffer):
                            terminal.input_buffer = terminal.input_buffer[:index] +terminal.input_buffer[index+1:]
                    
                        
                    case Key.ARROW_RIGHT:
                        if terminal.cursor_pos <len(terminal.input_buffer):
                            terminal.cursor_pos +=1
                        
                        
                    
                    case Key.ARROW_LEFT:
                        if terminal.cursor_pos >0:
                            terminal.cursor_pos -=1
                        
                    
                    case Key.ARROW_UP:
                        if terminal.nav_cmd_hist == len(terminal.command_history):
                            terminal.cur_input_line_on = terminal.input_buffer

                        prev = terminal.nav_cmd_hist
                        if terminal.nav_cmd_hist>0:
                            terminal.nav_cmd_hist-=1

                        if prev != terminal.nav_cmd_hist:
                            terminal.input_buffer = terminal.command_history[terminal.nav_cmd_hist]
                            terminal.cursor_pos = len(terminal.input_buffer)


                    case Key.ARROW_DOWN:
                        prev = terminal.nav_cmd_hist
                        if terminal.nav_cmd_hist<len(terminal.command_history):
                            terminal.nav_cmd_hist+=1
                        
                        if prev != terminal.nav_cmd_hist:
                            if terminal.nav_cmd_hist == len(terminal.command_history):
                                terminal.input_buffer = terminal.cur_input_line_on

                            else :
                                terminal.input_buffer = terminal.command_history[terminal.nav_cmd_hist]
                                
                            terminal.cursor_pos = len(terminal.input_buffer)

        
        terminal.needs_redraw=True




                        
