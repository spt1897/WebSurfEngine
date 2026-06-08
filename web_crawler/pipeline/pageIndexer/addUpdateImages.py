from crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def addUpdateImages(pages_batch,workerstate):
    mysql_cursor =  workerstate.mysql_cursor
    try:
        #delete old image entries if any
        page_ids = [page.id for page in pages_batch]
        formatstring = ",".join(["%s"]*len(page_ids))

        mysql_cursor.execute(f"""DELETE FROM Images
                             WHERE page_id IN({formatstring})""",page_ids)
        
        #insert new image entries to Images

        image_rows = [(page.id,image.image_url, image.description) for page in pages_batch for image in page.images]

        if image_rows:
            mysql_cursor.executemany("""INSERT INTO Images(page_id,image_url,description) 
                             VALUES (%s,%s,%s)""",image_rows)

            #get back the ids later useful for indexing
            
            mysql_cursor.execute(f"""SELECT page_id,image_url,id FROM Images WHERE page_id IN ({formatstring})""",page_ids)

            imageurl_id = {(page_id,image_url) :id for page_id,image_url,id in mysql_cursor.fetchall()}    

            for page in pages_batch:
                for image in page.images:
                    image.id = imageurl_id[page.id,image.image_url]
        
    
    except Exception as err:
        raise MysqlPoolErr(f"Error while adding images of page to MySQL. {err}") from err