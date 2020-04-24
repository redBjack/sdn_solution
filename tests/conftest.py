"""
Conftest for pytest tests
"""
import pytest
import json


@pytest.fixture
def response_json_example():
    with open("tests/response.json") as response_file:
        yield json.load(response_file)
