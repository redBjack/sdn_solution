import pytest
from datetime import datetime
from data_structures.entry import Entry


def test_entry_inits_address():
    # WHEN creating Entry instance
    entry = Entry("192.168.1.1", True, "30/01/20 17:00:00")

    # THEN entry address is initialized
    assert entry.address == "192.168.1.1"


def test_entry_inits_available_field():
    # WHEN creating an Entry instance
    entry = Entry("192.168.1.1", True, "30/01/20 17:00:00")

    # THEN entry availabe is initialized
    assert entry.available is True


def test_entry_inits_last_used_field():
    # WHEN creating an Entry instance
    entry = Entry("192.168.1.1", True, "30/01/20 17:02:09")

    # THEN entry last_used is initialized
    assert isinstance(entry.last_used, datetime)
    assert entry.last_used.year == 2020
    assert entry.last_used.month == 1
    assert entry.last_used.day == 30
    assert entry.last_used.hour == 17
    assert entry.last_used.minute == 2
    assert entry.last_used.second == 9


def test_entry_inits_from_json_example(response_json_example):
    # GIVEN some data from th example json
    some_entries_data = response_json_example["Berlin"]["BER-1"]["networks"]["192.168.0.0/24"]

    # WHEN creating entry instances based on these entries
    entries = [
        Entry(entry_data["address"], entry_data["available"], entry_data["last_used"])
        for entry_data in some_entries_data
    ]

    # THEN all entries are valid
    for entry in entries:
        assert isinstance(entry.address, str)
        assert isinstance(entry.available, bool)
        assert isinstance(entry.last_used, datetime)


__VALID_IP_ADDRESS = {
    "1.1.1.1": True,
    "10.1.256.1": False,
    "1.1.1": False,
    "255.255.255.255": True,
    "0.0.0.0": True,
    "1.2.3.3.5": False,
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334": False,
    "30-65-EC-6F-C4-58": False,
    "1.1.1,1": False,
    "1A.1.1.1": False,
    "FF.FF.FF.FF": False,
    "-1.1.1.1": False
}


@pytest.mark.parametrize("address", __VALID_IP_ADDRESS)
def test_has_valid_address_returns_proper_value(address):
    # GIVEN an Entry instance with the test address
    entry = Entry(address, True, "30/01/20 17:00:00")

    # WHEN calling has_valid_address
    # THEN it returns the proper value
    expected = __VALID_IP_ADDRESS[address]
    assert entry.has_valid_address() is expected,\
        f"Address {address} should {'' if expected else 'not '}be valid."


def test_entry_with_smaller_ip_is_smaller():
    # GIVEN and entry with ip 192.168.1.1
    entry1 = Entry("192.168.1.1", True, "30/01/20 17:02:09")
    # and one with 192.168.1.2
    entry2 = Entry("192.168.1.2", True, "30/01/20 17:02:09")

    # WHEN comparing them
    # THEN the one with 192.168.1.1 is smaller
    assert entry1 < entry2


def test_entry_with_bigger_ip_is_bigger():
    # GIVEN and entry with ip 192.168.1.1
    entry1 = Entry("192.168.1.1", True, "30/01/20 17:02:09")
    # and one with 192.168.2.1
    entry2 = Entry("192.168.2.1", True, "30/01/20 17:02:09")

    # WHEN comparing them
    # THEN the one with 192.168.2.1 is bigger
    assert entry2 > entry1


def test_entry_with_smaller_ip_is_smaller_or_equal():
    # GIVEN and entry with ip 192.167.1.1
    entry1 = Entry("192.167.1.1", True, "30/01/20 17:02:09")
    # and one with 192.168.1.1
    entry2 = Entry("192.168.1.1", True, "30/01/20 17:02:09")

    # WHEN comparing them
    # THEN the one with 192.167.1.11 is smaller or equal
    assert entry1 <= entry2


def test_entry_with_same_ip_is_smaller_or_equal():
    # GIVEN and entry with ip 192.168.1.1
    entry1 = Entry("192.168.1.1", True, "30/01/20 17:02:09")
    # and one with 192.168.1.1
    entry2 = Entry("192.168.1.1", True, "30/01/20 17:02:09")

    # WHEN comparing them
    # THEN <= works both ways
    assert entry1 <= entry2 <= entry1
