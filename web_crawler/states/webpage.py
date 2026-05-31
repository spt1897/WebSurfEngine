#data related to the page being crawled
#Temporary page object created to store data at every iteration of worker loop
class WebPage:
    def __init__(self):        
        self.url = None
        self.title = None
        self.domain= None
        self.description = None
        self.favicon_url = None
        self.links = []
        self.words=[]