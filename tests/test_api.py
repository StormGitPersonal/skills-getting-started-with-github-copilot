import copy
from pathlib import Path
import sys

sys.path.append(str(Path.cwd() / "src"))

import pytest
from fastapi.testclient import TestClient

import app


# Keep an original snapshot to reset in-memory data between tests
ORIG_ACTIVITIES = copy.deepcopy(app.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities before each test
    app.activities = copy.deepcopy(ORIG_ACTIVITIES)
    yield


client = TestClient(app.app)


def test_get_activities():
    r = client.get('/activities')
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_and_duplicate():
    activity = 'Programming Class'
    email = 'integtest@example.com'

    # initial signup
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in app.activities[activity]['participants']

    # duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400


def test_signup_nonexistent_activity():
    r = client.post('/activities/NoSuchActivity/signup?email=a@b.com')
    assert r.status_code == 404


def test_remove_participant_flow():
    activity = 'Gym Class'
    email = 'john@mergington.edu'

    # Ensure participant exists
    assert email in app.activities[activity]['participants']

    # Remove participant
    r = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r.status_code == 200
    assert email not in app.activities[activity]['participants']

    # Removing again should return 404
    r2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r2.status_code == 404
