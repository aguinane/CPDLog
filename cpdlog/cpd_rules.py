import os
import pytoml as toml

thisdir = os.path.dirname(os.path.abspath(__file__))
cpd_rules = os.path.join(thisdir, 'cpd_rules.toml')
with open(cpd_rules, 'rb') as stream:
    CPD_RULES = toml.load(stream)
    CPD_TYPES = CPD_RULES['cpd_types']

CPD_MINS = {
    "yrs": CPD_RULES['cpd_period_yrs'],
    "total": CPD_RULES['cpd_hrs_total'],
    "risk": CPD_RULES['cpd_hrs_risk'],
    "area": CPD_RULES['cpd_hrs_area'],
    "bus": CPD_RULES['cpd_hrs_business'],
}
