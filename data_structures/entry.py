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

    def has_valid_address(self):
        """
        Validates address is IPv4 Address
        """
        try:
            IPv4Address(self.address)
            return True
        except AddressValueError:
            return False
