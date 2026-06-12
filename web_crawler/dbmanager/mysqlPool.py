import mysql.connector
from mysql.connector import pooling
import time
import sys 
from web_crawler.workersManager.shutdownHandler import force_shutdown

#MySQL Connection Pool :
def connect_to_MySQL_pool(config, appstate):
    with appstate.mysql_connect_lock:
        if not appstate.mysql_pool and not (appstate.mysql_server_down and config.keep_crawling):
            
            tries=0
            while not appstate.mysql_pool:
                if appstate.crawler_pause.is_set():
                    time.sleep(config.CRAWL_DELAY)
                    continue

                test_client =None # a test client for pinging and checking
                test_cursor=None # a test cursor for excuting pinging
                try:
                    tries+=1
                    appstate.mysql_pool=pooling.MySQLConnectionPool(
                    pool_name="mysql_pool",
                    pool_size=config.NUM_WORKERS,  
                    host=config.DB_HOST,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    database=config.DB_NAME,
                    auth_plugin="mysql_native_password"
                    )
                    #ping the connection
                    test_client = appstate.mysql_pool.get_connection()
                    test_cursor = test_client.cursor()
                    test_cursor.execute("SELECT 1;")
                    test_cursor.fetchone()
                    appstate.msg_queue.put(("SUCCESS","MySQL",f"Connected to MySQL Server.\nName:{config.DB_NAME}, Host:{config.DB_HOST}"))
                    appstate.mysql_server_down = False

                except Exception as err:
                    appstate.msg_queue.put(("ERROR","MySQL",f"Couldn't connect to MySQL server.\nError:{err}"))
                    appstate.mysql_pool=None
                
                finally:
                    if test_cursor:
                        test_cursor.close()
                    if test_client:
                        test_client.close()

                if not appstate.mysql_pool:
                    if tries<config.MAX_RETRY:
                        appstate.msg_queue.put(("INFO","MySQL",f"{tries}/{config.MAX_RETRY} tries. Retrying in {config.CONNECTION_DELAY} seconds..."))   
                        time.sleep(config.CONNECTION_DELAY)
                    else:
                        if config.keep_crawling == True:
                            appstate.msg_queue.put(("ERROR","MySQL","Couldn't connect to SQL after multiple tries.\nCONFIG:keep_crawling is set to 'True'. Crawling shall continue without sync or hydration."))
                            appstate.msg_queue.put(("INFO","MySQL","If you want to change this, use 'set keep_crawling false' to force shut crawling operations."))
                            appstate.msg_queue.put(("INFO","MySQL","To invoke reconnection with SQL, use 'reconnect-mysql' ."))
                            appstate.msg_queue.put(("INFO","MySQL","To pause crawling temporarily use 'pause' and 'resume' to resume crawling."))
                        else:
                            appstate.msg_queue.put(("ERROR","MySQL","Couldn't connect to SQL after multiple tries.\nCONFIG:keep_crawling is set to 'False'. Force shutting crawler."))
                            time.sleep(2)
                            force_shutdown()

                        appstate.mysql_server_down = True
                        return
