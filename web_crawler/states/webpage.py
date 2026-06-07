#data related to the page being crawled
#Temporary page object created to store data at every iteration of worker loop
from urllib.parse import urlparse

class WebPage:
    def __init__(self,url):    
        self.id=None    
        self.url :str= url
        parsed = urlparse(url)

        self.domain:str= parsed.netloc.lower()
        if self.domain.startswith("www."):
            self.domain = self.domain[4:]
        
        self.scheme: str= parsed.scheme

        self.title :str|None= None
        self.description:str|None = None
        self.favicon_url :str|None= None
        self.links = []
        self.images = []
        self.stemmedWords_TF: dict[str,int]={}