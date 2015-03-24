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

from flask_sqlalchemy import SQLAlchemy
from server.app.engine.models import *

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

    # Import models
    import server.app.config.models
    import server.app.engine.models
    import server.app.login.models
    import server.app.task.models

    # Create all models
    db.create_all()

    # Create base tables
    db.session.add(EngineStatus())
    db.session.add(WebStatus())
    db.session.add(CommandStats(COMMAND_TYPE_WEB))
    db.session.add(CommandStats(COMMAND_TYPE_CLI))
    db.session.commit()
    return