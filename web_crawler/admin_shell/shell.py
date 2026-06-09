from states.appstate import AppState
from states.config import Config
from states.configure import configure_crawler
from admin_shell.shell_tokenizer import tokenize
from admin_shell.shell_parser import parser
from admin_shell.shell_interpreter import shell_execute

config = Config()
appstate =AppState()
configure_crawler(config)

while(True):
    line:str = input("admin> ")
    try:
        tokenized = tokenize(line)
        parsed = parser(tokenized)
        print(shell_execute(parsed,config,appstate))
    except Exception as err:
        print(err)
