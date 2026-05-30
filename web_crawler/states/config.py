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
        self.DELAY_SEC : int| None =None
        self.BATCH_SIZE : int| None =None
        #=============================================================
        #Redis:=======================================================
        self.REDIS_HOST : str | None=None
        self.REDIS_PORT : int | None=None
        self.REDIS_PASSWORD : str| None =None
        #=============================================================