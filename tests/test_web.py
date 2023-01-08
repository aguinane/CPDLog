from cpdlog.views import app


app.config["logfile"] = "examples/cpdlog.csv"
test_site = app.test_client()


def test_index():
    response = test_site.get("/")
    assert response.status_code == 200
