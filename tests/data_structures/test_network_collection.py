import pytest
from ipaddress import IPv4Network, IPv4Address
from data_structures.network_collection import NetworkCollection
from data_structures.entry import Entry


@pytest.fixture
def two_entries_collection():
    yield NetworkCollection(
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


def test_network_collection_inits_network_ip():
    # WHEN creating a NetworkCollection instance
    network_collection = NetworkCollection("192.168.0.0/24", [])

    # THEN the ipv4_network field is a valid ip field
    assert isinstance(network_collection.ipv4_network, IPv4Network)


def test_network_collection_init_entries(two_entries_collection):
    # WHEN creating a NetworkCollection instance (in fixture)

    # THEN the entries field is properly initialized
    assert isinstance(two_entries_collection.entries, list)
    assert len(two_entries_collection.entries) == 2
    assert all([isinstance(entry, Entry) for entry in two_entries_collection.entries])


def test_network_collection_inits_from_json_example(response_json_example):
    # GIVEN some data from the example json
    some_networks_data = response_json_example["Berlin"]["BER-1"]["networks"]

    # WHEN creating network collection instances based on these entries
    network_collections = [
        NetworkCollection(network, entries)
        for network, entries in some_networks_data.items()
    ]

    # THEN all netowrk collections are valid
    assert len(network_collections) == 2
    assert all([
        isinstance(network_collection.ipv4_network, IPv4Network)
        for network_collection in network_collections
        ])
    assert all([
        isinstance(network_collection.entries, list)
        and
        all([isinstance(entry, Entry) for entry in network_collection.entries])
        for network_collection in network_collections
    ])


# TODO: fix failing cases
__VALID_IP_NETWORK_PAIR = {
    ("192.168.0.0/24", "192.168.0.1"): True,
    ("192.168.0.0/24", "192.168.1.1"): False,
    ("192.168.1.0/24", "192.168.1.255"): False,
    ("192.168.0.0/24", "192.167.0.1"): False,
    ("192.168.0.0/24", "192.168.0.0"): False,
    ("192.168.0.0/16", "192.168.1.1"): True,
    ("192.168.0.0/16", "192.167.1.1"): False,
    ("192.168.0.0/16", "192.168.118.1"): True,
    ("192.0.0.0/8", "192.16.118.1"): True,
    ("192.0.0.0/8", "192.16.0.0"): True,
    ("192.0.0.0/8", "192.16.0.255"): True,
    ("192.0.0.0/8", "192.255.255.255"): False,
    ("192.0.0.0/8", "193.0.1.2"): False,
    ("192.0.116.0/22", "192.0.119.254"): True,
    ("192.0.116.0/22", "192.0.119.255"): False,
    ("192.0.116.0/22", "192.0.118.255"): True,
    ("192.0.116.0/22", "192.0.117.156"): True,
    ("192.0.116.0/22", "192.0.120.156"): False,
}


@pytest.mark.parametrize("network, addr", __VALID_IP_NETWORK_PAIR)
def test_is_address_in_network_returns_proper_value(network, addr):
    # GIVEN a network collection instance based on the input network
    network_collection = NetworkCollection(network, [])

    # WHEN calling is_address_in_network on the input address
    valid = network_collection.is_address_in_network(IPv4Address(addr))

    # THEN it returns proper value
    expected = __VALID_IP_NETWORK_PAIR[(network, addr)]
    assert valid is expected,\
        f"Address {addr} should {'' if expected else 'not '}be part of network {network}."


def test_remove_invalid_records_removes_entry(two_entries_collection):
    # GIVEN network collection with two entries (one valid, one not valid)
    assert len(two_entries_collection.entries) == 2

    # WHEN calling remove_invalid_records on that collection
    two_entries_collection.remove_invalid_records()

    # THEN one entry has been removed
    assert len(two_entries_collection.entries) == 1


def test_remove_invalid_records_with_json_example(json_example_data_centers):
    # GIVEN a set of data centers from the json example
    # with 2 networks in Berlin first cluster
    networks = json_example_data_centers["Berlin"].clusters[0].networks
    assert len(networks) == 2
    # with 10 and 5 entries respectively
    assert len(networks[0].entries) == 10
    assert len(networks[1].entries) == 5

    # WHEN calling remove_invalid_records
    for network in networks:
        network.remove_invalid_records()

    # THEN only valid entries remain (4 and 2 respectively)
    assert len(networks[0].entries) == 4
    assert len(networks[1].entries) == 2
