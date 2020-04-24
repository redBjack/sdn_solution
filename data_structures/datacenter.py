from data_structures.cluster import Cluster


class Datacenter:
    def __init__(self, name, cluster_dict):
        """
        Constructor for Datacenter data structure.

        self.name -> str
        self.clusters -> list(Cluster)
        """
        self.name = name
        self.clusters = [
            Cluster(name, cluster_data["networks"], cluster_data["security_level"])
            for name, cluster_data in cluster_dict.items()
        ]

    def remove_invalid_clusters(self):
        """
        Removes invalid objects from the clusters list.
        """
        self.clusters = [cluster for cluster in self.clusters if cluster.has_valid_name()]

    def remove_invalid_records(self):
        """
        Remove all invalid records downstream
        """
        for cluster in self.clusters:
            cluster.remove_invalid_records()

    def sort_records(self):
        """
        Sort records downstream
        """
        for cluster in self.clusters:
            cluster.sort_records()
