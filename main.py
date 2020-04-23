from data_structures.datacenter import Datacenter
from sdn.lib_get_data import get_data

URL = "http://www.mocky.io/v2/5e539b332e00007c002dacbe"


def main():
    """
    Main entry to our program.
    """

    data = get_data(URL)

    if not data:
        raise ValueError('No data to process')

    datacenters = [
        Datacenter(key, value)
        for key, value in data.items()
    ]

    pass  # the rest of your logic here


if __name__ == '__main__':
    main()
