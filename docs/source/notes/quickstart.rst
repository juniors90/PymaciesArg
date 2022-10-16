Quickstart
==========

Installation
------------

Create a project folder and a :file:`venv` folder within:

.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ mkdir myproject
         $ cd myproject
         $ python3 -m venv venv

   .. group-tab:: Windows

      .. code-block:: text

         > mkdir myproject
         > cd myproject
         > py -3 -m venv venv


Activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before you work on your project, activate the corresponding environment:

.. tabs::

   .. group-tab:: macOS/Linux

      .. code-block:: text

         $ . venv/bin/activate

   .. group-tab:: Windows

      .. code-block:: text

         > venv\Scripts\activate

Your shell prompt will change to show the name of the activated
environment.


Install
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ pip install 


Initialization
--------------

.. code-block:: python

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

ETL - Extract, Transform and Load
---------------------------------

.. code-block:: python
    
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

Resources helpers
-----------------

Flask-FomanticUI provides two helper functions to load `Fomantic UI <https://fomantic-ui.com/>`_
resources in the template: ``fomantic.load_css()`` and ``fomantic.load_js()``.

