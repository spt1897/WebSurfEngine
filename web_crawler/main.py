from web_crawler.states.appstate import AppState
from web_crawler.states.config import Config
from web_crawler.states.terminal import TerminalState
from web_crawler.states.configure import configure_crawler
#from web_crawler.workersManager.spawner import spawn_workers
from web_crawler.admin_shell.shell import shell
import time
import threading

def spam(appstate, id):
    while True:
        appstate.msg_queue.put(("","",f"hello from {id}"))
        time.sleep(5) 


def main():
    terminal= TerminalState()
    config = Config()
    configure_crawler(config,".env")    #initial configuration from environment variables


    while not terminal.shutdown_achieved or terminal.restart:
        if terminal.restart:
            appstate= AppState()
            appstate.msg_queue = terminal.msg_queue
            terminal.restart = False
            terminal.shutdown_achieved =False

            for i in range(5):
                threading.Thread(target=spam,args=(appstate,i),daemon=True).start()
        

        shell(config, appstate, terminal)


        

    


if __name__=="__main__":
    main()