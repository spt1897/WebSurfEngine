#dependencies=====================================
from bs4 import BeautifulSoup
from queue import Queue
import requests
from pathlib import Path
from nltk.stem import PorterStemmer
import nltk
import urllib.robotparser
#=================================================
#crawler and indexer modules:=================
import indexer

def crawler_indexer_pipeline():
    #local variables for each worker==============================
    mysql_client=None
    mysql_cursor=None
    redis_client=None
    #=============================================================
    while True:
        #====================================
        #Startup initial connection to mysql and redis (Only any one worker does it)
        if not mysql_pool: 
            connect_to_MySQL_pool()

        if not redis_pool: connect_to_Redis_pool()
        #===================================
        #get a connection from the pool:
        
        #====================================

def main():
    pass


if __name__=="main":
    main()