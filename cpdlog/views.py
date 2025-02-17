import json

import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, redirect, render_template, request, url_for

from .activity import Activity
from .logfile import load_logfile, save_logfile
from .summary import get_cpd_summary

app = Flask(__name__)


def build_quarters_graph_json(quarter_totals: dict):
    df = pd.DataFrame(list(quarter_totals.items()), columns=["Quarter", "Hours"])
    fig = px.bar(df, x="Quarter", y="Hours")
    fig.add_shape(
        type="line",
        xref="paper",
        x0=0,
        x1=1,
        yref="y",
        y0=12.5,
        y1=12.5,
        line=dict(color="Red", dash="dot"),
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def build_types_graph_json(cpd_type_totals: dict):
    df = pd.DataFrame(list(cpd_type_totals.items()), columns=["CPD Type", "Hours"])
    fig = px.bar(df, x="Hours", y="CPD Type", orientation="h")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
def home():
    logfile = app.config["logfile"]
    activities = load_logfile(logfile)
    summary = get_cpd_summary(logfile, years=3)
    summary2 = get_cpd_summary(logfile, years=2)
    expiring = summary["total_hours"] - summary2["total_hours"]
    quarters_graph_json = build_quarters_graph_json(summary["quarter_totals"])
    types_graph_json = build_types_graph_json(summary["cpd_type_totals"])
    return render_template(
        "index.html",
        logfile=logfile,
        activities=activities,
        summary=summary,
        expiring=expiring,
        quarters_graph_json=quarters_graph_json,
        types_graph_json=types_graph_json,
    )


@app.route("/new_activity", methods=["POST"])
def new_activity():
    """Create new CPD activity"""
    logfile = app.config["logfile"]
    act = Activity(
        act_date=request.form["date"],
        topic=request.form["topic"],
        cpd_hours=request.form["duration"],
        cpd_type=request.form["cpd_category"],
        technical=request.form["technical"],
        provider=request.form["provider"],
        learning_outcome=request.form["learning_outcome"],
        notes=request.form["notes"],
    )
    save_logfile(logfile, activities=[act], append=True)
    return redirect(url_for("home"))
