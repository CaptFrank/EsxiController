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
    date            = Column(DateTime,      default         = datetime.utcnow())
    access          = Column(DateTime)
    recent          = Column(DateTime)
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
    date            = Column(DateTime,      default         = datetime.utcnow())
    count           = Column(Integer)

    # Favorite Relationship
    favorite_id     = Column(Integer,       ForeignKey('favorites.id'))

    # Core attributes
    config_id       = Column(Integer,       ForeignKey('configs.config_type'))
    config          = relationship(
                        'Configuration',
                        backref     = 'parents',
                        lazy        = 'dynamic'
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self,
                 name           = None,
                 config_id      = None,
                 favorite       = None):
        """
        This is the default constructor for the table

        :param name:                    the config name
        :param config_id:               the config type to unionize
        :param favorite:                the favorite boolean
        :return:
        """

        self.name           = name
        self.config_id      = config_id
        self.uuid           = str(uuid.uuid4())
        self.favorite       = favorite
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
    date            = Column(DateTime,      default         = datetime.utcnow())

    # Core attributes
    fav_config      = relationship("Configuration",
                               primaryjoin="and_(Favorite.id==Configuration.favorite_id, "
                                           "Configuration.favorite==True")
    fav_session     = relationship("Configuration",
                               primaryjoin="and_(Favorite.id==Session.favorite_id, "
                                           "Session.favorite==True")

    # ===================
    # Sources
    # ===================

    def __init__(self, name = None):
        """
        This is the default constructor for the class.

        :param name:                the name of the favorite
        :return:
        """
        self.name = name
        self.uuid           = str(uuid.uuid4())
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
