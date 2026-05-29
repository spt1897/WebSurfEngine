#This contains all the important worker states #
# local for the worker -variables , individual connections to DB from the pools , and others
#Every thread(worker) has its own worker state object and is NOT shared globally

class WorkerState:
    def __init__(self):
        #worker id in the worker array===================================
        self.worker_id : int | None  = None 
        #================================================================
        #Individual MySQL and Redis client:===============================
        self.mysql_client= None 
        self.mysql_cursor = None
        self.redis_client = None
        #=================================================================