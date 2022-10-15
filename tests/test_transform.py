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

import os

import pandas as pd

from pymacies_arg import Transform


def test_trasform(file_path):
    data_path = os.path.join(file_path, "pharmacies.csv")
    df = pd.read_csv(data_path)
    transform = Transform()
    df_trasform = transform.transform(df)
    cols = [
        "id",
        "name",
        "adress",
        "id_location",
        "location",
        "id_province",
        "province",
        "id_department",
        "department",
        "postal_code",
        "webpage",
    ]
    # Get the list of all column names from headers
    column_headers = list(df_trasform.columns.values)
    assert cols == column_headers
