from ipaddress import IPv4Network
from data_structures.network_collection import NetworkCollection


def test_network_collection_inits_network_ip():
    # WHEN creating a NetworkCollection instance
    network_collection = NetworkCollection("192.168.0.0/24", [])

    # THEN the ipv4_network field is a valid ip field
    assert isinstance(network_collection.ipv4_network, IPv4Network)
