"""
Module that offers remote data fetching
"""
import urllib.request
import json
import logging
from http import HTTPStatus
import http.client

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
        with urllib.request.urlopen(url) as response:
            if response.status != HTTPStatus.OK:
                __LOGGER.error("Bad response %s, %s", response.status, response.reason)
                return None

            data = response.read()
    except (ValueError, urllib.error.URLError, http.client.HTTPException) as exc:
        __LOGGER.error("Get Data failed \n%s", exc)
        return None

    return json.loads(data)
