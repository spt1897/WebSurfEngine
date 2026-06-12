import os

#clean shutdown , makes sure every incomplete and failed-urls are processed/tried 
#syncs all parsed data and current stats to DB
#then shuts down safely with loss of data
def shutdown(appstate):
    appstate.crawler_shutdown.set() #signalling workers to prepare for shutdown
    #handle only failed_incomplete_urls, and sync everything in pages-queue to DB

    appstate.failed_urls.join() #make sure all failed_urls tried
    appstate.pages_queue.join() #make sure all parsed pages have been indexed and sync in DB


    for worker in appstate.crawler_workers:
        worker.join()   #wait for all workers to stop one by one

    appstate.redis_pool.disconnect()
    
   

#forceful emergency shutdown 
# [warning this shutdown forcefully kills the process,
#  so any unsynced data may be lost]
def force_shutdown():
    os._exit(0)
