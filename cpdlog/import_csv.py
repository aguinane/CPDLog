import logging
import csv
from typing import List, Tuple
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model import Activities

log = logging.getLogger(__name__)


def import_csv_file(file_path) -> Tuple[List[str], List[List[str]]]:
    """ Import the csv file """
    rows = []
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        headings = next(reader, None)
        for row in reader:
            rows.append(row)
    return headings, rows


def import_cpd_activities(db_url: str, filename):
    """ Save records from export to specified database """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    h, rows = import_csv_file(filename)
    rows = reversed(rows)
    for row in rows:
        ext_ref = row[0]
        cpd_category = row[1]
        start_date = parse(row[2], dayfirst=True)
        end_date = parse(row[3], dayfirst=True)
        act_type = row[4]
        topic = row[5]
        provider = row[6]
        location = row[7]
        duration = row[8]
        practice_hrs = row[9]
        risk_hrs = row[10]
        business_hrs = row[11]
        learning_outcome = row[12]
        notes = row[13]

        r = session.query(Activities).filter(Activities.ext_ref == ext_ref).first()
        if r:
            log.info("Skipped existing entry %s", ext_ref)
            continue

        activity = Activities(
            cpd_category=cpd_category,
            start_date=start_date,
            end_date=end_date,
            act_type=act_type,
            topic=topic,
            provider=provider,
            location=location,
            duration=duration,
            learning_outcome=learning_outcome,
            notes=notes,
            ext_ref=ext_ref,
            practice_hrs=practice_hrs,
            risk_hrs=risk_hrs,
            business_hrs=business_hrs,
        )
        session.add(activity)
        session.commit()
    session.commit()
