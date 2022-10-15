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

log = logging.getLogger()

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
            log.info(f"create table {file}")
            with open(
                constants.SQL_DIR / f"{file}.sql", "r", encoding="utf-8"
            ) as f:
                query = text(f.read())
                print(query)

            conn.execute(f"DROP TABLE IF EXISTS {file} CASCADE;")
            conn.execute(query)

        conn.execute(query1)
        print(query1)
        conn.execute(query2)
        print(query2)


if __name__ == "__main__":
    create_table()
