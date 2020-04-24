from sdn.lib_get_data import get_data
from data_structures.datacenter import Datacenter


def __data_centers_from_dict(data):
    return [
        Datacenter(name, cluster_data)
        for name, cluster_data in data.items()
    ]


def __assert_data_centers_eq(data_centers, expected_data_centers):
    assert len(data_centers) == len(expected_data_centers)
    for data_center, expected_data_center in zip(data_centers, expected_data_centers):
        assert data_center.name == expected_data_center.name
        assert len(data_center.clusters) == len(expected_data_center.clusters)
        for cluster, expected_cluster in zip(data_center.clusters, expected_data_center.clusters):
            assert cluster.name == expected_cluster.name
            assert len(cluster.networks) == len(expected_cluster.networks)
            for network, expected_network in zip(cluster.networks, expected_cluster.networks):
                assert network.ipv4_network == expected_network.ipv4_network
                assert len(network.entries) == len(expected_network.entries)
                for entry, expected_entry in zip(network.entries, expected_network.entries):
                    assert entry.address == expected_entry.address
                    assert entry.available == expected_entry.available
                    assert entry.last_used == expected_entry.last_used


def test_get_data_full_functionality(test_url, expected_json):
    data_centers = __data_centers_from_dict(get_data(test_url))

    for data_center in data_centers:
        data_center.remove_invalid_clusters()
        data_center.remove_invalid_records()
        data_center.sort_records()

    expected_data_centers = __data_centers_from_dict(expected_json)

    __assert_data_centers_eq(data_centers, expected_data_centers)
