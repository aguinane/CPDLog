import os
from flask import render_template
from flask import flash
from flask import url_for, redirect
from pathlib import Path
from . import app
from cpdlog.forms import FileForm, ActivityForm
from cpdlog.model import Activities, SubjectArea
from cpdlog.model import get_cpd_activities, get_cpd_providers, get_locations
from cpdlog.report import combine_report_data
from cpdlog.migrate_ea import import_ea_cpd_activities
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///data/cpdlog.db"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summary")
def summary():

    activities = get_cpd_activities(DB_URL)
    report_data = combine_report_data(activities)
    return render_template("summary.html", **report_data)


@app.route("/activities")
def activities():
    activities = get_cpd_activities(DB_URL)
    return render_template("activities.html", activities=activities)


@app.route("/new_activity", methods=["GET", "POST"])
def new_activity():
    """ Import meter data """

    form = ActivityForm()
    if form.validate_on_submit():
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        activity = Activities(
            cpd_category=form.cpd_category.data,
            start_date=form.start_date.data,
            end_date=form.start_date.data,
            act_type=form.act_type.data,
            topic=form.topic.data,
            provider=form.provider.data,
            location=form.location.data,
            duration=form.duration.data,
            notes=form.notes.data,
            ext_ref=None,
        )
        session.add(activity)
        session.commit()
        act_id = activity.act_id
        """
        area = SubjectArea(
            act_id=act_id,
            practice_hrs=form.area_hrs.data,
            risk_hrs=form.risk_hrs.data,
            business_hrs=form.bus_hrs.data,
        )
        session.add(area)
        """
        session.commit()

        flash("New activity created!", category="success")
        return redirect(url_for("index"))

    providers = get_cpd_providers(DB_URL)
    locations = get_locations(DB_URL)

    return render_template(
        "activity_new.html", form=form, providers=providers, locations=locations
    )


@app.route("/import_ea", methods=["GET", "POST"])
def import_ea():
    """ Import meter data """

    form = FileForm()
    if form.validate_on_submit():
        file_path = os.path.abspath("data/imported.xlsx")
        form.upload_file.data.save(file_path)
        import_ea_cpd_activities(DB_URL, file_path)
        flash("Activities imported", category="success")
        return redirect(url_for("index"))

    return render_template("importea.html", form=form)
