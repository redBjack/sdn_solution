import pytest
from data_structures.datacenter import Datacenter
from data_structures.cluster import Cluster


@pytest.fixture
def two_cluster_data_center():
    yield Datacenter(
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
            "BER-2030": {
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


@pytest.fixture
def json_example_data_centers(response_json_example):
    """
    Gives a dict with the data centers from the json example indexed by name
    """
    yield {
        name: Datacenter(name, cluster_data)
        for name, cluster_data in response_json_example.items()
    }


def test_datacenter_inits_name():
    # WHEN a Datacenter is created
    datacenter = Datacenter("Berlin", {})

    # THEN name is initialized
    assert datacenter.name == "Berlin"


def test_datacenter_inits_clusters(two_cluster_data_center):
    # WHEN a Datacenter is created (in fixture two_cluster_data_center

    # THEN clusters field is properly initialized
    assert isinstance(two_cluster_data_center.clusters, list)
    assert len(two_cluster_data_center.clusters) == 2
    assert all([isinstance(cluster, Cluster) for cluster in two_cluster_data_center.clusters])


def test_datacenter_inits_from_json_example(json_example_data_centers):
    # WHEN creating network cluster instances based on example entries (fixture)

    # THEN all datacenters are valid
    assert len(json_example_data_centers) == 2
    assert all([
        isinstance(data_center, Datacenter) for data_center in json_example_data_centers.values()
    ])
    assert all([
        isinstance(data_center.name, str)
        and
        isinstance(data_center.clusters, list)
        and
        all([isinstance(cluster, Cluster) for cluster in data_center.clusters])
        for data_center in json_example_data_centers.values()
    ])
    # and this random value is correct
    assert json_example_data_centers["Berlin"].clusters[1].\
               networks[1].entries[2].address == "192.168.11.522"


def test_remove_invalid_clusters_removes_an_invalid_cluster(two_cluster_data_center):
    # GIVEN a data center with two cluster (one with a valid name, one invalid) (from fixture)
    assert len(two_cluster_data_center.clusters) == 2

    # WHEN calling remove_invalid_clusters
    two_cluster_data_center.remove_invalid_clusters()

    # THEN the data center is only left with one cluster
    assert len(two_cluster_data_center.clusters) == 1
