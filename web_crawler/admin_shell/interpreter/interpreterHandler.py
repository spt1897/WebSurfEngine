from web_crawler.admin_shell.interpreter.shell_tokenizer import tokenize
from web_crawler.admin_shell.interpreter.shell_parser   import parser
from web_crawler.admin_shell.interpreter.shell_interpreter import shell_execute

def interpreterHandler(config,appstate,terminal,inputLine):
    try:
        with terminal.input_lock:
            terminal.inputLine = ""
        exec_result = shell_execute(parser(tokenize(inputLine)),config,appstate,terminal)
        if exec_result != "@{clear}":
             terminal.msg_queue.put(("SUCCESS_NO_WRITE","",exec_result))
                    
    except Exception as err:
        terminal.msg_queue.put(("ERROR","INTERPRETER",str(err)))

        