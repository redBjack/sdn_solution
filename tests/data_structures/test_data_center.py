from data_structures.datacenter import Datacenter


def test_datacenter_inits_name():
    # WHEN a Datacenter is created
    datacenter = Datacenter("Berlin", {})

    # THEN name is initialized
    assert datacenter.name == "Berlin"
