from data_structures.entry import Entry


def test_entry_inits_address():
    # WHEN creating Entry instance
    entry = Entry("192.168.1.1", True, "30/01/20 17:00:00")

    # THEN entry address is initialized
    assert entry.address == "192.168.1.1"
