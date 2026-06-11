from enum import Enum

#shell commands
class Command(Enum):
    SET = 1   #command: 'set <variable> <value>' (sets or changes the value of a config variable)
    GET = 2   #command: 'get <variable>' (gets the current value of a config variable)
    GET_DB = 3 #command: 'get-db' (gets all the database credentials)
    GET_REDIS = 4 #command: 'get-redis' (gets all the redis credentials)
    STATUS = 5 #command: 'status' (gets crawler status: num_workers,pages_queue_size, pages_batch_size and other necessary values)
    RECONNECT_DB = 6 #command: 'emergency-reconnect-db' (invokes reconnection to database manually after multiple failed connection tries)
    PAUSE = 7 #command: 'pause' (pauses the crawlers from any task)
    RESUME = 8 #command: 'resume' (resumes the crawler after pause)
    SHUTDOWN = 9 #command: 'shutdown' (shuts the crawler down gracefully after finishing all important tasks(processing sync and failed urls))
    FORCE_SHUTDOWN = 10 #command: 'force-shutdown' (force fully shuts the crawler despite any pending sync or failed urls)
    RESTART = 11 #command: 'restart' (restarts the crawler after graceful 'shutdown')
    HELP=12 #command: 'help' (helps user on how to use the admin shell)
    STATUS_WORKERS =13 #command: 'status-workers' (views current status of all workers)
    STATUS_WORKER =14 #command: 'status-worker <id>' (views current status of a specific worker(id starts from 0))
    RESTORE_DEFAULT =15 #command: 'restore-default' (restores default configuration settings from environment variables)
    CLEAR =16

#shell commands mapped to command enums
command_map = {
    "set": Command.SET,
    "get": Command.GET,
    "get-db":Command.GET_DB,
    "get-redis":Command.GET_REDIS,
    "status": Command.STATUS,
    "status-workers": Command.STATUS_WORKERS,
    "status-worker": Command.STATUS_WORKER,
    "emergency-reconnect-db": Command.RECONNECT_DB,
    "pause": Command.PAUSE,
    "resume":Command.RESUME,
    "shutdown":Command.SHUTDOWN,
    "quit":Command.SHUTDOWN,
    "exit":Command.SHUTDOWN,
    "force-shutdown":Command.FORCE_SHUTDOWN,
    "restart":Command.RESTART,
    "help":Command.HELP,
    "h":Command.HELP,
    "info":Command.HELP,
    "restore-default":Command.RESTORE_DEFAULT,
    "clear" : Command.CLEAR,
    "cls" : Command.CLEAR,
    "clean": Command.CLEAR,
    "clr": Command.CLEAR
}

command_expected_args = {
    Command.SET : 2,
    Command.GET : 1,
    Command.STATUS_WORKER :1
}