from crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from addUpdateWebPage import addUpdateWebPage
from addUpdateImages import addUpdateImages
from indexPage import indexPage
from indexImage import indexImage

def indexWebPage(page,workerstate):
    try:
        page.id = addUpdateWebPage(page,workerstate)
        if page.id and page.stemmedWords_tf:
            indexPage(page,workerstate)

        if page.images:
            addUpdateImages(page,workerstate)
            indexImage(page,workerstate)

        workerstate.mysql_client.commit()
        return True
    
    except MysqlPoolErr as mysqlErr:
        workerstate.mysql_client.rollback()
        raise MysqlPoolErr(f"{mysqlErr}") from mysqlErr