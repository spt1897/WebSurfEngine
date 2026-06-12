import urllib.robotparser
import redis
from web_crawler.pipeline.crawler.request_page import request_page
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr

#this functions checks if robots.txt of the domain allows the particular page to be crawled
#if robots.txt doesn't exist we consider crawling is allowed

def check_robots(page,config,workerstate):
    try:
        redis_client = workerstate.redis_client
        robots_key = f"robots:{page.domain}"

        robots_file =  redis_client.get(robots_key)

        if not robots_file:
            res = request_page(config,f"{page.scheme}://{page.domain}/robots.txt")
            if res and res.status_code == 200:
                robots_file = res.text
                redis_client.set(robots_key,robots_file)
            else:
               return True
            
        
        rp = urllib.robotparser.RobotFileParser()

        rp.parse(robots_file.splitlines())

        return rp.can_fetch(config.USER_AGENT, page.url)
            

    except Exception as err: # malformed robots.txt file
        return True

    except redis.RedisError as err:
        raise RedisPoolErr("Error while checking robots.txt!") from err