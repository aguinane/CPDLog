import logging
from pathlib import Path
from cpdlog import create_db
from cpdlog import app
from cpdlog.views import *


Path('data/').mkdir(exist_ok=True) 
db_url = "sqlite:///data/cpdlog.db"
create_db(db_url)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)

    app.run(threaded=False)
