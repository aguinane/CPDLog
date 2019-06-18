import pytoml as toml
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired
from wtforms import StringField, SelectField, DateField, FloatField, TextAreaField

from .cpd_rules import CPD_RULES,CPD_TYPES


class FileForm(FlaskForm):
    """ Upload form to specify import file """

    upload_file = FileField("Data File", validators=[DataRequired()])


class ActivityForm(FlaskForm):
    """ Form for creating new activity """

    cpd_categories = []
    for cat in CPD_TYPES.keys():
        cat_desc = "{}: {}".format(cat, CPD_TYPES[cat]["desc"])
        cpd_categories.append((cat, cat_desc))
    cpd_category = SelectField(u"CPD Category", choices=cpd_categories)

    act_types = []
    for act in sorted(CPD_RULES['activity_types']):
        act_types.append((act, act))
    act_type = SelectField(u"Activity Type", choices=act_types)

    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    duration = FloatField("Duration (hrs)", validators=[DataRequired()])
    topic = StringField("Topic", validators=[DataRequired()])
    provider = StringField("Provider", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    notes = TextAreaField("Learning Outcomes and Notes", validators=[DataRequired()])
