from data_structures.datacenter import Datacenter
from data_structures.cluster import Cluster


def test_datacenter_inits_name():
    # WHEN a Datacenter is created
    datacenter = Datacenter("Berlin", {})

    # THEN name is initialized
    assert datacenter.name == "Berlin"


def test_datacenter_inits_clusters():
    # WHEN a Datacenter is created
    datacenter = Datacenter(
        "Berlin",
        {
            "BER-1": {
                "security_level": 1,
                "networks": {
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
                }
            },
            "BER-203": {
                "security_level": 3,
                "networks": {
                    "192.168.10.0/24": [
                        {
                            "address": "192.168.10.8",
                            "available": True,
                            "last_used": "30/01/20 17:00:00"
                        }
                    ]
                }
            }
        }
    )

    # THEN clusters field is properly initialized
    assert isinstance(datacenter.clusters, list)
    assert len(datacenter.clusters) == 2
    assert all([isinstance(cluster, Cluster) for cluster in datacenter.clusters])


def test_datacenter_inits_from_json_example(response_json_example):
    # WHEN creating network cluster instances based on example entries
    data_centers = {
        name: Datacenter(name, cluster_data)
        for name, cluster_data in response_json_example.items()
    }

    # THEN all datacenters are valid
    assert len(data_centers) == 2
    assert all([isinstance(data_center, Datacenter) for data_center in data_centers.values()])
    assert all([
        isinstance(data_center.name, str)
        and
        isinstance(data_center.clusters, list)
        and
        all([isinstance(cluster, Cluster) for cluster in data_center.clusters])
        for data_center in data_centers.values()
    ])
    # and this random value is correct
    assert data_centers["Berlin"].clusters[1].networks[1].entries[2].address == "192.168.11.522"
