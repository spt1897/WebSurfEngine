from states.appstate import AppState
from states.config import Config
from states.configure import configure_crawler
from workersManager.spawner import spawn_workers

def main():
    config = Config()
    appstate = AppState()
    configure_crawler(config=config)
    spawn_workers(config,appstate)
    


if __name__=="main":
    main()