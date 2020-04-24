from ipaddress import ip_network
from data_structures.entry import Entry


class NetworkCollection:
    def __init__(self, ipv4_network, raw_entry_list):
        """
        Constructor for NetworkCollection data structure.

        self.ipv4_network -> ipaddress.IPv4Network
        self.entries -> list(Entry)
        """
        self.ipv4_network = ip_network(ipv4_network)
        self.entries = [
            Entry(raw_entry["address"], raw_entry["available"], raw_entry["last_used"])
            for raw_entry in raw_entry_list
        ]

    def remove_invalid_records(self):
        """
        Removes invalid objects from the entries list.
        """

        pass

    def sort_records(self):
        """
        Sorts the list of associated entries in ascending order.
        DO NOT change this method, make the changes in entry.py :)
        """

        self.entries = sorted(self.entries)

    def is_address_in_network(self, address):
        """
        :param address: ipaddress.Ipv4Address address to test
        :return bool - True if it is an address of the network, False if not
        @note working under the assumption that network address and broadcast address are not valid
        """
        return address in self.ipv4_network.hosts()
