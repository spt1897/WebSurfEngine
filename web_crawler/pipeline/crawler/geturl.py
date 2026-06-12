import redis
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr

def getUrlfromCrawlQueue(workerstate):
    try:
        return workerstate.redis_client.lpop("crawl_queue")
    
    except redis.RedisError as err:
        raise RedisPoolErr("Error during getting url from crawl queue") from err

    