from dbmanager.mysqlPool import connect_to_MySQL_pool
from dbmanager.redisPool import connect_to_Redis_pool
from dbmanager.redisHydrator import hydrate_redis
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
            #Hydrate Redis:
            if not (workerstate.redis_client.llen("crawl_queue")>0 
             and workerstate.redis_client.hlen("domains") >0):
                hydrate_redis()

            #=====================================



        
        except Exception as err:
            pass
