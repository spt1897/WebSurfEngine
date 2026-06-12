import redis
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr

def pushLinkstoQueue(page,workerstate):
    redis_client = workerstate.redis_client
    pipeline = redis_client.pipeline()
    try:
        for link in page.links:
            pipeline.rpush("crawl_queue",link)
        
        pipeline.execute()

        return True

    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while pushing links to crawl Queue!. {err}") from err
    
