"""

    db.py
    ==========

    This module is the database interface module. It handles
    all the interactions with the mysql database.

    :copyright: (c) 2015 by GammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         GammaRay
    Version:        1.0
    Date:           3/11/2015

"""

"""
=============================================
Imports
=============================================
"""

import os
import sys
sys.path.append(".")

from flask_sqlalchemy import SQLAlchemy

"""
=============================================
Constant
=============================================
"""

DATABASE_ACCESS         = 'sqlite:///db/data.db'

"""
=============================================
Source
=============================================
"""

# =====================
# Database
# =====================

def setup_db(app):
    """
    Returns a hanlde to a sql database.

    The database config must be in the app.config dict

        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_ACCESS

    :param app:             the web app and its configs
    :return:
    """
    return SQLAlchemy(app)

def init_db(db):
    """
    Import all modules here that might define models so that
    they will be registered properly on the metadata. Otherwise
    you will have to import them first before calling init_db()

    :param db:              the database handle
    :return:
    """

    print(os.getcwd())

    # Import all models
    import apps.config.models
    import apps.engine.models
    import apps.login.models
    import apps.task.models

    # Create all models
    db.create_all()
    return