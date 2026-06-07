from crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def addUpdateImages(page,workerstate):
    mysql_cursor =  workerstate.mysql_cursor
    try:
        #delete old image entries if any
        mysql_cursor.execute("""DELETE FROM Images
                             WHERE page_id = %s""",(page.id,))
        
        #insert new image entries to Images

        image_rows = [(page.id,image.image_url, image.description) for image in page.images]

        mysql_cursor.executemany("""INSERT INTO Images(page_id,image_url,description) 
                             VALUES (%s,%s,%s)""",image_rows)

        #get back the ids later useful for indexing
        
        mysql_cursor.execute("""SELECT id, image_url FROM Images WHERE page_id = %s""",(page.id,))

        imageurl_id = {}

        results = mysql_cursor.fetchall()

        for result in results :
            imageurl_id[result[1]]= result[0]

        for image in page.images:
            image.id = imageurl_id[image.image_url]
        
    
    except Exception as err:
        raise MysqlPoolErr(f"Error while adding images of page to MySQL. {err}") from err