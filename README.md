# Empora Code Sample
An implementation of the Empora take home code challenge.

[Prompt](code-sample-prompt.md)

# Installation
## Requirements
Requires [python](https://www.python.org/) >= 3.10 and [poetry](https://python-poetry.org/).

## Install Dependencies
``` bash
# To install python >= 3.10 please refer to:
# https://www.python.org/downloads/
#
# If you have not installed poetry please refer to the documentation at:
# https://python-poetry.org/docs/

# Install code sample dependencies
poetry install
```

# Configuration
This project accesses the smarty street address verification api. To configure
credentials to the api you can use the following environment variables:


**Required:**
* SMARTY\_API\_KEY: The smarty api secret key/token.
* SMARTY\_API\_ID: The smarty api id.


**Optional**
* SMARTY\_API\_LICENSE: The smarty api license. Defaults to `us-core-cloud`.
* SMARTY\_API\_BASE\_ROUTE: The smarty api server base route. Defaults to
`https://us-street.api.smartystreets.com`.

For convenience the script can also load variables from a .env in the root of
the project. An example of the .env file can be found in
[.env.example](.env.example)


# Running
``` bash
poetry run sample example.csv

# Or

cat example.csv | poetry run sample
```

# Testing
Tests are written using the standard python unittest library so can be
discovered by running the following within the poetry environment:
```bash
python -m unittest
```

For convenience there is also a poetry script that can be run without activating
the poetry shell:
```bash
poetry run tests
```

# Decisions thought process
The requested thought process on decisions is contained in [decisions.md](decisions.md)
