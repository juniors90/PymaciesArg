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

import constants

import settings

from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine(settings.setup_data["SQLALCHEMY_DATABASE_URI"])

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

query1 = """ALTER TABLE pharmacies
            ADD CONSTRAINT locfk
            FOREIGN KEY (id_location)
            REFERENCES locations (id_location) MATCH FULL;"""

query2 = """ALTER TABLE pharmacies
            ADD CONSTRAINT depfk
            FOREIGN KEY (id_department)
            REFERENCES departments (id_department) MATCH FULL;
        """


def create_table():
    """Create all table in database."""
    with engine.connect() as conn:
        for file in constants.TABLE_NAMES[0:3]:
            logger.info(f"create table {file}")
            with open(
                constants.SQL_DIR / f"{file}.sql", "r", encoding="utf-8"
            ) as f:
                query = text(f.read())

            conn.execute(f"DROP TABLE IF EXISTS {file} CASCADE;")
            conn.execute(query)

        conn.execute(query1)
        conn.execute(query2)
    logger.info("create table is done!")


if __name__ == "__main__":
    create_table()
