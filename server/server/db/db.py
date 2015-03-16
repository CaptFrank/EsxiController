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

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
=============================================
Constant
=============================================
"""

DATABASE_ACCESS         = 'sqlite://db/data.db'

"""
=============================================
Source
=============================================
"""

# =====================
# Database
# =====================

# Create a database engine
engine      = create_engine(DATABASE_ACCESS,
                            convert_unicode=True)

# Create a session
session     = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))

# Create a base
base        = declarative_base()
base.query  = session.query_property()

def init_db():
    """
    Import all modules here that might define models so that
    they will be registered properly on the metadata. Otherwise
    you will have to import them first before calling init_db()

    :return:
    """

    # Import all models
    import server.server.apps.task.models
    import server.server.apps.config.models
    import server.server.apps.engine.models

    # Create all models
    base.metadata.create_all(bind=engine)