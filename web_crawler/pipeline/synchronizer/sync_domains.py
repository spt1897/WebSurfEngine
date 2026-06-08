import redis
from crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from crawler_exceptions.CrawlerDBErr import RedisPoolErr

def sync_domains(workerstate):
    redis_client = workerstate.redis_client
    mysql_cursor = workerstate.mysql_cursor
    try:
       
        domains_rows = [(domain, num_pages, num_pages) for domain , num_pages in redis_client.hgetall("domains").items()]

        mysql_cursor.executemany("""INSERT INTO domains(domain,num_pages) 
                                VALUES (%s,%s) ON DUPLICATE KEY UPDATE 
                                 num_pages = %s""",domains_rows)
    
    except redis.RedisError as err:
        raise RedisPoolErr(f"Error while syncing domains.{err}") from err

    except Exception as err:
        raise MysqlPoolErr(f"Error while syncing domains.{err}") from err

