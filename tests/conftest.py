import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

@pytest.fixture(autouse=True)
def preserve_activities():
    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)


@pytest.fixture
def client():
    return TestClient(app_module.app)
