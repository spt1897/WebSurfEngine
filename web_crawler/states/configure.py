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
    config.DELAY_SEC=int(os.getenv("DELAY_SEC","3").strip())
    print("Environment variables loaded successfully✅!")