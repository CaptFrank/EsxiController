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

import uuid

from server import app, db
from sqlalchemy import *
from sqlalchemy import sql
from datetime import datetime
from flask_sqlalchemy import *
from sqlalchemy.orm import relationship

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

# ===================
# Configuration
# ===================

class Configuration(Model):
    """
    This is the main table used in this application.
    It stores the configs in form of str(json).

    Extends the Model class.
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'configs'

    # ===================
    # Attributes
    # ===================

    id              = Column(Integer,       primary_key     = True)
    name            = Column(String,        unique          = True)
    uuid            = Column(String,        unique          = True)
    favorite        = Column(Boolean,       default         = False)
    date            = Column(DateTime)
    access          = Column(DateTime)
    recent          = Column(Integer,       default         = 0)
    user            = Column(String)


    # Favorite Relationship
    favorite_id     = Column(Integer,       ForeignKey('favorites.id'))

    # Core attributes
    config_type     = Column(String)
    configs         = Column(String,        unique          = False)

    # ===================
    # Sources
    # ===================

    def __init__(self,
                 name           = None,
                 configs        = None,
                 favorite       = None,
                 config_type    = None):
        """
        This is the default constructor for the table

        :param name:                    the config name
        :param configs:                 the config in dict form
        :param favorite:                the favorite boolean
        :param config_type:             the config type
        :return:
        """

        self.name           = name
        self.configs        = str(configs)
        self.uuid           = str(uuid.uuid4())
        self.favorite       = favorite
        self.config_type    = config_type
        self.date           = datetime.utcnow()
        return

    def update_config_record(self, user):
        """
        We update the configs timestamps and counts

        :param access:
        :param recent:
        :param user:
        :return:
        """

        # Update internals
        self.access = datetime.utcnow()
        self.recent += 1
        self.user = user
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

# ===================
# Session
# ===================

class Session(Model):
    """
    This is the main table used in this application.
    It stores the sessions in form of union of configs.

    Extends the Model class.
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'sessions'

    # ===================
    # Attributes
    # ===================

    id              = Column(Integer,       primary_key     = True)
    name            = Column(String,        unique          = True)
    uuid            = Column(String,        unique          = True)
    favorite        = Column(Boolean,       default         = False)
    date            = Column(DateTime)
    config_type     = Column(String)

    # Favorite Relationship
    favorite_id     = Column(Integer,       ForeignKey('favorites.id'))

    # Core attributes
    config_id       = Column(String,       ForeignKey('configs.config_type'))
    config          = relationship(
                        'Configuration',
                        backref     = 'session',
                        lazy        = 'dynamic',
                        primaryjoin = sql.and_(config_type == Configuration.config_type)
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self,
                 name           = None,
                 config_type    = None,
                 favorite       = None):
        """
        This is the default constructor for the table

        :param name:                    the config name
        :param config_id:               the config type to unionize
        :param favorite:                the favorite boolean

        :return:
        """

        self.name           = name
        self.config_type    = config_type
        self.uuid           = str(uuid.uuid4())
        self.favorite       = favorite
        self.date           = datetime.utcnow()
        return

    def __str__(self):
        """
        Override the str method.

        :return:
        """
        return '<Session %s - favorite: %s - config: %s' \
               % (self.name, str(self.favorite), self.config_id)

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """

        return '<Configuration %r - favorite %r>' \
               % (self.name, self.favorite)

# ===================
# Favorite
# ===================

class Favorite(Model):
    """
    This is the favorite table. It hosts both the
    favorite used config and the favorite used session.

    Extends the Model class.
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'favorites'

    # ===================
    # Attributes
    # ===================

    id              = Column(Integer,       primary_key     = True)
    name            = Column(String,        unique          = True)
    uuid            = Column(String,        unique          = True)
    date            = Column(DateTime)
    config_type     = Column(String)

    # Extended keys
    config_fav      = ForeignKey('configs.favorite')
    session_fav     = ForeignKey('sessions.favorite')

    # Core attributes
    fav_config      = relationship(
                                "Configuration",
                                backref     = 'favorite_config',
                                lazy        = 'dynamic',
                                primaryjoin = sql.and_(config_type == Configuration.config_type,
                                                    Configuration.favorite == True))
    fav_session     = relationship(
                                "Configuration",
                                backref     = 'favorite_session',
                                lazy        = 'dynamic',
                                primaryjoin = sql.and_(config_type == Session.config_type,
                                                    Session.favorite == True))

    # ===================
    # Sources
    # ===================

    def __init__(self, name = None, config_type = None):
        """
        This is the default constructor for the class.

        :param name:                the name of the favorite
        :param config_type:         the config type
        :return:
        """
        self.name = name
        self.config_type = config_type
        self.date = datetime.utcnow()
        self.uuid = str(uuid.uuid4())
        return

    def __str__(self):
        """
        Override the str method.

        :return:
        """
        return '<Favorite %s' % self.name

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """
        return '<Favorite %s' % self.name
