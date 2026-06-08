from crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from addUpdateWebPages import addUpdateWebPages
from addUpdateImages import addUpdateImages
from indexPages import indexPages
from indexImages import indexImages

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
