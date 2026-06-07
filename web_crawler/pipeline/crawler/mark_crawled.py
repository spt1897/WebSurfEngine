import redis
import time
from crawler_exceptions.CrawlerDBErr import RedisPoolErr


def mark_crawled(page,workerstate):
    redis_client = workerstate.redis_client
    try:
        #increment the domain counter of the page
        if(redis_client.hget("visited_urls",page.url)):
            cur_domain_count=int(redis_client.hget("domains",page.domain) or 0)
            redis_client.hset("domains",page.domain,cur_domain_count+1)

        #add url to visited urls list
        cur_time = int(time.time())
        redis_client.hset("visited_urls",page.url,cur_time)

        #add url to successful_crawl : makes it easy to update crawl_queue in sql
        redis_client.rpush("successful_crawl",page.url)


    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while marking done!{err}") from err