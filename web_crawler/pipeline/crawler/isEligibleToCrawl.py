import time
import redis
from crawler_exceptions.CrawlerDBErr import RedisPoolErr

def isEligibleToCrawl(config,page,workerstate):
    try:
        last_crawled = workerstate.redis_client.hget("visited_urls",page.url)
        cur_time = int(time.time())

        if last_crawled:
            if not (cur_time - int(last_crawled) >= config.RECRAWL_TIMER_SEC):
                return False
        
        if not int(workerstate.redis_client.hget("domains",page.domain) or 0 )<=config.PAGES_PER_DOMAIN:
            return False

        return True
    
    except redis.RedisError as err:
        raise RedisPoolErr("Error while checking eligibity") from err