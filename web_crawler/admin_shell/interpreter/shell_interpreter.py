from datetime import datetime
import time
from web_crawler.admin_shell.interpreter.shell_commands import Command
from web_crawler.states.configure import configure_crawler
from web_crawler.workersManager.shutdownHandler import force_shutdown, shutdown
from web_crawler.admin_shell.keyboard.key_api import read_key
from web_crawler.admin_shell.keyboard.keys import Key
from web_crawler.admin_shell.keyboard.switch_terminal_mode import switch_terminal_mode


#argument errors:
class ArgumentError(Exception):
    pass

class TypeError(ArgumentError):
    pass

class VarNameError(ArgumentError):
    pass

class ValueOutOfBoundsError(ArgumentError):
    pass


def status(config, appstate):
    cur_time = time.time()
    exec_result = ( f"Crawler Status:"
                    f"\nUser-Agent: {config.USER_AGENT}"
                    f"\nSession started at: {datetime.fromtimestamp(appstate.start_time).strftime('%Y-%m-%d %H:%M:%S')}"
                    f"\nSeconds passed(since start): {cur_time-appstate.start_time}"
                    f"\nActive Workers: {len(appstate.crawler_workers)}"
                    f"\nTotal Pages Crawled (Success): {appstate.pages_crawled}"
                    f"\nPages failed(in request/robots.txt/parsing): {appstate.error_pages}"
                    f"\nPages failed due to DB/Redis issue(to be crawled): {appstate.failed_urls.qsize()}"
                    f"\nPages(parsed) in Queue to be Indexed: {appstate.pages_queue.qsize()}"
                    f"\nExport Batch Size: {config.EXPORT_BATCH_SIZE}")
    
    return exec_result



def status_workers(config,appstate):
    exec_result = ( f"Worker Status:"
                    f"Active Workers: {len(appstate.crawler_workers)}\n\n")
            
    for worker in appstate.worker_states:
        exec_result += (f"Worker#{worker.worker_id}:"
                        f"\nTotal Pages Crawled (Success): {worker.pages_crawled}"
                        f"\nPages failed(in request/robots.txt/parsing): {worker.error_pages}"
                        f"\nCurrent url under process: {worker.url}"
                        f"\nCurrent url started at: {datetime.fromtimestamp(worker.started_at).strftime('%Y-%m-%d %H:%M:%S') if worker.started_at else "N/A"}"
                        f"\n\n")
        
    return exec_result



def status_worker(appstate,id):
    worker = appstate.worker_states[id]
    exec_result = (f"Status - Worker#{worker.worker_id}:"
                    f"\nTotal Pages Crawled (Success): {worker.pages_crawled}"
                    f"\nPages failed(in request/robots.txt/parsing): {worker.error_pages}"
                    f"\nCurrent url under process: {worker.url}"
                    f"\nCurrent url started at: {datetime.fromtimestamp(worker.started_at).strftime('%Y-%m-%d %H:%M:%S') if worker.started_at else "N/A"}"
                    f"\n\n")
    
    return exec_result




