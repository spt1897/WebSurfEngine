import redis
import mysql.connector
import crawler_exceptions.CrawlerDBErr
import sys
#this fucntion checks whether 
# there is any current crawl queue or crawl domain in the redis cache
#Ensures that if a current crawling session is already on , 
# the new crawler continues it
#else if the cache is empty,
#  we hydrate it by the the data from the DB and resume crawling from last saved crawl list
def hydrate_redis(config, appstate, workerstate):
    redis_client = workerstate.redis_client
    mysql_client = workerstate.mysql_client
    mysql_cursor = workerstate.mysql_cursor


    with appstate.redis_hydrator_lock:
        try:

            if(redis_client.llen("crawl_queue")>0 
             and redis_client.hlen("domains") >0):
                print("A crawling session is already active. Continuing the same.")
                return
            
            pipeline = redis_client.pipeline()
            #pushing the crawl queue in batches to redis cache
            mysql_cursor.execute("""
                SELECT id, url
                FROM crawl_queue
                WHERE status = 'not_crawled'
                ORDER BY id
                LIMIT %s;
            """, (config.IMPORT_BATCH_SIZE,))

            crawl_queue = mysql_cursor.fetchall()

            if not crawl_queue:
                print("No url to crawl in crawl queue in SQL server. Closing crawler.")
                sys.exit(0)
            
            ids = [row[0] for row in crawl_queue]
            urls = [row[1] for row in crawl_queue]

            format_ids = ",".join(["%s"] * len(ids))

            mysql_cursor.execute(f"""
                UPDATE crawl_queue
                SET status = 'in_process',
                 in_process_started=NOW()
                WHERE id IN ({format_ids});
            """, ids)

            mysql_client.commit()

            for url in urls:
                pipeline.rpush("crawl_queue", url)

            pipeline.execute()

            #pushing the domain hashmap to redis cache
            mysql_cursor.execute("""
                SELECT domain, num_pages
                FROM domains;
            """)

            domains=mysql_cursor.fetchall()

            for domain , num_pages in domains:
                pipeline.hset("domains", domain, int(num_pages))

            pipeline.execute()

            #pushing the visited pages url from mysql to seen set in redis cache

            mysql_cursor.execute("""
                SELECT url,last_crawled
                FROM WebPages
                ORDER BY id;
            """)

            while True:
                visited_urls = mysql_cursor.fetchmany(10000)

                if not visited_urls:
                    break

                for (url,last_crawled) in visited_urls:
                    pipeline.hset("visited_urls",url,int(last_crawled.timestamp()))
                
                pipeline.execute()

        
        except mysql.connector.Error as mysqlerr:
            mysql_client.rollback()
            raise crawler_exceptions.CrawlerDBErr.MysqlPoolErr(f"Error during redis hydration : {mysqlerr}") from mysqlerr
        
        except redis.RedisError as rediserr:
            mysql_client.rollback()
            raise crawler_exceptions.CrawlerDBErr.RedisPoolErr(f"Error during redis hydration : {rediserr}") from rediserr

        except Exception as err:
            print(f"Error while hydrating redis: {err}")
            raise
            

        
