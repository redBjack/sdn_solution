from ipaddress import IPv4Network
from data_structures.network_collection import NetworkCollection
from data_structures.entry import Entry


def test_network_collection_inits_network_ip():
    # WHEN creating a NetworkCollection instance
    network_collection = NetworkCollection("192.168.0.0/24", [])

    # THEN the ipv4_network field is a valid ip field
    assert isinstance(network_collection.ipv4_network, IPv4Network)


def test_network_collection_init_entries():
    # WHEN creating a NetworkCollection instance
    network_collection = NetworkCollection(
        "192.168.0.0/24",
        [
            {
                "address": "255.255.255.0",
                "available": True,
                "last_used": "30/01/20 17:00:00"
            },
            {
                "address": "192.168.0.1",
                "available": False,
                "last_used": "20/12/19 17:10:01"
            }
        ]
    )

    # THEN the entries field is properly initialized
    assert isinstance(network_collection.entries, list)
    assert len(network_collection.entries) == 2
    assert all([isinstance(entry, Entry) for entry in network_collection.entries])
