from states.image import Image
from urllib.parse import urljoin
from tokenizer import tokenize_by_freq

def getImages(config,soup,url):
    img_tags = soup.find_all("img")
    images = []
    stopwords = config.stopwords
    stemmer = config.stemmer
    for img_tag in img_tags:
        src= img_tag.get("src")
        if not src:
            continue
        image  = Image(urljoin(url,src))
        image.description = (img_tag.get("alt") or img_tag.get("title") or "").strip()

        if image.description:
            image.word_tf  = tokenize_by_freq(image.description,stopwords,stemmer)
        
        images.append(image)

    return images

                
        
        
