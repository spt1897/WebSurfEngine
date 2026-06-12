import redis
from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr

def sync_domains(workerstate):
    redis_client = workerstate.redis_client
    mysql_cursor = workerstate.mysql_cursor
    try:
       
        domains_rows = [(domain, num_pages) for domain , num_pages in redis_client.hgetall("domains").items()]

        mysql_cursor.executemany("""INSERT INTO domains(domain,num_pages) 
                                VALUES (%s,%s) AS domain_row ON DUPLICATE KEY UPDATE 
                                 num_pages = domain_row.num_pages""",domains_rows)
    
    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while syncing domains.{err}") from err

    except Exception as err:
        raise MysqlPoolErr(f"Error while syncing domains.{err}") from err

