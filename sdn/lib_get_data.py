"""
Module that offers remote data fetching
"""
import urllib.request
import json
import logging
from http import HTTPStatus
import http.client
import time

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
    for retry in range(max_retries + 1):
        if retry > 0:
            __LOGGER.info("Previous run failed, retrying - attempt %s", retry)
            time.sleep(delay_between_retries)
        try:
            return __get_data_attempt(url)
        except (
                ValueError,                    # raised by urlopen
                urllib.error.URLError,         # raised by urlopen
                http.client.HTTPException,     # raised by read
                json.decoder.JSONDecodeError   # raised by loads
        ) as exc:
            __LOGGER.error("Get Data failed \n%s", exc)
            continue

    return None


def __get_data_attempt(url):
    with urllib.request.urlopen(url) as response:
        if response.status != HTTPStatus.OK:
            raise ValueError(f"Bad response {response.status}, {response.reason}")

        data = response.read()

    return json.loads(data)
