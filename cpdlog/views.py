
import altair as alt
import polars as pl
from flask import Flask, redirect, render_template, request, url_for

from .activity import Activity
from .logfile import load_logfile, save_logfile
from .summary import get_cpd_summary

app = Flask(__name__)


def build_quarters_graph(quarter_totals: dict):
    data = []
    for quarter, hours in quarter_totals.items():
        data.append({"Quarter": quarter, "Hours": hours})
    df = pl.DataFrame(data)
    bar = alt.Chart(df).mark_bar().encode(x=alt.X("Quarter:N"), y=alt.Y("Hours:Q"))
    rule_df = pl.DataFrame({"Hours": [12.5]})
    rule = (
        alt.Chart(rule_df)
        .mark_rule(color="red", strokeDash=[4, 4])
        .encode(y=alt.Y("Hours:Q"))
    )
    chart = (bar + rule).properties(width=600, height=300)
    return chart.to_json()


def build_types_graph(cpd_type_totals: dict):
    data = []
    for cpd_type, hours in cpd_type_totals.items():
        data.append({"CPD Type": cpd_type, "Hours": hours})
    df = pl.DataFrame(data)
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("Hours:Q"),
            y=alt.Y("CPD Type:N", sort=alt.SortField("Hours", order="descending")),
        )
        .properties(width=600, height=300)
    )
    return chart.to_json()


@app.route("/")
def home():
    logfile = app.config["logfile"]
    activities = load_logfile(logfile)
    summary = get_cpd_summary(logfile, years=3)
    summary2 = get_cpd_summary(logfile, years=2)
    expiring = summary["total_hours"] - summary2["total_hours"]
    quarters_graph = build_quarters_graph(summary["quarter_totals"])
    types_graph = build_types_graph(summary["cpd_type_totals"])
    return render_template(
        "index.html",
        logfile=logfile,
        activities=activities,
        summary=summary,
        expiring=expiring,
        quarters_graph=quarters_graph,
        types_graph=types_graph,
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
