"""The command-line interface for CPDLog."""

import typer
import logging
from pathlib import Path
from cpdlog import create_db
from cpdlog import app
from cpdlog.views import *


import click
from cheroot.wsgi import Server

__version__ = '0.1.0'


def main(
    port: int = 5003
) -> None:

    LOG_FORMAT = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)

    folder = Path('.')
    db_fp = folder / "cpdlog.db"
    db_uri = f"sqlite:///{db_fp}"

    if not db_fp.is_file():
        typer.echo(f"Creating {db_fp}")
        create_db(db_uri)

    host = "127.0.0.1"

    typer.echo(f"Starting CPDLog on http://{host}:{port}")

    server = Server((host, port), app)
    server.start()

typer.run(main)