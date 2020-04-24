"""
Conftest for pytest tests
"""
import pytest
import json
import os
from data_structures.datacenter import Datacenter


__DIR_PATH = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def response_json_example():
    with open(os.path.join(__DIR_PATH, "response.json")) as response_file:
        yield json.load(response_file)


@pytest.fixture
def expected_json():
    with open(os.path.join(__DIR_PATH, "expected.json")) as response_file:
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


@pytest.fixture
def test_url():
    yield "http://www.mocky.io/v2/5e539b332e00007c002dacbe"
