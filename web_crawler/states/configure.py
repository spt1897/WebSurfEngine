from dotenv import load_dotenv
import os

def configure_crawler(config):
    #load environment variables 
    load_dotenv(dotenv_path="../.env")
    #database:
    config.DB_HOST=os.getenv("DB_HOST","localhost").strip()
    config.DB_USER=os.getenv("DB_USER","").strip()
    config.DB_PASSWORD=os.getenv("DB_PASSWORD","").strip()
    config.DB_NAME=os.getenv("DB_NAME","").strip()
    #Redis
    config.REDIS_HOST=os.getenv("REDIS_HOST","localhost").strip()
    config.REDIS_PORT=int(os.getenv("REDIS_PORT","6379").strip())
    config.REDIS_PASSWORD=os.getenv("REDIS_PASSWORD","").strip()
    #Crawler config
    config.NUM_WORKERS=int(os.getenv("NUM_WORKERS","5").strip())
    config.LINKS_PER_PAGE=int(os.getenv("LINKS_PER_PAGE","20").strip())
    config.PAGES_PER_DOMAIN=int(os.getenv("PAGES_PER_DOMAIN","100").strip())
    config.MAX_RETRY=int(os.getenv("MAX_RETRY","10").strip())
    config.REQUEST_DELAY=int(os.getenv("REQUEST_DELAY","3").strip())
    config.CONNECTION_DELAY=int(os.getenv("CONNECTION_DELAY","3").strip())
    config.CRAWL_DELAY=int(os.getenv("CRAWL_DELAY","3").strip())
    config.REQUEST_TIMEOUT=int(os.getenv("REQUEST_TIMEOUT","10").strip())
    config.IMPORT_BACTH_SIZE=int(os.getenv("IMPORT_BACTH_SIZE","10").strip())
    config.EXPORT_BACTH_SIZE=int(os.getenv("EXPORT_BACTH_SIZE","10").strip())
    config.USER_AGENT=os.getenv("USER_AGENT","WebSurfBot").strip()
    config.RECRAWL_TIMER_SEC=int(os.getenv("RECRAWL_TIMER_SEC","").strip())
    config.keep_crawling=bool(os.getenv("keep_crawling","False").strip())
    print("Environment variables loaded successfully✅!")