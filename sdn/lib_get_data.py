"""
Module that offers remote data fetching
"""
import urllib.request
import json
import logging
from http import HTTPStatus
import http.client
from retry.api import retry_call

__LOGGER = logging.getLogger(__name__)


def get_data(url, max_retries=5, delay_between_retries=1):
    """
    Fetch the data from given URL and return it as a JSON object.
​
    Args:
        url (str): The url to be fetched.
        max_retries (int): Number of retries.
        delay_between_retries (int): Delay between retries in seconds.
    Returns:
        data (dict)
    """
    try:
        return retry_call(
            __get_data_attempt, fargs=[url], tries=max_retries+1, delay=delay_between_retries
        )
    except (
            ValueError,                    # raised by urlopen
            urllib.error.URLError,         # raised by urlopen
            http.client.HTTPException,     # raised by read
            json.decoder.JSONDecodeError   # raised by loads
    ) as exc:
        __LOGGER.error("Get Data failed \n%s", exc)
        return None


def __get_data_attempt(url):
    """
    Fetch the data from given URL and return it as a JSON object with no retries
​
    Args:
        url (str): The url to be fetched.
    Returns:
        data (dict)
    """
    with urllib.request.urlopen(url) as response:
        if response.status != HTTPStatus.OK:
            raise ValueError(f"Bad response {response.status}, {response.reason}")

        data = response.read()

    return json.loads(data)
