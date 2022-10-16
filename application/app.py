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
