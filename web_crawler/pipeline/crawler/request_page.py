import requests
import time

#This function requests response from a url, 
# and retries if any error occurs after delaying sometime else returns None

def request_page(config,url):
    tries = 0 
    while tries<=config.MAX_RETRY:
        try:
            tries+=1
            response = requests.get(
                    url,
                    headers={
                        "User-Agent": config.USER_AGENT
                    },
                    timeout=config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
            
            if 400<= response.status_code <500:
                return None
            if response.status_code ==200:
                return response

        except Exception as err:
           time.sleep(config.REQUEST_DELAY)
    
    return None
