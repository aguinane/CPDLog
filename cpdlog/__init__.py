"""
    cpdlog
    ~~~~~
    Record and build reports on CPD Activities
"""

import logging
from logging import NullHandler

from cpdlog.model import Activities, get_cpd_activities, create_db
from cpdlog.migrate_ea import import_ea_cpd_activities
from cpdlog.report import combine_report_data, build_report

__all__ = [
    'Activities',
    'get_cpd_activities',
    'create_db',
    'import_ea_cpd_activities',
    'combine_report_data',
    'build_report',
]

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
