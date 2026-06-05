#Configuration setting for the crawler, database and redis credentials
#loaded once from the enviornment variables
#Static and globaly shared by all threads
class Config:
    def __init__(self):
        #database:==================================================
        self.DB_HOST : str | None=None
        self.DB_USER : str | None =None
        self.DB_PASSWORD : str | None =None
        self.DB_NAME : str| None =None
        #============================================================
        #Web_Crawler Configuration:==================================
        self.NUM_WORKERS : int| None =None
        self.LINKS_PER_PAGE : int | None=None
        self.PAGES_PER_DOMAIN : int | None=None
        self.MAX_RETRY : int| None =None
        self.REQUEST_DELAY: int |None=None
        self.CONNECTION_DELAY: int |None=None
        self.CRAWL_DELAY: int |None=None
        self.REQUEST_TIMEOUT:int |None =None
        self.BATCH_SIZE : int| None =None
        self.USER_AGENT :str|None  = None
        #=============================================================
        #Redis:=======================================================
        self.REDIS_HOST : str | None=None
        self.REDIS_PORT : int | None=None
        self.REDIS_PASSWORD : str| None =None
        #=============================================================
        #others(constants for parsing, indexing etc.):
        self.stopwords =  set(["i", "is","are","am","the","a","an","be","being",
                    "will","shall","would","should","can","not","or","and",
                    "could","cannot","if","of","for","in","on","at","by","about"])
        
        #==============================================================