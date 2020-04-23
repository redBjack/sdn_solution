from sdn.lib_get_data import get_data


def test_get_data_returns_none():
    # WHEN calling get_data with a fake url
    # THEN it returns None
    assert get_data("/fake/url") is None
