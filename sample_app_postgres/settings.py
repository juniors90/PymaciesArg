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
from configparser import ConfigParser

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])

path = "/".join((os.path.abspath(__file__).replace("\\", "/")).split("/")[:-1])
config.read(os.path.join(path, "settings.ini"))

cfg = config["DEFAULT"]

cfg_data = "SQLALCHEMY_DATABASE_URI".split()

setup_data = {o: cfg[o] for o in cfg_data}
