from api.app import create_app
import pytest

@pytest.fixture
def hello():
    return create_app()
