import datetime
import os
import pathlib

from pymacies_arg import (
    PymaciesArg,
    PharmaciesLoader,
    LocationsLoader,
    DepartmentsLoader,
)

from sqlalchemy import create_engine

# this path is pointing to project/
PATH = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = "sqlite:///" + PATH + "db_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

now = datetime.datetime.now()
date = f"{now.year}-{now.month}-{now.day}"

pymacies = PymaciesArg(date, pathlib.Path(PATH))

# Extract
file_paths = pymacies.extract_raws()

# Transform
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
for path in paths:
    PharmaciesLoader(engine).load_table(path[0])
    LocationsLoader(engine).load_table(path[1])
    DepartmentsLoader(engine).load_table(path[2])
