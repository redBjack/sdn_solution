"""
Module that offers remote data fetching
"""
import urllib.request
import json
from http import HTTPStatus


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
        response = urllib.request.urlopen(url)
    except (ValueError, urllib.error.URLError):
        return None

    if response.status != HTTPStatus.OK:
        return None

    data = response.read()
    return json.loads(data)
