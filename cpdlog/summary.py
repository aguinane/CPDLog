import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from .logfile import load_logfile
from .activity import CPD_TYPE_MAX, MAX_NON_TECHNICAL

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
    total_non_tech_hours = 0.0
    quarter_totals = defaultdict(int)
    cpd_type_totals = defaultdict(int)
    groups = list(get_trimester_groups(years))
    for group in reversed(groups):
        quarter_totals[group] = 0.0
    for act in activities:
        cpd_type_code = act.cpd_type_code
        cpd_type_max = CPD_TYPE_MAX[cpd_type_code]
        if cpd_type_max and cpd_type_totals[cpd_type_code] >= cpd_type_max:
            continue  # Do not count any further hours
        if not act.technical and total_non_tech_hours >= MAX_NON_TECHNICAL:
            continue  # Do not count any further hours

        cpd_type_totals[cpd_type_code] += act.cpd_hours
        group = f"{act.year}-Q{act.trimester}"
        quarter_totals[group] += act.cpd_hours
        total_hours += act.cpd_hours
        if not act.technical:
            total_non_tech_hours += act.cpd_hours
    return {
        "total_hours": total_hours,
        "total_non_tech_hours": total_non_tech_hours,
        "quarter_totals": dict(sorted(quarter_totals.items())),
        "cpd_type_totals": dict(sorted(cpd_type_totals.items(), reverse=True)),
    }
