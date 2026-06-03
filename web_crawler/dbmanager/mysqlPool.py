import mysql.connector
from mysql.connector import pooling
import time
import sys 

#MySQL Connection Pool :
def connect_to_MySQL_pool(config, appstate):
    with appstate.mysql_connect_lock:
        if appstate.mysql_pool is not None:
            return
        
        tries=0
        while not appstate.mysql_pool:
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
                database=config.DB_NAME
                )
                #ping the connection
                test_client = appstate.mysql_pool.get_connection()
                test_cursor = test_client.cursor()
                test_cursor.execute("SELECT 1;")
                test_cursor.fetchone()
                print(f"Connected to MySQL Server✅-Name:{config.DB_NAME}, Host:{config.DB_HOST}")
            
            except Exception as err:
                print(f"Couldn't connect to MySQL server. Error:{err}")
                appstate.mysql_pool=None
            
            finally:
                if test_cursor:
                    test_cursor.close()
                if test_client:
                    test_client.close()

            if not appstate.mysql_pool:
                if tries<config.MAX_RETRY:
                    print(f"{tries}/{config.MAX_RETRY} tries. Retrying in {config.CONNECTION_DELAY} seconds...")   
                    time.sleep(config.CONNECTION_DELAY)
                else:
                    sys.exit(1)
