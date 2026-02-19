from datetime import date
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, field_validator

CPD_TYPES = {
    "A": "Tertiary Education",
    "B": "Industry Education",
    "C": "Workplace Learning",
    "D": "Private Study",
    "E": "Service to Industry",
    "F": "Academic Preparation",
    "G": "Industry Engagement",
}

CPD_TYPE_MAX = {
    "A": None,
    "B": None,
    "C": 75.0,
    "D": 18.0,
    "E": 50.0,
    "F": 45.0,
    "G": None,
}

MAX_NON_TECHNICAL = 37.5


class CPDType(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


def create_id() -> str:
    """Generate id"""
    return str(uuid4())[0:8].upper()


class Activity(BaseModel):
    act_id: str = create_id()
    act_date: date
    topic: str
    cpd_hours: float
    cpd_type: CPDType
    technical: bool = False
    provider: str = ""
    learning_outcome: str
    notes: str = ""

    def expired(self, years: int = 3) -> bool:
        """Return whether activity is still valid"""
        diff = date.today() - self.act_date
        return not diff.days < 365.25 * years

    @property
    def cpd_type_code(self) -> str:
        return str(self.cpd_type)[-1]

    @property
    def cpd_type_desc(self) -> str:
        return CPD_TYPES[self.cpd_type_code]

    @property
    def year(self) -> int:
        return self.act_date.year

    @property
    def semester(self) -> int:
        if self.act_date.month <= 6:
            return 1
        return 2

    @property
    def trimester(self) -> int:
        if self.act_date.month <= 3:
            return 1
        if self.act_date.month <= 6:
            return 2
        if self.act_date.month <= 9:
            return 3
        return 4

    @field_validator("act_date")
    @classmethod
    def ensure_date_range(cls, v):
        if v > date.today():
            raise ValueError("Cannot be in future")
        return v
