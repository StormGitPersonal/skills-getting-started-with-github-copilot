from pathlib import Path
import sys
import pytest

# Ensure src is importable
sys.path.append(str(Path.cwd() / "src"))

from fastapi import HTTPException
import app


def test_signup_duplicate_raises():
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    with pytest.raises(HTTPException) as exc:
        app.signup_for_activity(activity, existing_email)
    assert exc.value.status_code == 400
    assert "already signed up" in str(exc.value.detail)


def test_signup_new_succeeds():
    activity = "Programming Class"
    new_email = "teststudent@example.com"
    # Ensure clean state
    participants = app.activities[activity]["participants"]
    if new_email in participants:
        participants.remove(new_email)

    res = app.signup_for_activity(activity, new_email)
    assert res["message"] == f"Signed up {new_email} for {activity}"
    assert new_email in app.activities[activity]["participants"]
