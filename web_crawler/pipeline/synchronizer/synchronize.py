from crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from crawler_exceptions.CrawlerDBErr import RedisPoolErr
from pageIndexer.indexer import indexWebPages
from sync_crawlqueue import sync_crawlqueue
from sync_domains import sync_domains

def synchronize(config,appstate,workerstate):
    if not appstate.pages_queue.qsize() >=config.EXPORT_BATCH_SIZE:
        return
    if appstate.mysql_sync_lock.acquire(blocking = False):
        try:
            pages_batch= [appstate.pages_queue.get() for _ in range(config.EXPORT_BATCH_SIZE)]

            #index all the pages in pages_batch:
            indexWebPages(pages_batch,workerstate)
            #update and sync crawl queue in mysql:
            sync_crawlqueue(workerstate)
            #update and sync domains table:
            sync_domains(workerstate)
            
            #commit all to sql
            workerstate.mysql_client.commit()

        except MysqlPoolErr as err:
            workerstate.mysql_client.rollback()
            raise MysqlPoolErr(f"{err}") from err
        
        except RedisPoolErr as err:
            workerstate.mysql_client.rollback()
            raise RedisPoolErr(f"{err}") from err

    
    else:
        return