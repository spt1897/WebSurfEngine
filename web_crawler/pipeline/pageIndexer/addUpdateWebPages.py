from crawler_exceptions.CrawlerDBErr import MysqlPoolErr
from datetime import datetime
def addUpdateWebPages(pages_batch,workerstate):
    mysql_cursor = workerstate.mysql_cursor
    try:
          
          insert_row = [(page.url, page.title, page.description,page.favicon_url,
                       page.domain,page.scheme,datetime.fromtimestamp(page.crawled_at),page.title,page.description,page.favicon_url,datetime.fromtimestamp(page.crawled_at))
                       for page in pages_batch]
          mysql_cursor.executemany("""INSERT INTO WebPages
                (url,title, description , favicon, domain, scheme,last_crawled)
                              VALUES (%s,%s,%s,%s,%s,%s,NOW())
                              ON DUPLICATE KEY UPDATE
                              title = %s, description =%s , favicon =%s, last_crawled=%s""",
                              insert_row)
         

          #get ids of the pages:
          urls = [page.url for page in pages_batch]

          formatstring = ",".join(["%s"] * len(urls))

          mysql_cursor.execute(f"""SELECT url,id FROM WebPages WHERE url IN ({formatstring})""",urls)

          #map urls to ids
          url_id = {url:id for url,id in mysql_cursor.fetchall()}

          #assign ids to respective pages
          for page in pages_batch:
               page.id= url_id[page.url]

          


    except Exception as err:
         raise MysqlPoolErr(f"Error while adding page to MySQL.Err={err}") from err