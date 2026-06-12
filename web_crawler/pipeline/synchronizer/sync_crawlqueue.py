import redis
from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr

def sync_crawlqueue(workerstate):
    redis_client = workerstate.redis_client
    mysql_cursor = workerstate.mysql_cursor
    try:
        successful_urls = [str(redis_client.lpop("successful_crawl")) for _ in range(int(redis_client.llen("successful_crawl"))) ]
        formatstring = ",".join(["%s"]*len(successful_urls))

        #delete succesfully crawled urls from crawl_queue
        if successful_urls:
            mysql_cursor.execute(f"""DELETE FROM crawl_queue WHERE url IN ({formatstring})""",
                             successful_urls)
        
        #update new urls to crawl_queue

        crawling_urls = [(url,) for url in redis_client.lrange("crawl_queue",0,-1)]

        mysql_cursor.executemany("""INSERT INTO crawl_queue(url,status,in_process_started)
                                 VALUES (%s,'in_process',NOW())
                                 ON DUPLICATE KEY UPDATE 
                                 status ='in_process',
                                 in_process_started = NOW()""",crawling_urls)
    
    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while syncing crawl queue.{err}") from err

    except Exception as err:
        raise MysqlPoolErr(f"Error while syncing crawl queue.{err}") from err

