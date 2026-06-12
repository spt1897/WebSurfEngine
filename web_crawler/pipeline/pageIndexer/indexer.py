from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from web_crawler.pipeline.pageIndexer.addUpdateWebPages import addUpdateWebPages
from web_crawler.pipeline.pageIndexer.addUpdateImages import addUpdateImages
from web_crawler.pipeline.pageIndexer.indexPages import indexPages
from web_crawler.pipeline.pageIndexer.indexImages import indexImages

def indexWebPages(pages_batch,workerstate):
    try:
        #add and index webpages
        addUpdateWebPages(pages_batch,workerstate)
        indexPages(pages_batch,workerstate)

        #add and index images in the pages
        addUpdateImages(pages_batch,workerstate)
        indexImages(pages_batch,workerstate)

        return True
    
    except MysqlPoolErr as mysqlErr:
        raise MysqlPoolErr(f"{mysqlErr}") from mysqlErr
