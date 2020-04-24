# SDN Developer Challenge
This is a solution for the challenge presented for SDN Developer candidates

Solution Author: Cristian Anca <cristi.anca@gmail.com>
## Running the solution
The solution contains a collection of tests written with pytest.

### Environment for running
All required python packages are listed in requirements.txt`
### Option 1
To install the packages on your local machine:
```bash
pip install -r requirements.txt
```
### Option 2
A conda environment has been provided.
To use it (assuming conda is installed), in base folder run:
```bash
conda env create -f sdn.yml
conda activate RemoteJsonData
```

Once the environment is ready, simply run the tests using pytest
```
pytest
```
Or, to get more info
```
pytest -sv
```
**Disclaimer**

This has only been tested under macOS but should work on any posix system

## Content of solution
### get_data
`get_data` function was implemented in a separate module, under `sdn` folder
### data structures
`data_structures` folder contains all data structures
### tests
`tests` folder contains a collection of tests for all code
with same folder structure as the implementation
### main
main.py was not implemented (see below)

## Notes on the solution

### Development
The solution was written in Python3.7 using a TDD approach.
One commit at the start of development was done to exemplify it (committed example test before implementation)
but after that all code commits have a test(s) included. 

As a result every line of code is tested (although coverage is not provided in the solution)

### Solution for get_data
Although there are many options available `get_data` was implemented
using `urllib.request` which is most available

The retrying mechanism was implemented manually but then refactored
using a python PyPI package to be more idiomatic

#### Testing
`get_data` has a set of unit tests that are combined with component testing.

Normally tests that are actually doing web connections are not to be mixed
with unit tests and should be in a different stage.
Since this is not intended for production but for candidate evaluation
the decision was made to exemplify more styles of testing in the same file.
(e.g. unit tests with mocking, component test that connect to url)

### main.py
End 2 end testing is done in a separate test file also using pytest.
There was no need to implement main anymore, which is not clear what is supposed to do.
All the functionality and testing lie somewhere else.

### Solution for data structures
The solutions where straight forward as resulted naturally when driven by tests.

However there were a few decisions that had to be made:
* `Entry` stores a version of address in `str`format as requested
but also stores in a lazy way (when needed) an IPv4Address object.
This is to avoid converting all the time and improve performance.
Could be prone to errors but tests are very reliable
* validating an ip address was done as part of `Entry`,
close to where the data that is being validated actually is stored
* however, validating that the address is part of the network was done in
`NetworkCollection` where the network is defined.
* validating cluster name also belongs in `Cluster` class even though
the datacenter needs to filter its clusters
* sorting and removing invalid records were propagated to `Datacenter` class
to be able to easily sort and filter everything in the data at any time

#### Testing
Testing for data structures is comprehensive and is mostly done in
"social unit testing" style. I.e. mocks are not used and structures use one another for testing.

Although everything is well tested, some little more focus was placed on the functions
requested in Section III of the problem.
I.e. More test cases were provided even when sometimes not fully needed.

However `sort_records` is a special case.
Although it has some test(s) there is no focus on it.
The function only calls a library/buildin (depending on choice) function
that is properly tested in python and is very reliable, there is no need for further testing it.
Focus was placed on comparison operators instead.

### Improvements
Although some attention to detail was placed on this solution there is always room for improvement.

Just a few examples:
* address handling in `Entry` as explained above
* handling more error cases. E.g Utf8 characters, validating types (e.g date), etc
* implementing `__eq__` for data_structures to simplify testing
* add assert messages to all tests
