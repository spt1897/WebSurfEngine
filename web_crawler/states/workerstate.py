#This contains all the important worker states #
# local for the worker -variables , individual connections to DB from the pools , and others
#Every thread(worker) has its own worker state object and is NOT shared globally

class WorkerState:
    def __init__(self,id):
        #worker id in the worker array===================================
        self.worker_id : int | None  = id 
        #================================================================
        #Individual MySQL and Redis client:===============================
        self.mysql_client= None 
        self.mysql_cursor = None
        self.redis_client = None
        #=================================================================
        #Current url being processed======================================
        self.url = None
        self.started_at = None
        #pages crawled by worker==========================================
        self.pages_crawled = 0
        self.error_pages =0