def shell_execute(command, config, appstate,terminal):
    exec_result = ""
    match command.cmd:

        #set <var> <val>
        case Command.SET:
            var = command.args[0]
            original_var = var 
            value = None
            try:
                if not hasattr(config, var):
                    var = var.replace("-","_")
                    if not hasattr(config,var):
                        var= var.upper()
                        if not hasattr(config,var):
                            var=var.lower()
                          
                var_type = type(getattr(config,var))
            except AttributeError:
                raise VarNameError(f"Variable:'{original_var}' (or similar name) does not exist in configuration.")

            if var_type ==int :
                try:
                    value = int(command.args[1])
                except ValueError:
                    raise TypeError(f"Value Type Error. Variable:'{var}' expects an integer.")
                
                if value < 0:
                    raise ValueOutOfBoundsError(f"Negative value Error. Configuration variables expect a non-negative value.")

            elif var_type ==str :
                value = command.args[1]
              
            elif var_type ==float :
                try:
                    value = float(command.args[1])
                except ValueError:
                    raise TypeError(f"Value Type Error. Variable:'{var}' expects a float.")

            elif var_type ==bool :
                value = command.args[1].lower()
                    
                if value == "true":
                    setattr(config,var,True)
                elif value == "false":
                    setattr(config,var,False)
                else:
                    raise TypeError(f"Value Type Error. Variable:'{var}' expects a boolean value.")


            if not var_type == bool:
                setattr(config,var,value)
            
            exec_result = f"Successfully set {var}:{value}."

            if var.startswith("DB") or var.startswith("REDIS") or var=="NUM_WORKERS":
                exec_result+=f"\n[IMPORTANT] Config variable: '{var}' is an initialization variable and requires 'restart' to be applicable.\n'set' only changes the value in this case but does enforce its use."


        #get <var>
        case Command.GET:
            var = command.args[0]
            original_var = var 
            try:
                if not hasattr(config, var):
                    var = var.replace("-","_")
                    if not hasattr(config,var):
                        var= var.upper()
                        if not hasattr(config,var):
                            var=var.lower()

                exec_result = f"{var} : {getattr(config,var)}"
            except AttributeError:
                raise VarNameError(f"Variable:'{original_var}' (or similar name) does not exist in configuration.")
            
        case Command.HELP:
            available_commands = ("-'set <variable> <value>' (sets or changes the value of a configuration variable. DB,redis credentials or num_worker changes require 'restart' to apply.)"
            "\n-'get <variable>' (gets the current value of a config variable)"
            "\n-'get-db' (gets all the database credentials)"
            "\n-'get-redis' (gets all the redis credentials)"
            "\n-'status' (gets crawler status: num_workers,pages_queue_size, pages_batch_size,user_agent and other necessary values)"
            "\n-'status-workers' (views current status of all workers)"
            "\n-'status-worker <id>' (views current status of a specific worker(id starts from 0))"
            "\n-'emergency-reconnect-db' (invokes reconnection to database manually during crawl-only mode after multiple failed connection tries)"
            "\n-'pause' (pauses the crawlers from any task)"
            "\n-'resume' (resumes the crawler after pause)"
            "\n-'shutdown' (shuts the crawler down gracefully after finishing all important tasks(processing sync and failed urls))"
            "\n-'force-shutdown' (force fully shuts the crawler despite any pending sync or failed urls)"
            "\n-'restart' (restarts the crawler after graceful 'shutdown' with current modified config settings)"
            "\n-'help' (helps user on how to use the admin shell)"
            "\n-'restore-default' (restores default configuration settings from environment variables)"
            "\n")

            exec_result= f"ADMIN SHELL HELP------------------------\n\nWelcome to Websurf Crawler Administrator shell(CLI).\nYou can control(shut,pause,resume,reconnect) the crawler or view/change configuration settings via the shell commands.\n\nAvailable commands:\n{available_commands}"

        case Command.GET_DB:
            exec_result= (f"MySQL Database Credentials:"
                        f"\nName: {config.DB_NAME}"
                        f"\nHost: {config.DB_HOST}"
                        f"\nUser: {config.DB_USER}"
                        f"\nPassword: {config.DB_PASSWORD}")
        
        case Command.GET_REDIS:
            exec_result = (f"Redis Credentials:"
                           f"\nHost: {config.REDIS_HOST}"
                           f"\nPort: {config.REDIS_PORT}"
                           f"\nPassword: {config.REDIS_PASSWORD}")

        case Command.STATUS:
            exec_result= status(config,appstate)


        case Command.STATUS_WORKERS:
           exec_result = status_workers(config,appstate)

        case Command.STATUS_WORKER:
            try:
                id = int(command.args[0])
            except ValueError:
                raise TypeError(f"Value Type Error. Command:'status-worker <id>' expects an integer value for <id>.")

            if id>len(appstate.worker_states)-1 or id <0:
                raise ValueOutOfBoundsError(f"Value out of bounds Error. Worker with id:{id} does not exist in current session.(Id ranges from 0 to (num_worker - 1))")
            
            exec_result = status_worker(appstate,id)
        


        case Command.PAUSE:
            appstate.crawler_pause.set()
            exec_result = "Crawler Operations Paused. Use 'resume' to resume operations."

        case Command.RESUME:
            appstate.crawler_pause.clear()
            exec_result = "Crawler Operations Resumed."
        
        case Command.RECONNECT_DB:
            if appstate.mysql_server_down and config.keep_crawling:
                appstate.mysql_server_down = False
                exec_result= "Trying reconnection to Database."
            
            else:
                exec_result = "Cannot use command: 'emergency-reconnect-db' during normal operation.\nIt is available only when DB server is down and keep_crawling: True"

        case Command.SHUTDOWN:
            appstate.msg_queue.put(("INFO","Crawler","Preparing for Shutdown...\nNot taking any new pages.\nCompleting all incomplete parses...\nFixing DB connections if any...\nSyncing unsynced data to Database...\n"))
            shutdown(appstate)
            appstate.msg_queue.put(("SUCCESS","Crawler","Successfully completed all processes and synced to Database. Exiting REPL..."))
            time.sleep(1)
            appstate.msg_queue.join()
            import sys
            sys.stdout.flush()
            terminal.shutdown_achieved = True



        case Command.RESTART:
            appstate.msg_queue.put(("INFO","Crawler","Preparing for Shutdown...\nNot taking any new pages.\nFixing DB connections if any...\nCompleting all incomplete parses...\nSyncing unsynced data to Database...\n"))
            shutdown(appstate)
            appstate.msg_queue.put(("SUCCESS","Crawler","Successfully completed all processes and synced to Database."))
            terminal.shutdown_achieved = True
            terminal.restart = True
           

        case Command.FORCE_SHUTDOWN:
            appstate.msg_queue.put(("WARNING","Admin-REPL",
                                    "\nUsing 'force-shutdown' force kills all workers and shutsdown the crawler immediately."
                                    +"\nAny unsynced parsed data will not be saved to Database and will be lost."
                                    +"\nAll incomplete or in process urls will be not be processed."
                                    +"\nFor safe shutdown use: 'shutdown' or 'exit'."
                                    +"\nAre you sure you want to Force Shutdown? Press: [Y/N]"))
            
            #get control from updateinputbuffer to this function to take user input
            #flush any existing data
            switch_terminal_mode(terminal)

            key = None
            while not key:
                key= read_key() #take input

            if key[0] ==Key.CHAR and key[1].lower()=='y':
                force_shutdown()
            else:
                appstate.msg_queue.put(("INFO","Admin-REPL","Force Shutdown Aborted."))
                exec_result="@{clear}"
            
            #flush again before handing over control back to updateinputbuffer
            switch_terminal_mode(terminal)
            
            

        case Command.RESTORE_DEFAULT:
            configure_crawler(config,".env")
            exec_result = "Default Configurations restored successfully!"
            
        case Command.CLEAR:
            with terminal.msg_lock:
                terminal.render_buffer = []
                exec_result="@{clear}"

        

    return exec_result