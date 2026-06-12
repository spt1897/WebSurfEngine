from web_crawler.crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def indexPages(pages_batch,workerstate):
    mysql_cursor =  workerstate.mysql_cursor
    try:
        #delete existing indexing if any for all pages
        page_ids = [page.id for page in pages_batch]
        formatstring = ",".join(["%s"]*len(page_ids))

        mysql_cursor.execute(f"""DELETE FROM keywords WHERE page_id IN ({formatstring})"""
                             ,page_ids)

        #Index the page using stemmedWords_TF
        keywords_rows = [(words,page.id,tf) for page in pages_batch for words,tf in page.stemmedWords_TF.items()]
        
        if keywords_rows:
            mysql_cursor.executemany("""INSERT IGNORE INTO keywords(keyword,page_id,tf)
                                 VALUES (%s,%s,%s)""",keywords_rows)
        
        

    except Exception as err:
        raise MysqlPoolErr(f"Error while indexing page! {err}") from err