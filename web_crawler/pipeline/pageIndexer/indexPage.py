from crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def indexPage(page,workerstate):
    mysql_cursor =  workerstate.mysql_cursor
    try:
        #delete existing indexing if any
        mysql_cursor.execute("""DELETE FROM keywords WHERE page_id=%s""",(page.id,))

        #Index the page using stemmedWords_TF
        keywords_rows = [(words,page.id,tf) for words,tf in page.stemmedWords_TF.items()]

        mysql_cursor.executemany("""INSERT INTO keywords(keyword,page_id,tf)
                                 VALUES (%s,%s,%s)""",keywords_rows)
        
        

    except Exception as err:
        raise MysqlPoolErr(f"Error while indexing page! {err}") from err