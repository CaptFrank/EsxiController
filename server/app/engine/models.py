"""

    models.py
    ==========

    This is the models interface for the database for the engine
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

ENGINE_STATUS               = [
                                'CREATED',
                                'SUSPENDED',
                                'STOPPED',
                                'RUNNING',
                                'ERROR'
                                ]

"""
=============================================
Source
=============================================
"""

# ===================
# Engine
# ===================

class engineStatus(db.Model):
    """
    This is the table that houses the backend engine status and
    service attributes.

    extends: db.Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'engine_status'

    # ===================
    # Attributes
    # ===================

    # Generic
    id              = db.Column(db.Integer,       primary_key     = True)
    uuid            = db.Column(db.String,        unique          = True)
    created         = db.Column(db.DateTime)
    updated         = db.Column(db.DateTime)
    uptime          = db.Column(db.DateTime)
    status          = db.Column(db.DateTime)

    # Application attributes
    splunk_enable   = db.Column(db.Boolean,       default          = False)
    splunk_settings = db.Column(db.String)

    syslog_enable   = db.Column(db.Boolean,       default          = False)
    syslog_settings = db.Column(db.String)

    log_enable      = db.Column(db.Boolean,       default          = True)

    # Tasks stats
    task_stats      = db.Column(db.Integer,       db.ForeignKey('task_stats.id'))

    # Users stats
    user_stats      = db.Column(db.Integer,       db.ForeignKey('user_stats.id'))

    # Command stats
    command_stats   = db.Column(db.Integer,       db.ForeignKey('command_stats.id'))

    # ===================
    # Sources
    # ===================

    def __init__(self):

        return

    def push_update(self):

        return

    def push_status(self, status):

        return

    def __str__(self):

        return

    def __repr__(self):

        return

# ===================
# Commands
# ===================

class commandStats(db.Model):
    """
    This table houses the command stats within time
    and their return codes.

    extends: db.Model
    """

    def __init__(self):

        return

    def __str__(self):

        return

    def __repr__(self):

        return

class commandHistory(db.Model):
    """
    This table houses the command history within time
    and their return codes.

    extends: db.Model
    """

    def __init__(self):

        return

    def __str__(self):

        return

    def __repr__(self):

        return

# ===================
# Users
# ===================

class userStats(db.Model):
    """
    This table houses the user stats within time
    and their return codes.

    extends: db.Model
    """

    def __init__(self):

        return

    def __str__(self):

        return

    def __repr__(self):

        return


class userHistory(db.Model):
    """
    This table houses the user history within time
    and their return codes.

    extends: db.Model
    """

    def __init__(self):

        return

    def __str__(self):

        return

    def __repr__(self):

        return

# ===================
# Web
# ===================

class webStatus(db.Model):
    """
    This is the table that houses the front end
    web server status and service attributes.

    extends: db.Model
    """

    def __init__(self):

        return

    def __str__(self):

        return

    def __repr__(self):

        return



