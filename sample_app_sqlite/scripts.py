# !/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the PymaciesArg Project
#     https://github.com/juniors90/PymaciesArg.
#
# Copyright (c) 2022. Ferreira Juan David
# License: MIT
#   Full Text: https://github.com/juniors90/PymaciesArg/blob/main/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""
PymaciesArg.

An extension that registers all pharmacies in Argentina.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import logging
import os

from pymacies_arg import TABLE_NAMES

from sqlalchemy import create_engine

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    base, "sample_app_sqlite", "db_data.db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

logging.basicConfig(filename="pipeline.log", encoding="utf-8")

# create logger
logger = logging.getLogger(name="pymacies_arg")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

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
            logger.info(f"create table {tname}")
            for q in [query1, query2, query3]:
                conn.execute(f"DROP TABLE IF EXISTS {tname};")
                conn.execute(q)


if __name__ == "__main__":
    create_table()
