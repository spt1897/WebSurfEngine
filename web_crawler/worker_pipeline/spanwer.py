import threading

def spawn_workers(config, appstate, pipeline):
    for i in range(config.NUM_WORKERS):
        worker= threading.Thread(target=pipeline, daemon=True)
        appstate.crawler_workers.append(worker)
        worker.start()
        print(f"Crawler_Worker #id:{i} spawned.")