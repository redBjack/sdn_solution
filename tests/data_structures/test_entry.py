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
