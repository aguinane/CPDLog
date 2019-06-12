"""
    cpdlog
    ~~~~~
    Record and build reports on CPD Activities
"""

import logging
from logging import NullHandler
from flask import Flask
from cpdlog.model import create_db

app = Flask(__name__)
app.config.from_object("config")

__all__ = ["app", "create_db"]


# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
