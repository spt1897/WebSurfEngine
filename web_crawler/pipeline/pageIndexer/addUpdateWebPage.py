from crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def addUpdateWebPage(page,workerstate):
    mysql_cursor = workerstate.mysql_cursor
    try:
         mysql_cursor.execute("""INSERT INTO WebPages
                (url,title, description , favicon, domain, scheme,last_crawled)
                              VALUES (%s,%s,%s,%s,%s,%s,NOW())
                              ON DUPLICATE KEY UPDATE
                              title = %s, description =%s , favicon =%s, last_crawled=NOW()""",
                              (
                                    page.url,
                                    page.title,
                                    page.description,
                                    page.favicon_url,
                                    page.domain,
                                    page.scheme,

                                    page.title,
                                    page.description,
                                    page.favicon_url
                                ))
         
         mysql_cursor.execute("""SELECT id FROM WebPages WHERE url = %s""",(page.url,))

          #return id for indexing
         return mysql_cursor.fetchone()[0]


    except Exception as err:
         raise MysqlPoolErr(f"Error while adding page to MySQL.Err={err}") from err