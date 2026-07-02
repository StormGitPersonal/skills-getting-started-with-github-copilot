import copy
from pathlib import Path
import sys

sys.path.append(str(Path.cwd() / "src"))

import pytest
import app


# Snapshot original activities and reset before each test
ORIG_ACTIVITIES = copy.deepcopy(app.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app.activities = copy.deepcopy(ORIG_ACTIVITIES)
    yield
