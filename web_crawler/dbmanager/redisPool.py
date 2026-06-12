import redis
import time
import sys 

#Redis Connection pool:
def connect_to_Redis_pool(config, appstate):
    with appstate.redis_connect_lock:
        if appstate.redis_server_down or appstate.redis_pool is not None :
            return 
        tries =0 
        while not appstate.redis_pool:
            if appstate.crawler_pause.is_set():
                    time.sleep(config.CRAWL_DELAY)
                    continue

            try:
                tries+=1
                appstate.redis_pool=redis.ConnectionPool(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=0,
                password=config.REDIS_PASSWORD,
                decode_responses =True
                )
                #ping the connection
                test_client = redis.Redis(connection_pool=appstate.redis_pool)
                if test_client.ping():
                    appstate.msg_queue.put(("SUCCESS","Redis","Connected to Redis Server."))
                    appstate.redis_server_down=False
                    
                else:
                    appstate.msg_queue.put(("ERROR","Redis","Redis Server didn't respond."))
                    appstate.redis_pool=None

            except redis.exceptions.AuthenticationError:
                appstate.msg_queue.put(("ERROR","Redis","Couldn't connect to Redis! Authentication Error."))
                appstate.redis_pool= None 
            
            except Exception as err:
                appstate.msg_queue.put(("ERROR","Redis",f"Couldn't connect to Redis server.\nError:{err}"))
                appstate.redis_pool=None
            
            if not appstate.redis_pool:
                if tries<config.MAX_RETRY:
                    appstate.msg_queue.put(("INFO","Redis",f"{tries}/{config.MAX_RETRY} tries. Retrying in {config.CONNECTION_DELAY} seconds..."))
                    time.sleep(config.CONNECTION_DELAY)
                else:
                    appstate.msg_queue.put(("ERROR","Redis","Couldn't connect to redis after multiple tries.Saving data to MySQL and Shutting down!"))
                    appstate.redis_server_down=True
                    return