import http.client
import json
import pytest
import urllib.request
from mock import patch, MagicMock, call
from sdn.lib_get_data import get_data


@pytest.fixture(autouse=True)
def sleep_mock(mocker):
    """
    Skip sleeps in testing to speed it up
    """
    yield mocker.patch("time.sleep")


@pytest.fixture
def bad_response_mock():
    """
    Fixture that gives a mock for a bad response
    """
    urlopen_mock = MagicMock()
    # storing the underlying mock for test easy access
    urlopen_mock.response_mock = MagicMock(http.client.HTTPResponse)
    urlopen_mock.response_mock.status = 400
    urlopen_mock.response_mock.reason = "Oh this is baaaad!"
    urlopen_mock.__enter__.return_value = urlopen_mock.response_mock  # mocking the context manager
    yield urlopen_mock


def test_get_data_returns_none_for_badly_formed_url():
    # WHEN calling get_data with a badly formed url
    # THEN it returns None
    assert get_data("/bad/url") is None


def test_get_data_returns_none_for_nonexistent_url():
    # WHEN calling get_data with a nonexistent url
    # THEN it returns None
    assert get_data("http://this_url_does_not_exist.not_ever") is None


def test_get_data_returns_a_dict(test_url):
    # WHEN calling get_data on the test url
    response = get_data(test_url)

    # THEN it returns a valid dict object
    assert isinstance(response, dict)


def test_get_data_returns_none_fora_bad_http_response_status(test_url, bad_response_mock):
    # GIVEN that the response is not 200
    with patch("urllib.request.urlopen", return_value=bad_response_mock):
        # WHEN calling get_data
        response = get_data(test_url)

    # THEN it returns None
    assert response is None


def test_get_data_returns_none_if_read_gives_exception(test_url):
    # GIVEN that the response is unreadable and it raises HTTPException
    response_mock = MagicMock(http.client.HTTPResponse)
    response_mock.status = 200
    response_mock.read.side_effect = http.client.HTTPException("Cannot read")
    urlopen_mock = MagicMock()
    urlopen_mock.__enter__.return_value = response_mock  # mocking the context manager
    with patch("urllib.request.urlopen", return_value=urlopen_mock):
        # WHEN calling get_data
        response = get_data(test_url)

    # THEN the response is None
    assert response is None


def test_get_data_returns_none_if_json_gives_exception(test_url):
    # GIVEN that upon parsing the response an exception is raised
    with patch("json.loads", side_effect=json.JSONDecodeError("Bad json", doc="my doc", pos=11)):
        # WHEN calling get_data
        response = get_data(test_url)

    # THEN the response is None
    assert response is None


def test_get_data_retries_on_error(test_url, bad_response_mock):
    # GIVEN that the response is not 200
    with patch("urllib.request.urlopen", return_value=bad_response_mock):
        # WHEN calling get_data
        get_data(test_url)

    # THEN urllib.request.urlopen was called 6 times (first attempt + 5 retries)
    assert bad_response_mock.__enter__.call_count == 6


def test_get_data_sleeps_between_retries(test_url, sleep_mock):
    # GIVEN that upon parsing the response an exception is raised
    with patch("json.loads", side_effect=json.JSONDecodeError("Bad json", doc="my doc", pos=11)):
        # WHEN calling get_data
        get_data(test_url)

    # THEN sleep is only called 5 times (not 6)
    assert sleep_mock.call_count == 5


def test_get_data_stops_retrying_if_succeeds_and_returns_dict(test_url, bad_response_mock):
    # GIVEN that http response is bad a couple of times and a good one the third time
    bad_response_mock.__enter__.side_effect = [
        bad_response_mock.response_mock,    # the response 400
        bad_response_mock.response_mock,    # the response 400 at first retry
        urllib.request.urlopen(test_url)  # second retry - does the actual call
    ]
    with patch("urllib.request.urlopen", return_value=bad_response_mock):
        # WHEN calling get_data
        response = get_data(test_url)

    # THEN response is a dict
    assert isinstance(response, dict)
    # and urllib.request.urlopen was called 3 times
    assert bad_response_mock.__enter__.call_count == 3


def test_get_data_gives_expected_result_for_test_json(test_url, response_json_example):
    # WHEN calling get_data on the test url
    response = get_data(test_url)

    # THEN the response is exactly as expected (saved in the file)
    assert response_json_example == response  # comparing dicts


def test_get_data_sleeps_desired_amount_between_retries(test_url, sleep_mock):
    # GIVEN that upon parsing the response an exception is raised
    with patch("json.loads", side_effect=json.JSONDecodeError("Bad json", doc="my doc", pos=11)):
        # WHEN calling get_data with 4 retries and 2 seconds delay
        get_data(test_url, max_retries=4, delay_between_retries=2)

    # THEN sleep is only called 4 times
    assert sleep_mock.call_count == 4
    # each time with 2 seconds as argument
    sleep_mock.assert_has_calls([call(2)] * 4)
