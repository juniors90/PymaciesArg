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
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .constants import farmacias_ds
from .extractor import UrlExtractor
from .transform import Transform

log = logging.getLogger()

data_extractors = {
    "pharmacies": UrlExtractor(farmacias_ds["name"], farmacias_ds["url"]),
}


def extract_raws(date_str: str, base_file_dir: Path) -> Dict[str, str]:
    """
    Read files from `source <datos.gob.ar>`_ and extract the data.

    Create a dataframe with the data and rewrite headers format.
    Save all dataframes as `.csv` file.

    Parameters
    ----------
    date_str : str
        The date on run with format YYYY-mm-dd.

    Return
    ------
    file_paths : dict[str]
        A dict of stored data file paths.
    """
    file_paths = dict()
    for name, extractor in data_extractors.items():
        file_path = extractor.extract(
            date_str=date_str, base_file_dir=base_file_dir
        )
        file_paths[name] = file_path
    return file_paths


def trasform_raws(
    date_str: str, file_paths, province: str, base_file_dir: Path
) -> List[str]:
    """
    Read files from `source <datos.gob.ar>`_ and extract the data.

    Create a dataframe with the data and rewrite headers format.
    Save all dataframes as `.csv` file.

    Parameters
    ----------
    date_str : str
        The date on run with format YYYY-mm-dd.
    file_paths : str
        The destination location.
    province : str
        The province name in UPPERCASE.
    base_file_dir : Path
        A base file directory.


    Return
    ------
    data_paths : list[str]
        The destination location of data trasform.
    """
    for name, extractor in data_extractors.items():
        df = pd.read_csv(file_paths[name])
        trasform = Transform()
        dft = trasform.transform(df)

    df = dft[dft["province"] == province]

    df_fixed = df[
        [
            "id",
            "name",
            "id_location",
            "id_department",
            "postal_code",
            "adress",
        ]
    ].set_index("id")

    df_localidades = (
        df.groupby(["id_location", "location"], as_index=False)
        .count()[["id_location", "location"]]
        .set_index("id_location")
    )

    df_departamentos = (
        df.groupby(["id_department", "department"], as_index=False)
        .count()[["id_department", "department"]]
        .set_index("id_department")
    )

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    file_path_crib = (
        "data"
        + "/{full_category}"
        + "/{year}-{month:02d}"
        + "/{category}"
        + "/{full_category}-{day:02d}-{month:02d}-{year}.csv"
    )  # noqa: E501
    data_paths = []
    for name in [
        f"pharmacies_{province.lower().replace(' ', '_')}",
        f"locations_{province.lower().replace(' ', '_')}",
        f"departments_{province.lower().replace(' ', '_')}",
    ]:
        full_category = name.split("_")
        category = "_".join(full_category[1:])
        file_path = file_path_crib.format(
            full_category=full_category[0],
            category=category,
            year=date.year,
            month=date.month,
            day=date.day,
        )

        f_path = base_file_dir / file_path
        data_paths.append(f_path)
        f_path.parent.mkdir(parents=True, exist_ok=True)

    df_fixed.to_csv(data_paths[0])
    df_localidades.to_csv(data_paths[1])
    df_departamentos.to_csv(data_paths[2])
    return data_paths
