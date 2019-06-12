import logging
import webbrowser
from cpdlog import create_db
from cpdlog import app
from cpdlog.views import *


db_url = "sqlite:///data/cpdlog.db"
create_db(db_url)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)

    # import_ea_file()
    app.run(threaded=False)
