import re
from data_structures.network_collection import NetworkCollection


class Cluster:
    def __init__(self, name, network_dict, security_level):
        """
        Constructor for Cluster data structure.

        self.name -> str
        self.security_level -> int
        self.networks -> list(NetworkCollection)
        """
        self.name = name
        self.networks = [
            NetworkCollection(network_addr, entries)
            for network_addr, entries in network_dict.items()
        ]
        self.security_level = security_level

    def has_valid_name(self):
        """
        Validates name of the cluster

        :return bool: True if valid, False if not
        """
        return bool(re.match(r'^[A-Z]{3}-\d{1,3}$', self.name))
