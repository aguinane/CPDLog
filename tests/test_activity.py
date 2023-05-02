from datetime import date
import tempfile
from pathlib import Path
from cpdlog import Activity
from cpdlog import save_logfile, load_logfile
from cpdlog.logfile import check_create_logfile


def test_example_act():
    """Create an Activity and test attributes"""

    today = date.today()
    act = Activity(
        act_date=today,
        topic="my topic",
        cpd_hours=5,
        cpd_type="B",
        learning_outcome="I learnt things",
    )

    assert len(act.act_id) > 1
    assert act.expired() is False
    assert act.year == today.year
    assert act.cpd_type_desc == "Industry Education"

    with tempfile.TemporaryDirectory() as tmpdir:
        logfile = Path(tmpdir) / "cpdlog.csv"
        save_logfile(logfile, [act], append=True)
        num_act = check_create_logfile(logfile)
        assert num_act == 1


def test_empty_logfile():
    """Create an logfile"""

    with tempfile.TemporaryDirectory() as tmpdir:
        logfile = Path(tmpdir) / "cpdlog.csv"
        save_logfile(logfile, [], append=False)
        num_act = check_create_logfile(logfile)
        assert num_act == 0


def test_example_logfile():
    """Use existing logfile"""

    logfile = Path("examples") / "cpdlog.csv"
    activities = load_logfile(logfile)
    assert len(activities) == 2
    first = activities[-1]
    assert first.act_id == "441DF80B"
    assert first.act_date == date(2023, 1, 6)
    assert first.topic == "Example Training Course"
    assert first.technical is False
