import os
import webbrowser
from datetime import datetime
from pathlib import Path

import typer
from cheroot.wsgi import Server

from .activity import CPD_TYPES, Activity, CPDType
from .logfile import check_create_logfile, load_logfile, save_logfile
from .summary import get_cpd_summary
from .views import app as webapp

app = typer.Typer()


DEFAULT_PATH = Path(os.getenv("CPD_LOG_FILE", "cpdlog.csv"))
CPD_TYPE_PROMPT = "\n".join([f"{i}: {j}" for i, j in CPD_TYPES.items()]) + "\n"
today = datetime.now().strftime("%Y-%m-%d")


@app.command()
def where():
    """Show the path to the default logfile"""
    logfile = DEFAULT_PATH.resolve()
    typer.echo(f"The logfile will default to {logfile}")
    typer.echo("This can be set by the CPD_LOG_FILE environment variable")


@app.command()
def new(
    logfile: Path = DEFAULT_PATH,
    date: datetime = typer.Option(today, prompt=True),
    topic: str = typer.Option(..., prompt=True),
    hours: float = typer.Option(..., prompt=True),
    cpd_type: CPDType = typer.Option("B", prompt=CPD_TYPE_PROMPT, case_sensitive=False),
    technical: bool = typer.Option(False, prompt=True),
    provider: str = typer.Option("", prompt=True),
    learning_outcome: str = typer.Option(..., prompt=True),
):
    """Add a new activity to the CPD Log"""
    check_create_logfile(logfile)

    act = Activity(
        act_date=date,
        topic=topic,
        cpd_hours=hours,
        cpd_type=cpd_type,
        technical=technical,
        provider=provider,
        learning_outcome=learning_outcome,
    )
    save_logfile(logfile, [act], append=True)
    typer.echo(f"Added entry to {logfile}")


@app.command()
def recent(logfile: Path = DEFAULT_PATH, num: int = 5):
    """Show the most recent activities from a CPD Log"""
    num_act = check_create_logfile(logfile)
    typer.echo(f"There are {num_act} entries in the CPD Log File '{logfile}'")
    activities = load_logfile(logfile)
    for act in activities[0:num]:
        line = f"{act.act_date.isoformat()}\t{act.cpd_hours}hrs\t{act.topic}"
        typer.echo(line)


@app.command()
def summary(logfile: Path = DEFAULT_PATH):
    """Calculate a summary of the CPD Log"""
    num_act = check_create_logfile(logfile)
    typer.echo(f"There are {num_act} entries in the CPD Log File '{logfile}'")

    sum3 = get_cpd_summary(logfile, years=3)
    sum2 = get_cpd_summary(logfile, years=2)
    sum1 = get_cpd_summary(logfile, years=1)

    t1 = sum1["total_hours"]
    t2 = sum2["total_hours"] - t1
    t3 = sum3["total_hours"] - t2
    tall = sum3["total_hours"]
    typer.echo(f"Total for last 3 years: {tall}hrs")
    typer.echo(f"Y1: {t1}hrs\tY2: {t2}hrs\tY3: {t3}hrs")


@app.command()
def gui(logfile: Path = DEFAULT_PATH, port: int = 5003):
    """Open a webpage viewer of the CPD Log"""
    num_act = check_create_logfile(logfile)
    typer.echo(f"There are {num_act} entries in the CPD Log File '{logfile}'")
    host = "127.0.0.1"

    url = f"http://{host}:{port}"
    typer.echo(f"Starting CPDLog on {url}")

    webbrowser.open(url, new=2)

    webapp.config["logfile"] = logfile
    server = Server((host, port), webapp)
    server.start()
