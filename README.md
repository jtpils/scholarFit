# ScholarFit

ScholarFit is a machine learning based approach for finding potential customers for a publishing industry.

## Getting Started
The following steps will guide you through the process of using ScholarFit on your local machine.

### Prerequisites

See _**requirements.txt**_ for the list of requirements.

### Installing
It is a good practice to use a virtual environment for deploying Python programs. Using **conda**, we will create an environment named *ScholarFit*. The environment name is arbitrary.

```bash
conda create -n ScholarFit python=3.6
```
To install requirements, the following command can be run.

```bash
make setup
```

## Running the tests

Regression tests can be run through the following command:

```bash
make regression
```

### Adding more tests

New tests should be added as modules where their names start with *test_* under *test* directory.


## Versioning

We use [Semantic Versioning 2.0.0](http://semver.org/) for versioning.

## Authors

* [**Farhad Maleki**](https://github.com/FarhadMaleki) - *Initial work* 
