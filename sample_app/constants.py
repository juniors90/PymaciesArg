# !/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the PyPharmsArg Project
#     https://github.com/juniors90/PyPharmsArg.
#
# Copyright (c) 2022. Ferreira Juan David
# License: MIT
#   Full Text: https://github.com/juniors90/PyPharmsArg/blob/main/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""
PyPharmsArg.

An extension that registers all pharmacies in Argentina.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path

script_location = Path(__file__).absolute().parent
SQL_DIR = script_location / "sql"
print("file_location :", SQL_DIR)

DEPARTAMENTOS_TABLE_NAME = "departments"
LOCALIDADES_TABLE_NAME = "locations"
FARMACIAS_TABLE_NAME = "pharmacies"

TABLE_NAMES = [
    DEPARTAMENTOS_TABLE_NAME,
    LOCALIDADES_TABLE_NAME,
    FARMACIAS_TABLE_NAME,
]
