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

import datetime
import os
import pathlib

import pandas as pd

from pymacies_arg import (
    DEPARTMENTS_TABLE_NAME,
    DepartmentsLoader,
    LOCATIONS_TABLE_NAME,
    LocationsLoader,
    PHARMACIES_TABLE_NAME,
    PharmaciesLoader,
    UrlExtractor,
    extract_raws,
    farmacias_ds,
    trasform_raws,
)

# this path is pointing to project/docs/source
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
date = f"{year}-{month}-{day}"
_date = f"{year}-{month}"
province = "BUENOS AIRES"
prov_lower = province.lower().replace(" ", "_")


def test_url_extractor():
    name = farmacias_ds["name"]
    url = farmacias_ds["url"]
    extractor = UrlExtractor(farmacias_ds["name"], farmacias_ds["url"])
    assert repr(extractor) == f"<Extractor for Name: {name}, URL: {url}>"


def test_extract_trasform_and_load_raws(engine):
    # Test Extract
    file_paths = extract_raws(date_str=date, base_file_dir=CURRENT_PATH)
    assert isinstance(file_paths, dict)
    assert isinstance(file_paths["pharmacies"], pathlib.Path)
    # Test Transform
    paths = trasform_raws(
        date_str=date,
        province=province,
        file_paths=file_paths,
        base_file_dir=CURRENT_PATH,
    )
    assert isinstance(paths, list)
    df = pd.read_csv(paths[0])
    # Test Load
    assert PharmaciesLoader(engine).load_table(paths[0]) == df.to_sql(
        PHARMACIES_TABLE_NAME, con=engine, index=False, if_exists="replace"
    )
    df = pd.read_csv(paths[1])
    assert LocationsLoader(engine).load_table(paths[1]) == df.to_sql(
        LOCATIONS_TABLE_NAME, con=engine, index=False, if_exists="replace"
    )
    df = pd.read_csv(paths[2])
    assert DepartmentsLoader(engine).load_table(paths[2]) == df.to_sql(
        DEPARTMENTS_TABLE_NAME, con=engine, index=False, if_exists="replace"
    )
