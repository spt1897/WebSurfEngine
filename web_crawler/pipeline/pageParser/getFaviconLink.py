from urllib.parse import urljoin
from urllib.parse import urlparse

def getFaviconLink(soup,url):
    #find the link tag with "icon"
    favicon_tag = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
    if favicon_tag and favicon_tag.get("href"):
        return urljoin(url,favicon_tag.get("href"))
    
    parsed_url = urlparse(url)
    return urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}","/favicon.ico")