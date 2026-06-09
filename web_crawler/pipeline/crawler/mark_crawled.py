import redis
import time
from crawler_exceptions.CrawlerDBErr import RedisPoolErr


def mark_crawled(page,appstate,workerstate):
    redis_client = workerstate.redis_client
    try:
        
        pipeline = redis_client.pipeline()
        
        #increment the domain counter of the page
        if not (redis_client.hget("visited_urls",page.url)):
            cur_domain_count=int(redis_client.hget("domains",page.domain) or 0)
            pipeline.hset("domains",page.domain,cur_domain_count+1)

        #add url to visited urls list
        cur_time = int(time.time())
        pipeline.hset("visited_urls",page.url,page.crawled_at)

        #add url to successful_crawl : makes it easy to update crawl_queue in sql
        pipeline.rpush("successful_crawl",page.url)

        #push page object to parsed pages queue
        appstate.pages_queue.put(page)
        pipeline.execute()
        appstate.pages_crawled +=1
        workerstate.pages_crawled += 1

    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while marking_done!{err}") from err