"""

    models.py
    ==========

    This is the models interface for the database for the config
    applications.

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

import json
import uuid
from sqlalchemy import *
from datetime import datetime
from server.server.db.db import base
from sqlalchemy.orm import relationship, backref

"""
=============================================
Constant
=============================================
"""

"""
=============================================
Source
=============================================
"""

class Configuration(base):
    """
    This is the main table used in this application.
    It stores the configs in form of str(json).

    Extends the base class.
    """

    # ===================
    # Table name
    # ===================

    __tablename__ = 'configs'

    # ===================
    # Attributes
    # ===================

    id          = Column(Integer,       primary_key     = True)
    name        = Column(String(50),    unique          = True)
    uuid        = Column(String(20),    unique          = True)
    favorite    = Column(Boolean,       default         = False)
    date        = Column(DateTime,      default         = datetime.utcnow)

    # Core attributes
    config_type = Column(String())
    configs     = Column(String(),      unique          = False)

    # ===================
    # Sources
    # ===================

    def __init__(self, name = None,
                 configs = None,
                 favorite = None,
                 config_type = None):
        """
        This is the default constructor for the table

        :param name:                    the config name
        :param configs:                 the config in dict form
        :param favorite:                the favorite boolean
        :param config_type:             the config type
        :return:
        """

        self.name           = name
        self.configs        = json.dumps(configs)
        self.uuid           = str(uuid.uuid4())
        self.favorite       = favorite
        self.config_type    = config_type
        return

    def __str__(self):
        """
        Override the str method.

        :return:
        """
        return '<Configuration %s - favorite: %s - configs: %s - type: %s' \
               % (self.name, str(self.favorite), self.configs, self.config_type)

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """

        return '<Configuration %r - favorite %r>' \
               % (self.name, self.favorite)

class Session(base):
    """
    This is the main table used in this application.
    It stores the sessions in form of union of configs.

    Extends the base class.
    """

    # ===================
    # Table name
    # ===================

    __tablename__ = 'sessions'

    # ===================
    # Attributes
    # ===================

    id          = Column(Integer,       primary_key     = True)
    name        = Column(String(50),    unique          = True)
    uuid        = Column(String(20),    unique          = True)
    favorite    = Column(Boolean,       default         = False)
    date        = Column(DateTime,      default         = datetime.utcnow)

    # Core attributes
    config_id   = Column(Integer,       ForeignKey('configs.type'))
    config      = relationship(
                        "Configuration",
                        backref = "parents"
                        )

    def __init__(self, name = None, favorite = None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class Favorite(base):

    # ===================
    # Table name
    # ===================

    __tablename__ = 'favorites'

    # ===================
    # Attributes
    # ===================

    id          = Column(Integer,       primary_key=True)
    name        = Column(String(50),    unique=True)
    email       = Column(String(120),   unique=True)


    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)