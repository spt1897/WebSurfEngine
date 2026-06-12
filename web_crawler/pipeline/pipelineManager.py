from web_crawler.dbmanager.mysqlPool import connect_to_MySQL_pool
from web_crawler.dbmanager.redisPool import connect_to_Redis_pool
from web_crawler.dbmanager.redisHydrator import hydrate_redis
from web_crawler.states.webpage import WebPage
from web_crawler.pipeline.crawler.geturl import getUrlfromCrawlQueue
from web_crawler.pipeline.crawler.isEligibleToCrawl import isEligibleToCrawl
from web_crawler.pipeline.crawler.check_robots import check_robots
from web_crawler.pipeline.pageParser.parser import parseWebPage
from web_crawler.pipeline.crawler.pushLinkstoQueue import pushLinkstoQueue
from web_crawler.pipeline.crawler.mark_crawled import mark_crawled
from web_crawler.pipeline.synchronizer.synchronize import synchronize
from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr
from web_crawler.pipeline.crawler.snapshot import dumpDataToDisk, loadDumpedDataIfAny
import time
import redis
import queue


#The pipeline Manager function handles the entire pipeline execution:
#connecting to MySQL server
#connecting to Redis server
#Hydrating redis
#parsing (extracting links , metadata, texts)
#word stemming and indexing 
#updating database
#syncing to DB periodically from redis
def pipelineManager(config, appstate, workerstate):
    while (not appstate.crawler_shutdown.is_set() 
           or not appstate.failed_urls.empty() 
           or not appstate.pages_queue.empty() or appstate.pages_batch) and not appstate.redis_server_down and not (appstate.mysql_server_down and not config.keep_crawling):
        try:
            workerstate.url = None #url to be crawled in this session
            #========================================
            #check if system is not paused (if yes hold from any operations):
            if appstate.crawler_pause.is_set():
                time.sleep(config.CRAWL_DELAY)
                continue
            #====================================
            #Startup initial connection to mysql and redis (Only any one worker does it)
            if not appstate.mysql_pool and not (appstate.mysql_server_down and config.keep_crawling): 
                connect_to_MySQL_pool(config,appstate)

            if not appstate.redis_pool and not appstate.redis_server_down:
                connect_to_Redis_pool(config,appstate)

            if appstate.redis_server_down or (appstate.mysql_server_down and not config.keep_crawling):
                break            
            #===================================
            #get a connection from the pool:
            if not (appstate.mysql_server_down) and (not workerstate.mysql_client 
                or not workerstate.mysql_client.is_connected()): 
                workerstate.mysql_client = appstate.mysql_pool.get_connection()
                workerstate.mysql_cursor =  workerstate.mysql_client.cursor()

            if not workerstate.redis_client and not appstate.redis_server_down:
                workerstate.redis_client = redis.Redis(connection_pool=appstate.redis_pool)       
            #====================================
            #Hydrate Redis on startup (initialization of cache):
            if not (workerstate.redis_client.llen("crawl_queue")>0 
             and workerstate.redis_client.hlen("domains") >0) and not (appstate.mysql_server_down) :
                hydrate_redis(config,appstate,workerstate)

            if not appstate.pages_lock:
                loadDumpedDataIfAny(config,appstate) #load any incomplete dumped data to sync

            #========================================================
            #periodic synchronization to database=====================
            # by any one worker once pages_queue has hit export_batch_size without interrupting other workers
            # (instead of writing to DB after every page crawl)
            if((appstate.pages_queue.qsize()>=config.EXPORT_BATCH_SIZE or appstate.pages_batch) or appstate.crawler_shutdown.is_set()) and not (appstate.mysql_server_down) :
                synchronize(config,appstate,workerstate)

            #=====================================
            #get the url from the crawl queue
            #and call the crawling , parsing, indexing functions to operate:

            #get url:
        
            if not appstate.failed_urls.empty():
                with appstate.pages_lock:
                    try:
                        workerstate.url = appstate.failed_urls.get_nowait()
                        appstate.failed_urls.task_done()
                    except queue.Empty:
                        continue
                if workerstate.redis_client.hget("visited_urls",workerstate.url):
                    workerstate.redis_client.srem("in_process_pages",workerstate.url)
                    if appstate.crawler_shutdown.is_set():
                        continue
                    workerstate.url  = getUrlfromCrawlQueue(workerstate)

            ### if shutdown event has been triggered , no new parsing from crawl_queue
            #only crawl failed urls and batch sync pages to DB 
            
            else:
                if appstate.crawler_shutdown.is_set():
                    continue
                workerstate.url  = getUrlfromCrawlQueue(workerstate)


            if not workerstate.url:
                continue  # if crawl queue empty ,
                        # go to next iteration and load queue from mysql
            
            #otherwise create a page object , pass the url and call the other fucntions

            page = WebPage(workerstate.url)
            workerstate.started_at = time.time()

            
            if( 
            (isEligibleToCrawl(config,page,workerstate) or appstate.msg_queue.put(("ERROR","","Failed at eligibility")))#check whether the link is already a visited link
             #check if we have not crossed the domain page limit
                and
            (check_robots(page, config, workerstate) or appstate.msg_queue.put(("ERROR","","Failed at robots check")))#robots.txt compliance and then we proceed for rest of the task
                    and
            (parseWebPage(config,appstate,workerstate,page) or appstate.msg_queue.put(("ERROR","","Failed at parsing stage")))#parse for metadata, links ,stemmed text
                and
            pushLinkstoQueue(page,workerstate) #push the links from the page to redis crawl queue before indexing
            ):
                mark_crawled(page,appstate,workerstate)

            else:
                workerstate.redis_client.rpush("crawl_queue",workerstate.url)
                appstate.error_pages +=1
                workerstate.error_pages+=1

        
            workerstate.redis_client.srem("in_process_pages",page.url)
            

            #rate-limiting:
            time.sleep(config.CRAWL_DELAY)
        

        except MysqlPoolErr as err:
            appstate.msg_queue.put(("ERROR",f"Worker#{workerstate.worker_id}",f"{err}"))
            workerstate.mysql_client.close()
            connect_to_MySQL_pool(config,appstate)
            workerstate.mysql_client = appstate.mysql_pool.get_connection()
            workerstate.mysql_cursor =  workerstate.mysql_client.cursor()
            if workerstate.url:
                with appstate.pages_lock:
                    appstate.failed_urls.put(workerstate.url)


        except RedisPoolErr as err:
            appstate.msg_queue.put(("ERROR",f"Worker#{workerstate.worker_id}",f"{err}"))
            connect_to_Redis_pool(config,appstate)
            if workerstate.url:
                with appstate.pages_lock:
                    appstate.failed_urls.put(workerstate.url)

    workerstate.mysql_client.close()    #close connection before exiting
    appstate.msg_queue.put(("INFO",f"Worker#{workerstate.worker_id}","Terminated all operations. Closed connection to Database."))