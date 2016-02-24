# Framework UnitTests
Here a placed all unittest which are asserts the functionality of the TestFramework.

Under the subdirectory */config* you can find prepared config files for special cases like running without namespace/VLAN capabilities. 
This is recommended if you what to run the server on Travis CI. 

We are using py.test as default testing tool.
Without coverage result: 'python3 -m pytest test_xyz.py'
With (appending) coverage result: 'python3 -m pytest --cov-append --cov=./ test_xyz.py'

## Naming conventions
### Automated test for Travis CI
Don't forget that on Travis CI you have to deactivate the VLAN capabilities.
Automated test has to be run on Travis CI _AND_ on a real system.
'test_A_xyz.py'

### Unittest for Travis CI
Unittest which are running on a real system which meets the requirements but are not executable on Travis CI.
'test_R_xyz.py'

### Manual tests
Unittest which are only runs on a specific prepared environment. For example: All routers in config mode.
The needed preconditions has to be documented in the unittest.
'test_M_xyz.py'

### Parallel execution
Unittest which can run concurrent with other unittests are marked with an extra _P_ in the name.
Concurrent tests are not allowed to create a Server instance.
'test_?P_xyz.py'
