# PymaciesArg

[![Build status](https://github.com/juniors90/PymaciesArg/actions/workflows/CI.yml/badge.svg)](https://github.com/juniors90/PymaciesArg/actions)
[![codecov](https://codecov.io/gh/juniors90/PymaciesArg/branch/main/graph/badge.svg?token=kMzNWlpS4X)](https://codecov.io/gh/juniors90/PymaciesArg)
[![Documentation Status](https://readthedocs.org/projects/pymaciesarg/badge/?version=latest)](https://pymaciesarg.readthedocs.io/en/latest/?badge=latest)
![docstr-cov](https://img.shields.io/endpoint?url=https://jsonbin.org/juniors90/PymaciesArg/badges/docstr-cov)
[![GitHub license](https://img.shields.io/github/license/juniors90/PymaciesArg)](https://github.com/juniors90/PymaciesArg/blob/main/LICENSE)
[![Forks](https://img.shields.io/github/forks/juniors90/PymaciesArg)](https://github.com/juniors90/PymaciesArg/stargazers)
[![star](https://img.shields.io/github/stars/juniors90/PymaciesArg?color=yellow)](https://github.com/juniors90/PymaciesArg/network/members)
[![issues](https://img.shields.io/github/issues/juniors90/PymaciesArg?color=teal)](https://github.com/juniors90/PymaciesArg/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/juniors90/PymaciesArg?color=green)](https://github.com/juniors90/PymaciesArg/graphs/contributors)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PymaciesArg is an extension that registers all pharmacies in Argentina.

## Features

- [x] [Data generation and extration](https://datos.gob.ar/dataset/salud-listado-establecimientos-farmacias).


## Requirements

Python 3.8+

## Dependecies for this project.

- [pandas==1.5.0](https://pandas.pydata.org/) for build the backend.
- [requests==2.28.1](https://requests.readthedocs.io/en/latest/) for build the backend.

## intallation

You can install via pip:

```cmd
    $> pip install PymaciesArg
```

## Example

Register the extension:

```python
import os
import pathlib

import click

from pymacies_arg import (
    DepartmentsLoader,
    LocationsLoader,
    PharmaciesLoader,
    PymaciesArg,
    TABLE_NAMES,
)

from sqlalchemy import create_engine

# this path is pointing to project/
PATH = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + PATH + "/db_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)


# this path is pointing to project/sample_app_sqlite
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

query1 = """CREATE TABLE IF NOT EXISTS pharmacies (
    "id"  INTEGER PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "id_location"  INTEGER NOT NULL,
    "id_department"  INTEGER NOT NULL,
    "postal_code"  INTEGER NOT NULL,
    "adress" VARCHAR(255) NOT NULL);"""

query2 = """CREATE TABLE IF NOT EXISTS department (
    "id_department"  INTEGER NOT NULL PRIMARY KEY,
    "department" VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_department) REFERENCES pharmacies(id_department));"""

query3 = """CREATE TABLE IF NOT EXISTS "locations"(
    "id_location"  INTEGER PRIMARY KEY,
    "location" VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_location) REFERENCES pharmacies(id_location));"""


def create_table():
    with engine.connect() as conn:
        for tname in TABLE_NAMES[0:3]:
            print(f"create table {tname}")
            for q in [query1, query2, query3]:
                conn.execute(f"DROP TABLE IF EXISTS {tname};")
                conn.execute(q)


# : configure the command for run pipeline.
@click.command()
@click.option("--date", help="run date in format yyyy-mm-dd")
@click.argument("province")
def run_pipeline(date, province) -> None:

    pymacies = PymaciesArg(date, CURRENT_PATH)
    # Extract
    print("Extracting")
    file_paths = pymacies.extract_raws()

    # Transform
    print("Tansform")
    paths = pymacies.trasform_raws(file_paths, province)

    # Load
    print("Loading")
    PharmaciesLoader(engine).load_table(paths[0])
    LocationsLoader(engine).load_table(paths[1])
    DepartmentsLoader(engine).load_table(paths[2])

    # Done
    print("Done!")


if __name__ == "__main__":
    create_table()
    run_pipeline()
```

1. run the following command line:

    ```shell script
    $> python -m scripts --date 2022-10-16 "BUENOS AIRES"
    ```

## Recommended running instructions for dev:

1. Create a virtual environment:

    ```shell script
    $> python3 -m venv venv
    ```

2. Activate the newly created environment:

   On macOS and Linux:
    ```shell script
    $> source venv/bin/activate
    ```
   
   On Windows
   ```
   c:\> .\env\Scripts\activate
   ```

3. Install dependencies:

    ```shell script
    $> (venv) python -m pip install -r requirements/dev.txt
    ```
4. Start the sample app on server locally:

    ```shell script
    $> (venv) pip install -e .
    ```

5. Start the sample app on server locally:

    ```shell script
    $> (venv) python application/pipeline.py
    10/16/2022 04:58:34 AM - pymacies_arg - INFO - Extracting
    10/16/2022 04:58:35 AM - pymacies_arg - INFO - Tansform
    10/16/2022 04:58:38 AM - pymacies_arg - INFO - Loading
    10/16/2022 04:58:40 AM - pymacies_arg - INFO - Done!
    ```
    
## Links

- [Documentation](https://pymaciesarg.readthedocs.io)
- [Example Application using Postgresql](https://github.com/juniors90/PymaciesArg/tree/main/sample_app_postgres)
- [Example Application using sqlite](https://github.com/juniors90/PymaciesArg/tree/main/sample_app_sqlite)
- [PyPI Releases](https://pypi.org/project/PymaciesArg/)
- [Changelog](https://github.com/juniors90/PymaciesArg/blob/main/CHANGELOG.rst)

## Authors

- Ferreira, Juan David

Please submit bug reports, suggestions for improvements and patches via
the (E-mail: juandavid9a0@gmail.com).

## Contributors

Credits goes to these peoples:

<a href="https://github.com/juniors90/PymaciesArg/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=juniors90/PymaciesArg" />
</a>

## Official repository and Issues

- https://github.com/juniors90/PymaciesArg


## License

`PymaciesArg` is free software you can redistribute it and/or modify it
under the terms of the MIT License. For more information, you can see the
[LICENSE](https://github.com/juniors90/PymaciesArg/blob/main/LICENSE) file
for details.
