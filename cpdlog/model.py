from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Date, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Initialize the database
Base = declarative_base()


class Activities(Base):
    __tablename__ = "activities"
    act_id = Column(Integer, primary_key=True, autoincrement=True)
    cpd_category = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    act_type = Column(String)
    topic = Column(String)
    provider = Column(String)
    location = Column(String)
    duration = Column(Float)
    notes = Column(String)
    ext_ref = Column(String)
    subjectareas = relationship(
        "SubjectArea", lazy=True, cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return "<Activity {} {} {}>".format(
            self.ext_ref, self.start_date, self.act_type
        )

    @property
    def risk_hrs(self):
        try:
            return self.subjectareas[0].risk_hrs
        except IndexError:
            return 0.0

    @property
    def bus_hrs(self):
        try:
            return self.subjectareas[0].business_hrs
        except IndexError:
            return 0.0

    @property
    def area_hrs(self):
        try:
            return self.subjectareas[0].practice_hrs
        except IndexError:
            return 0.0

    @property
    def total_hrs(self):
        return self.duration

    @property
    def yr_grp(self):
        """ Return year grouping of CPD """
        if self.start_date.month <= 6:
            return f"{self.start_date.year}-H1"
        return f"{self.start_date.year}-H2"

    def cpd_expired(self, years=3):
        """ Return whether record is in last 3 years """
        diff = date.today() - self.start_date
        if diff.days < 365.25 * years:
            return False
        return True


class SubjectArea(Base):
    __tablename__ = "area"
    act_id = Column(Integer, ForeignKey("activities.act_id"), primary_key=True)
    practice_hrs = Column(Float)
    risk_hrs = Column(Float)
    business_hrs = Column(Float)


def get_cpd_activities(db_url):
    """ Get all CPD activities from database """
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    r = session.query(Activities)
    return r


def create_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
