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
