from states.image import Image
from urllib.parse import urljoin
from tokenizer import tokenize_by_freq

def getImages(config,soup,url):
    img_tags = soup.find_all("img")
    stopwords = config.stopwords
    stemmer = config.stemmer

    seen_images ={}
    seen_descp =set()
    for img_tag in img_tags:
        src= img_tag.get("src")
        if not src:
            continue

        image_url = urljoin(url,src)
        description = (img_tag.get("alt") or img_tag.get("title") or "").strip()

        if not image_url in seen_images:
            image  = Image(image_url)
            image.description = description
            seen_images[image_url] = image
            seen_descp.add((image_url,description))

        elif not (image_url,description) in seen_descp:
            seen_images[image_url].description += " "+description
            seen_descp.add((image_url,description))

        
    
    for image in seen_images.values():
        if image.description:
            image.word_tf  = tokenize_by_freq(image.description,stopwords,stemmer)
        
    return list(seen_images.values())

                
        
        
