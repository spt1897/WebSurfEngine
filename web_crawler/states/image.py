#stores important informations for images in web page
#useful for image search by indexing

class Image:
    def __init__(self,url):
        self.id = None
        self.image_url:str = url
        self.description : str= None
        self.word_tf: dict[str,int] = {}