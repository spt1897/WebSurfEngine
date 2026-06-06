#stores important informations for image

class Image:
    def __init__(self,url):
        self.image_url:str = url
        self.description : str|None= None
        self.word_tf: dict[str,int] = {}