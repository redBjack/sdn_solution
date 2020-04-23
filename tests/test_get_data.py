import http.client
import json
from mock import patch, MagicMock
from sdn.lib_get_data import get_data

__TEST_URL = "http://www.mocky.io/v2/5e539b332e00007c002dacbe"


def test_get_data_returns_none_for_badly_formed_url():
    # WHEN calling get_data with a badly formed url
    # THEN it returns None
    assert get_data("/bad/url") is None


def test_get_data_returns_none_for_nonexistent_url():
    # WHEN calling get_data with a nonexistent url
    # THEN it returns None
    assert get_data("http://this_url_does_not_exist.not_ever") is None


def test_get_data_returns_a_dict():
    # WHEN calling get_data on the test url
    response = get_data(__TEST_URL)

    # THEN it returns a valid dict object
    assert isinstance(response, dict)


def test_get_data_returns_none_fora_bad_http_response_status():
    # GIVEN that the response is not 200
    response_mock = MagicMock(http.client.HTTPResponse)
    response_mock.status = 400
    response_mock.reason = "Bad something something"
    urlopen_mock = MagicMock()
    urlopen_mock.__enter__.return_value = response_mock  # mocking the context manager
    with patch("urllib.request.urlopen", return_value=urlopen_mock):
        # WHEN calling get_data
        response = get_data(__TEST_URL)

    # THEN it returns None
    assert response is None


def test_get_data_returns_none_if_read_gives_exception():
    # GIVEN that the response is unreadable and it raises HTTPException
    response_mock = MagicMock(http.client.HTTPResponse)
    response_mock.status = 200
    response_mock.read.side_effect = http.client.HTTPException("Cannot read")
    urlopen_mock = MagicMock()
    urlopen_mock.__enter__.return_value = response_mock  # mocking the context manager
    with patch("urllib.request.urlopen", return_value=urlopen_mock):
        # WHEN calling get_data
        response = get_data(__TEST_URL)

    # THEN the response is None
    assert response is None


def test_get_data_returns_none_if_json_gives_exception():
    # GIVEN that upon parsing the response an exception is raised
    with patch("json.loads", side_effect=json.JSONDecodeError("Bad json", doc="my doc", pos=11)):
        # WHEN calling get_data
        response = get_data(__TEST_URL)

    # THEN the response is None
    assert response is None
