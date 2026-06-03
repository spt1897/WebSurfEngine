import redis
import time
import sys 

#Redis Connection pool:
def connect_to_Redis_pool(config, appstate):
    with appstate.redis_connect_lock:
        if appstate.redis_pool is not None:
            return 
        tries =0 
        while not appstate.redis_pool:
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
                    print("Connected to Redis Server✅.")

                else:
                    print("Redis Server didn't respond.")
                    appstate.redis_pool=None

            except redis.exceptions.AuthenticationError:
                print("Couldn't connect to Redis! Authentication Error.")
                appstate.redis_pool= None 
            
            except Exception as err:
                print(f"Couldn't connect to Redis server. Error:{err}")
                appstate.redis_pool=None
            
            if not appstate.redis_pool:
                if tries<config.MAX_RETRY:
                    print(f"{tries}/{config.MAX_RETRY} tries. Retrying in {config.CONNECTION_DELAY} seconds...")   
                    time.sleep(config.CONNECTION_DELAY)
                else:
                    sys.exit(1)