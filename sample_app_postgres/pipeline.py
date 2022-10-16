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
import pathlib

import click

from pymacies_arg import (
    DepartmentsLoader,
    LocationsLoader,
    PharmaciesLoader,
    PymaciesArg,
)

import scripts

import settings

from sqlalchemy import create_engine


# this path is pointing to project/sample_app
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

engine = create_engine(settings.setup_data["SQLALCHEMY_DATABASE_URI"])


# : configure the command for run pipeline.
@click.command()
@click.option("--date", help="run date in format yyyy-mm-dd")
@click.argument("province")
def run_pipeline(date, province) -> None:
    """
    Read files with data from `source <datos.gob.ar>`_.

    Create a dataframe with the data and rewrite headers format.
    Save all dataframes as `.csv` file.

    Parameters
    ----------
    date : str
        Path to files to be read.

    Return
    ------
    csv : str
        All `.csv` files with data.
    """
    pymacies = PymaciesArg(date, CURRENT_PATH)
    # Extract
    scripts.logger.info("Extracting")
    file_paths = pymacies.extract_raws()

    # Transform
    scripts.logger.info("Tansform")
    paths = pymacies.trasform_raws(file_paths, province)

    # Load
    scripts.logger.info("Loading")
    PharmaciesLoader(engine).load_table(paths[0])
    LocationsLoader(engine).load_table(paths[1])
    DepartmentsLoader(engine).load_table(paths[2])

    # Done
    scripts.logger.info("Done!")


if __name__ == "__main__":
    run_pipeline()
