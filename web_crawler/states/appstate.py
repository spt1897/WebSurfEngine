import threading
from nltk.stem import PorterStemmer
from queue import Queue
import time

#Contains important app state infos
#globally shared variables , connection pools ,threading locks etc.
#Modifiable and accesible by each worker 
class AppState:
    def __init__(self):
        #=======================================================
        #Global database and redis connection pools
        self.mysql_pool =None 
        self.redis_pool =None
        #========================================================
        #worker tracker
        self.crawler_workers =[]
        self.worker_states = []
        self.pages_crawled:int = 0
        self.error_pages:int =0
        self.start_time = time.time()
        #========================================================
        #Global threading locks
        self.mysql_connect_lock=threading.Lock()
        self.redis_connect_lock=threading.Lock()
        self.redis_hydrator_lock=threading.Lock()
        self.mysql_sync_lock=threading.Lock()
        #=========================================================
        #other shared objects/tools for parsing,indexing etc.
        self.stemmer = PorterStemmer()
        #=========================================================
        #globally shared parsed pages object queue which the synchronizer uses to batch writing/indexing to DB
        self.pages_queue = Queue()
        self.pages_batch=[]
        #=========================================================
        #urls not completely parsed due to infrastructure failure
        self.failed_urls=Queue()
        #=========================================================
        #Global Events:
        self.crawler_shutdown = threading.Event()
        self.crawler_pause = threading.Event()
        #when sql down
        self.mysql_server_down= False 
        #redis down
        self.redis_server_down = False
        #=========================================================
        #reference to msg_queue for workers to log errors/progress:
        self.msg_queue = None
        #=========================================================