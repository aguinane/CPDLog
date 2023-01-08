import logging
from datetime import datetime, timedelta
from pathlib import Path

from .logfile import load_logfile

log = logging.getLogger(__name__)


def get_trimester_groups(years: int = 3):
    now = datetime.now()
    num_grps = years * 4 + 1
    for x in range(num_grps):
        dt = now - timedelta(weeks=52 / 4 * x)
        if dt.month <= 3:
            yield f"{dt.year}-Q1"
        elif dt.month <= 6:
            yield f"{dt.year}-Q2"
        elif dt.month <= 9:
            yield f"{dt.year}-Q3"
        else:
            yield f"{dt.year}-Q4"


def get_cpd_summary(logfile: Path, years: int = 3):
    activities = [
        x for x in load_logfile(logfile, reverse=False) if not x.expired(years)
    ]

    total_hours = 0.0
    quarter_totals = {}
    groups = list(get_trimester_groups(years))
    for group in reversed(groups):
        quarter_totals[group] = 0.0
    for act in activities:
        total_hours += act.cpd_hours
        group = f"{act.year}-Q{act.trimester}"
        quarter_totals[group] += act.cpd_hours
    return {"total_hours": total_hours, "quarter_totals": quarter_totals}
