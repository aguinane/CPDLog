import csv
import logging
from pathlib import Path

from .activity import Activity

log = logging.getLogger(__name__)


def load_logfile(file_path: Path, reverse: bool = True) -> list[Activity]:
    """Load list of CPD Activities from file"""
    activities = []
    with open(file_path) as f:
        reader = csv.reader(f)
        firstline = next(reader)
        if firstline[0] != "CPDLog":
            raise ValueError(f"{file_path} is in the wrong format.")
        headings = [x.replace(" ", "_") for x in next(reader)]
        for row in reader:
            items = dict(zip(headings, row, strict=False))
            act = Activity(**items)
            activities.append(act)
    activities.sort(key=lambda x: x.act_date, reverse=reverse)
    return activities


def act_to_dict(act: Activity) -> dict:
    """Convert activity to dictionary for export"""
    item = act.dict()
    item["cpd_type"] = str(item["cpd_type"])[-1]  # Get last bit of enum
    return item


def save_logfile(file_path: Path, activities: list[Activity], append: bool = True):
    """Save list of activities to file"""

    fieldnames = Activity.schema()["properties"].keys()
    activities.sort(key=lambda x: x.act_date)
    if append:
        if not file_path.exists():  # Create empty file first
            save_logfile(file_path, activities=[], append=False)
        with open(file_path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            for act in activities:
                item = act_to_dict(act)
                writer.writerow(item)
    else:
        with open(file_path, "w", newline="", encoding="utf-8") as fh:
            fh.write("CPDLog\n")
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for act in activities:
                item = act_to_dict(act)
                writer.writerow(item)


def check_create_logfile(file_path: Path) -> int:
    """Create new logfile if does not exist"""

    if not file_path.exists():  # Create new file
        save_logfile(file_path, activities=[], append=False)

    num_activities = len(load_logfile(file_path))
    return num_activities
