import os
from flask import render_template
from flask import flash
from flask import url_for, redirect
from pathlib import Path
from . import app
from cpdlog.forms import FileForm
from cpdlog.model import get_cpd_activities
from cpdlog.report import combine_report_data
from cpdlog.migrate_ea import import_ea_cpd_activities

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