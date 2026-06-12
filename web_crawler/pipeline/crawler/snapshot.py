import pickle
import time
import os
from queue import Queue
from datetime import datetime
def dumpDataToDisk(config, appstate):
    with appstate.pages_lock:
        snapshot = {
            "pages_queue" : list(appstate.pages_queue.queue)+ appstate.pages_batch,
            "failed_urls" : list(appstate.failed_urls.queue),
            "created_at" : time.time()
        }
        
    with open(config.dump_path+".tmp","wb") as f:
        pickle.dump(snapshot,f)

    os.replace(config.dump_path+".tmp", config.dump_path)
    appstate.msg_queue.put(("INFO",f"Time: {datetime.fromtimestamp(time.time())}",f"Unsynced Parsed Data dumped to disc for emergency recovery."))


def loadDumpedDataIfAny(config, appstate):

    
    if not appstate.loadedDumped:
        try:
            with open(config.dump_path,"rb") as f:
                snapshot = pickle.load(f)
                appstate.loadedDumped = True
        except Exception:
            return
    
    with appstate.pages_lock:
            for page in snapshot["pages_queue"]:
                appstate.pages_queue.put(page)
                    
            for url in snapshot["failed_urls"]:
                appstate.failed_urls.put(url)

    appstate.msg_queue.put(("INFO","Crawler",f"Previous parsed dumped data with incomplete sync found.\nDumped at: {datetime.fromtimestamp(snapshot['created_at'])}.\nLoaded it successfully for syncing it to Database."))
            