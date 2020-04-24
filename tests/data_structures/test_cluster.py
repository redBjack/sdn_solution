from data_structures.cluster import Cluster
from data_structures.network_collection import NetworkCollection


def test_cluster_inits_name():
    # WHEN creating an instance of Cluster
    cluster = Cluster("BER-1", {}, 1)

    # THEN name is properly initialized
    assert cluster.name == "BER-1"


def test_cluster_inits_networks():
    # WHEN creating an instance of Cluster
    cluster = Cluster(
        "BER-1",
        {
            "192.168.0.0/24": [
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
            ],
            "10.0.8.0/22": [
                {
                    "address": "10.0.11.254",
                    "available": True,
                    "last_used": "30/01/20 17:00:00"
                },
            ]
        },
        1
    )

    # THEN networks field is properly initialized
    assert isinstance(cluster.networks, list)
    assert len(cluster.networks) == 2
    assert all([isinstance(network, NetworkCollection) for network in cluster.networks])
    assert cluster.networks[0].entries[1].last_used.year == 2019


def test_inits_cluster_security_level():
    # WHEN creating an instance of Cluster
    cluster = Cluster("BER-1", {}, 1)

    # THEN security_level is properly initialized
    assert cluster.security_level == 1


