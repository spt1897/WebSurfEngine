import threading
from pipeline.pipelineManager import pipelineManager
from states.workerstate import WorkerState

#spawns the worker threads ony by one and assigns their workerstate and id 
def spawn_workers(config, appstate):
    for i in range(config.NUM_WORKERS):
        workerstate = WorkerState(i)
        worker= threading.Thread(
            name=f"Crawler_Worker-{i}",
            target=pipelineManager,
            args=(config, appstate, workerstate),
              daemon=True)
        appstate.worker_states.append(workerstate)
        appstate.crawler_workers.append(worker)
        worker.start()
        print(f"Crawler_Worker #id:{i} spawned.")