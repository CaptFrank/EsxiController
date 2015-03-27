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
from server.app import db
from datetime import datetime

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

class Configuration(db.Model):
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

    id              = db.Column(db.Integer,       primary_key     = True)
    name            = db.Column(db.String,        unique          = True)
    uuid            = db.Column(db.String,        unique          = True)
    favorite        = db.Column(db.Boolean,       default         = False)
    date            = db.Column(db.DateTime)
    access          = db.Column(db.DateTime)
    recent          = db.Column(db.Integer,       default         = 0)
    user            = db.Column(db.String)


    # Favorite Relationship
    favorite_id     = db.Column(db.Integer,       db.ForeignKey('favorites.config_type'))

    # Core attributes
    session_type    = db.Column(db.String,        db.ForeignKey('sessions.config_type'))

    # Core attributes
    config_type     = db.Column(db.String)
    configs         = db.Column(db.String,        unique          = False)

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

        :param user:
        :return:
        """

        # Update internals
        self.access = datetime.utcnow()
        self.recent += 1
        self.user = user
        db.session.commit()
        return

    def __str__(self):
        """
        Override the str method.

        :return:
        """
        return '<Configuration %s - favorite: %s - configs: %s - type: %s>' \
               % (self.name, str(self.favorite), self.configs, self.config_type)

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """

        return '<Configuration %r - favorite %r>' \
               % (self.name, self.favorite)

# ===================
# SessionGroup
# ===================

class SessionGroup(db.Model):
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

    id              = db.Column(db.Integer,       primary_key     = True)
    name            = db.Column(db.String,        unique          = True)
    uuid            = db.Column(db.String,        unique          = True)
    favorite        = db.Column(db.Boolean,       default         = False)
    date            = db.Column(db.DateTime)
    config_type     = db.Column(db.String)

    # Favorite Relationship
    favorite_id     = db.Column(db.Integer,       db.ForeignKey('favorites.config_type'))
    config          = db.relationship(
                        'Configuration',
                        lazy        = 'dynamic',
                        primaryjoin = "SessionGroup.config_type == Configuration.config_type"
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
        return '<SessionGroup %s - favorite: %s - config: %s>' \
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

class Favorite(db.Model):
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

    id              = db.Column(db.Integer,       primary_key     = True)
    name            = db.Column(db.String,        unique          = True)
    uuid            = db.Column(db.String,        unique          = True)
    date            = db.Column(db.DateTime)
    config_type     = db.Column(db.String)

    # Core attributes
    fav_config      = db.relationship(
                                "Configuration",
                                lazy        = 'dynamic',
                                primaryjoin = "and_(Favorite.config_type == Configuration.config_type,"
                                                     + "Configuration.favorite == 1)")
    fav_session     = db.relationship(
                                "SessionGroup",
                                lazy        = 'dynamic',
                                primaryjoin = "and_(Favorite.config_type == SessionGroup.config_type,"
                                                    + "SessionGroup.favorite == 1)")

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
        return '<Favorite %s>' % self.name

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """
        return '<Favorite %s>' % self.name
