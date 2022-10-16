import datetime
import logging
import os
import pathlib

from pymacies_arg import (
    DepartmentsLoader,
    LocationsLoader,
    PharmaciesLoader,
    PymaciesArg,
)

from sqlalchemy import create_engine


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

# this path is pointing to project/
PATH = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = "sqlite:///" + PATH + "/db_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

now = datetime.datetime.now()
date = f"{now.year}-{now.month}-{now.day}"

pymacies = PymaciesArg(date, pathlib.Path(PATH))

# Extract
logger.info("Extracting")
file_paths = pymacies.extract_raws()

# Transform
logger.info("Tansform")
file_paths = pymacies.extract_raws()


provinces = [
    "BUENOS AIRES",
    "SANTA FE",
    "CABA",
    "TUCUMÁN",
    "MISIONES",
    "CÓRDOBA",
    "ENTRE RÍOS",
    "CHACO",
    "SALTA",
    "CORRIENTES",
    "RÍO NEGRO",
    "LA PAMPA",
    "SANTIAGO DEL ESTERO",
    "SAN LUIS",
    "SAN JUAN",
    "NEUQUÉN",
    "CHUBUT",
    "JUJUY",
    "CATAMARCA",
    "FORMOSA",
    "LA RIOJA",
    "SANTA CRUZ",
    "TIERRA DEL FUEGO",
    "MENDOZA",
]

paths = [
    pymacies.trasform_raws(file_paths, province) for province in provinces
]

# Load
logger.info("Loading")
for path in paths:
    PharmaciesLoader(engine).load_table(path[0])
    LocationsLoader(engine).load_table(path[1])
    DepartmentsLoader(engine).load_table(path[2])

# Done
logger.info("Done!")
