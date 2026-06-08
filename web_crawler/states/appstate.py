import threading
from nltk.stem import PorterStemmer
from queue import Queue

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
        pages_queue = Queue()