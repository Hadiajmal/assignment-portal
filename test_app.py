import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config["TESTING"] = True
    submissions.clear()
    with app.test_client() as c:
        yield c

GOOD = {
    "name": "Hadia Ajmal",
    "reg_no": "FA23-BSE-046",
    "title": "DevOps Lab",
    "url": "https://github.com/hadia/repo",
}

def test_valid_submission_saved(client):
    r = client.post("/", data=GOOD, follow_redirects=True)
    assert b"FA23-BSE-046" in r.data
    assert len(submissions) == 1

def test_missing_reg_no_rejected(client):
    r = client.post("/", data={**GOOD, "reg_no": ""})
    assert b"Missing registration number" in r.data
    assert len(submissions) == 0

def test_invalid_url_rejected(client):
    r = client.post("/", data={**GOOD, "url": "not-a-url"})
    assert b"Invalid submission URL" in r.data
    assert len(submissions) == 0