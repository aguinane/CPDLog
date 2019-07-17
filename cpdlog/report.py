import logging
from openpyxl import load_workbook
import attr
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from sqlalchemy import create_engine

from .cpd_rules import CPD_RULES, CPD_TYPES, CPD_MINS

log = logging.getLogger(__name__)


@attr.s
class CPDTotal(object):
    cpd_type = attr.ib()
    risk_hrs = attr.ib()
    business_hrs = attr.ib()
    practice_hrs = attr.ib()
    other_hrs = attr.ib()

    @property
    def total_hrs(self):
        total = self.risk_hrs + self.business_hrs + self.practice_hrs + self.other_hrs
        if not self.cpd_limit:
            return total  # No limits
        if self.cpd_limit > total:
            return total
        else:
            return self.cpd_limit

    @property
    def cpd_desc(self):
        return CPD_TYPES[self.cpd_type]["desc"]

    @property
    def cpd_long_desc(self):
        return CPD_TYPES[self.cpd_type]["desc_long"]

    @property
    def conditions(self):
        try:
            return CPD_TYPES[self.cpd_type]["conditions"]
        except KeyError:
            return ""

    @property
    def cpd_limit(self):
        try:
            return CPD_TYPES[self.cpd_type]["limit"]
        except KeyError:
            return None


def group_activities_by_cpd_type(activities, years=3):
    """ Group CPD activities by CPD Type """
    type_group = dict()
    for cpd_type in CPD_TYPES.keys():
        type_group[cpd_type] = list()
    for record in activities:
        cpd_type = record.cpd_category
        if not record.cpd_expired(years):
            type_group[cpd_type].append(record)
    return type_group


def sum_cpd_hours(activities):
    risk_hrs = 0
    business_hrs = 0
    practice_hrs = 0
    total_hrs = 0
    for record in activities:
        risk_hrs += record.risk_hrs
        business_hrs += record.business_hrs
        practice_hrs += record.practice_hrs
        total_hrs += record.total_hrs
    other_hrs = total_hrs - risk_hrs - business_hrs - practice_hrs
    return risk_hrs, business_hrs, practice_hrs, other_hrs


def get_cpd_totals(activities, years=3):
    """ Group CPD by FY and CPD Type """
    totals = list()
    cpd_group = group_activities_by_cpd_type(activities, years)
    for cpd_type in cpd_group:
        activities = cpd_group[cpd_type]
        risk_hrs, business_hrs, practice_hrs, other_hrs = sum_cpd_hours(activities)
        t = CPDTotal(cpd_type, risk_hrs, business_hrs, practice_hrs, other_hrs)
        totals.append(t)
    return totals


def build_summary_table(activities, years=3):
    """ Build a CPD summary table """
    type_summary = dict()
    totals = get_cpd_totals(activities, years)
    for row in totals:
        type_summary[row.cpd_type] = {
            "desc": row.cpd_desc,
            "long_desc": row.cpd_long_desc,
            "total_hrs": row.total_hrs,
            "limit": row.cpd_limit,
            "conditions": row.conditions,
        }
    area_summary = {
        "risk_hrs": sum(row.risk_hrs for row in totals),
        "business_hrs": sum(row.business_hrs for row in totals),
        "practice_hrs": sum(row.practice_hrs for row in totals),
        "other_hrs": sum(row.other_hrs for row in totals),
        "total_hrs": sum(row.total_hrs for row in totals),
    }
    return type_summary, area_summary


def yearly_hours(activities, years=4):
    """ Get hours by year grouping """
    group_data = dict()
    for record in activities:
        if not record.cpd_expired(years):
            yr_grp = record.yr_grp
            if yr_grp not in group_data.keys():
                group_data[yr_grp] = 0
            total_hrs = record.total_hrs
            group_data[yr_grp] += total_hrs
    return group_data


def combine_report_data(activities):
    """ Build CPD summaries """
    type_summary, area_summary = build_summary_table(activities)
    type_summary2, area_summary2 = build_summary_table(activities, years=2)
    yr_data = yearly_hours(activities)
    cpd_data = {
        "type_summary": type_summary,
        "area_summary": area_summary,
        "type_summary2": type_summary2,
        "area_summary2": area_summary2,
        "mins": CPD_MINS,
        "yr_data": yr_data,
    }
    return cpd_data
