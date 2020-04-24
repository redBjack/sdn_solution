from datetime import datetime
from ipaddress import IPv4Address, AddressValueError


class Entry:
    def __init__(self, address, available, last_used):
        """
        Constructor for Entry data structure.

        self.address -> str
        self.available -> bool
        self.last_used -> datetime
        """
        self.address = address
        self.available = available
        self.last_used = datetime.strptime(last_used, "%d/%m/%y %H:%M:%S")
        self.ipv4_address = None

    def has_valid_address(self):
        """
        Validates address is IPv4 Address
        As a side effect ipv4_address is stored
        """
        try:
            self.ipv4_address = IPv4Address(self.address)
            return True
        except AddressValueError:
            return False

    def __lt__(self, other):
        """
        Compares with other entry based on ip address
        """
        # these checks also ensure that ipv4_address is present
        if not (self.has_valid_address() and other.has_valid_address()):
            raise ValueError("Cannot compare if address is not valid")
        return self.ipv4_address < other.ipv4_address
