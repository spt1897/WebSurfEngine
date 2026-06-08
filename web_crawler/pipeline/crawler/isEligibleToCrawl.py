import time
import redis
from crawler_exceptions.CrawlerDBErr import RedisPoolErr

def isEligibleToCrawl(config,page,workerstate):
    try:
        last_crawled = workerstate.redis_client.hget("visited_urls",page.url)
        cur_time = int(time.time())

        #check if last crawled time from current time more than recrawl timer
        if last_crawled:
            if not (cur_time - int(last_crawled) >= config.RECRAWL_TIMER_SEC):
                return False
        
        #check if url already in process by other workers
        if workerstate.redis_client.sismember("in_process_pages",page.url):
            return False

        #check if domain count has not exceeded
        if not int(workerstate.redis_client.hget("domains",page.domain) or 0 )<=config.PAGES_PER_DOMAIN:
            return False

        workerstate.redis_client.sadd("in_process_pages",page.url)
        page.crawled_at= cur_time
        return True
    
    except redis.RedisError as err:
        raise RedisPoolErr("Error while checking eligibity") from err