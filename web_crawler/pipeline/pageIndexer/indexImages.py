from crawler_exceptions.CrawlerDBErr import MysqlPoolErr

def indexImages(pages_batch,workerstate):
    mysql_cursor  = workerstate.mysql_cursor
    try:
        #since images are deleted before so automatically respective indexes are deleted
        #insert new indexes of images of webpage
        imageIndex_rows = [(image.id,keyword,tf) for page in pages_batch for image in page.images for keyword,tf in image.word_tf.items()]
        if not imageIndex_rows:
            return

        mysql_cursor.executemany("""INSERT INTO image_index(image_id,keyword,tf)
                                 VALUES (%s,%s,%s)""",imageIndex_rows)


    except Exception as err:
        raise MysqlPoolErr(f"Error while indexing image in page.{err}") from err