import logging
import csv

log = logging.getLogger(__name__)


def build_activity_export(file_path, activities):
    """ Export Activities to CSV """
    headings = [
        "refno",
        "cpd type",
        "start date",
        "end date",
        "activity type",
        "topic",
        "provider",
        "location",
        "total hrs",
        "area of practice hrs",
        "risk hrs",
        "business hrs",
        "learning_outcome",
        "notes",
    ]

    rows = []
    for act in activities:
        row = [
            act.ext_ref,
            act.cpd_category,
            act.start_date,
            act.end_date,
            act.act_type,
            act.topic,
            act.provider,
            act.location,
            act.duration,
            act.practice_hrs,
            act.risk_hrs,
            act.business_hrs,
            act.learning_outcome,
            act.notes,
        ]
        rows.append(row)

    with open(file_path, "w", newline="") as csvfile:
        cwriter = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        cwriter.writerow(headings)
        for row in rows:
            cwriter.writerow(row)
    log.info("Created %s", file_path)
