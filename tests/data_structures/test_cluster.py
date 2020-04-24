from data_structures.cluster import Cluster


def test_cluster_inits_name():
    # WHEN creating an instance of Cluster
    cluster = Cluster("BER-1", {}, 1)

    # THEN name is properly initialized
    assert cluster.name == "BER-1"
