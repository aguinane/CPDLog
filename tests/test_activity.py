from datetime import datetime
import tempfile
from pathlib import Path
from cpdlog import Activity
from cpdlog import save_logfile
from cpdlog.logfile import check_create_logfile


def test_example_act():
    """Create an Activity and test attributes"""

    today = datetime.now().date()
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
