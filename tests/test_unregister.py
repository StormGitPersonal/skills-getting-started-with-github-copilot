from pathlib import Path
import sys
import pytest

sys.path.append(str(Path.cwd() / "src"))

from fastapi import HTTPException
import app


def test_remove_existing_participant():
    activity = "Gym Class"
    email = "john@mergington.edu"
    # ensure present
    assert email in app.activities[activity]["participants"]
    res = app.remove_participant(activity, email)
    assert res["message"] == f"Removed {email} from {activity}"
    assert email not in app.activities[activity]["participants"]


def test_remove_nonexistent_participant_raises():
    activity = "Gym Class"
    email = "not-a-person@example.com"
    with pytest.raises(HTTPException) as exc:
        app.remove_participant(activity, email)
    assert exc.value.status_code == 404
