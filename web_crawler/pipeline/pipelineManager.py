from dbmanager.mysqlPool import connect_to_MySQL_pool
from dbmanager.redisPool import connect_to_Redis_pool
from dbmanager.redisHydrator import hydrate_redis
from states.webpage import WebPage
from crawler.geturl import getUrlfromCrawlQueue
from crawler.isEligibleToCrawl import isEligibleToCrawl
from crawler.check_robots import check_robots
from pageParser.parser import parseWebPage
from crawler import pushLinkstoQueue
from pageIndexer.indexer import indexWebPage
import mysql.connector
import redis


#The pipeline Manager function handles the entire pipeline execution:
#connecting to MySQL server
#connecting to Redis server
#Hydrating redis
#parsing (extracting links , metadata, texts)
#word stemming and indexing 
#updating database
#syncing to DB periodically from redis
def pipelineManager(config, appstate, workerstate):
    while True:
        try:
            #====================================
            #Startup initial connection to mysql and redis (Only any one worker does it)
            if not appstate.mysql_pool: 
                connect_to_MySQL_pool()

            if not appstate.redis_pool:
                connect_to_Redis_pool()
            #===================================
            #get a connection from the pool:
            if (not workerstate.mysql_client 
                or not workerstate.mysql_client.is_connected()): 
                workerstate.mysql_client = appstate.mysql_pool.get_connection()
                workerstate.mysql_cursor =  workerstate.mysql_client.cursor()

            if not workerstate.redis_client :
                workerstate.redis_client = redis.Redis(connection_pool=appstate.redis_pool)       
            #====================================
            #Hydrate Redis on startup (initialization of cache):
            if not (workerstate.redis_client.llen("crawl_queue")>0 
             and workerstate.redis_client.hlen("domains") >0):
                hydrate_redis()

            #=====================================
            #get the url from the crawl queue
            #and call the crawling , parsing, indexing functions to operate:

            #get url:
            url  = getUrlfromCrawlQueue(workerstate)

            if not url:
                continue  # if crawl queue empty ,
                        # go to next iteration and load queue from mysql
            
            #otherwise create a page object , pass the url and call the other fucntions

            page = WebPage(url)
            

            
            if( 
            isEligibleToCrawl(config,page,workerstate) #check whether the link is already a visited link
             #check if we have not crossed the domain page limit
                and
            check_robots(page, config, workerstate) #robots.txt compliance and then we proceed for rest of the task
                and
            parseWebPage(config,appstate,workerstate,page) #parse for metadata, links ,stemmed text
                and
            pushLinkstoQueue(page,workerstate) #push the links from the page to redis crawl queue before indexing
                and 
            indexWebPage(page,workerstate)
            ):
                pass
                


        
        except Exception as err:
            pass
