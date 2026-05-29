from conn_pools.mysqlPool import connect_to_MySQL_pool
from conn_pools.redisPool import connect_to_Redis_pool

def crawler_indexer_pipeline(config, appstate, workerstate):
    while True:
        #====================================
        #Startup initial connection to mysql and redis (Only any one worker does it)
        if not appstate.mysql_pool: 
            connect_to_MySQL_pool()

        if not appstate.redis_pool: connect_to_Redis_pool()
        #===================================
        #get a connection from the pool:
        
        #====================================
