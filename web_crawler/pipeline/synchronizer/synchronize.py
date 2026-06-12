from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from web_crawler.crawler_exceptions.CrawlerDBErr import RedisPoolErr
from web_crawler.pipeline.pageIndexer.indexer import indexWebPages
from web_crawler.pipeline.synchronizer.sync_crawlqueue import sync_crawlqueue
from web_crawler.pipeline.synchronizer.sync_domains import sync_domains
import time
from datetime import datetime

def synchronize(config,appstate,workerstate):
    if not appstate.pages_queue.qsize() >=config.EXPORT_BATCH_SIZE and not appstate.pages_batch and not appstate.crawler_shutdown.is_set():
        return
    if appstate.mysql_sync_lock.acquire(blocking = False):
        try:
            with appstate.pages_lock:
                if not appstate.pages_batch:
                    if appstate.crawler_shutdown.is_set() and appstate.pages_queue.qsize() <config.EXPORT_BATCH_SIZE:
                        while not appstate.pages_queue.empty():
                            appstate.pages_batch.append(appstate.pages_queue.get_nowait())

                    else:
                        appstate.pages_batch= [appstate.pages_queue.get_nowait() for _ in range(config.EXPORT_BATCH_SIZE)]

                #index all the pages in pages_batch:
                indexWebPages(appstate.pages_batch,workerstate)
                #update and sync crawl queue in mysql:
                sync_crawlqueue(workerstate)
                #update and sync domains table:
                sync_domains(workerstate)
                
                #commit all to sql
                workerstate.mysql_client.commit()
                for _ in appstate.pages_batch:
                    appstate.pages_queue.task_done()

                appstate.pages_batch= []
                appstate.msg_queue.put(("INFO",f"Time: {datetime.fromtimestamp(time.time())}","Periodic Sync to Database succesfully."))


        except MysqlPoolErr as err:
            workerstate.mysql_client.rollback()
            raise MysqlPoolErr(f"{err}") from err
        
        except RedisPoolErr as err:
            workerstate.mysql_client.rollback()
            raise RedisPoolErr(f"{err}") from err
        
        finally:
            appstate.mysql_sync_lock.release()

    
    else:
        return