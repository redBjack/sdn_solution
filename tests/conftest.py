"""
Conftest for pytest tests
"""
import pytest
import json
from data_structures.datacenter import Datacenter


@pytest.fixture
def response_json_example():
    with open("tests/response.json") as response_file:
        yield json.load(response_file)


@pytest.fixture
def json_example_data_centers(response_json_example):
    """
    Gives a dict with the data centers from the json example indexed by name
    """
    yield {
        name: Datacenter(name, cluster_data)
        for name, cluster_data in response_json_example.items()
    }
