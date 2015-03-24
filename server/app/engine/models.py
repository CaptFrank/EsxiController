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
import json
import uuid

from server.app import db
from datetime import datetime

"""
=============================================
Constant
=============================================
"""

COMMAND_TYPE_WEB            = "WEB"
COMMAND_TYPE_CLI            = "CLI"

# Indexes
ENGINE_STATUS_CREATED       = 0
ENGINE_STATUS_UPDATED       = 1
ENGINE_STATUS_STALE         = 2
ENGINE_STATUS_ERROR         = 3
ENGINE_STATUS_RUNNING       = 4
ENGINE_STATUS_STOPPED       = 5
ENGINE_STATUS_SUSPENDED     = 6

# Indexes
WEB_STATUS_CREATED          = 0
WEB_STATUS_UPDATED          = 1
WEB_STATUS_STALE            = 2
WEB_STATUS_ERROR            = 3
WEB_STATUS_RUNNING          = 4
WEB_STATUS_STOPPED          = 5
WEB_STATUS_SUSPENDED        = 6

# Strings
STATUS                      = [
                                'CREATED',
                                'UPDATED',
                                'STALE',
                                'ERROR',
                                'RUNNING',
                                'STOPPED',
                                'SUSPENDED'
                                ]

# Command sources
COMMAND_SOURCE_ENGINE       = 'Engine'
COMMAND_SOURCE_WEB          = 'Web'

"""
=============================================
Source
=============================================
"""

# ===================
# Engine
# ===================

class EngineStatus(db.Model):
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

    log_level       = db.Column(db.Boolean,       default          = True)

    # Tasks stats
    task_stats      = db.Column(db.Integer,       db.ForeignKey('task_stats.id'))

    # Command stats
    command_stats   = db.Column(db.Integer,       db.ForeignKey('command_stats.id'))
    command_history = db.Column(db.Integer,       db.ForeignKey('command_history.id'))

    command_engine_stat  = db.relationship(
                        'CommandStats',
                        backref     = 'engine_commands_stats',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandStats.command_type == COMMAND_SOURCE_ENGINE)
                        )

    command_engine_hist  = db.relationship(
                        'CommandHistory',
                        backref     = 'engine_commands_history',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandHistory.command_type == COMMAND_SOURCE_ENGINE)
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self):
        """
        This is the default constructor for the class.
        It is never employed...
        """

        # Set creation attributes
        self.uuid = str(uuid.uuid4())
        self.created = datetime.utcnow()
        self.status = STATUS[ENGINE_STATUS_CREATED]
        return

    def push_update(self):
        """
        This updates the table contents.
        """

        # Set updates
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        self.status = STATUS[ENGINE_STATUS_UPDATED]
        db.session.commit()
        return

    def push_status(self, status):
        """
        This method updates the status of the record
        """

        # Update the record
        self.status = status
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        db.session.commit()
        return

    def push_engine_attributes(self, log, syslog, splunk):
        """
        This pushed the engine startup attributes to the DB.

        args
        =====

        log = level

        syslog = {
            'enable'    : Bool,

            'settings' : {
                    'address'   : IP,
                    'port'      : Integer
                    }
        }

        splunk = {
            'enable'    : Bool,

            'settings' : {
                    'token'     : String,
                    'project'   : String,
                    'api'       : String
                    }
        }

        :param log:                         Enable logging
        :param syslog:                      Enable syslogging
        :param splunk:                      Enable Splunk logging
        """

        # Set internal attributes
        self.log_level = log
        self.syslog_enable = syslog['enable']
        self.splunk_enable = splunk['enable']

        self.syslog_settings = json.dumps(syslog['settings'])
        self.splunk_settings = json.dumps(splunk['settings'])
        db.session.commit()
        return

    def __str__(self):
        """
        Override the internal string output.
        """
        return "<EngineStatus - date: %s - running: %s>" \
               % (str(datetime.utcnow()), self.status)

    def __repr__(self):
        """
        Override the internal repr output.
        """
        return "<EngineStatus - date: %s - running: %s>" \
               % (str(datetime.utcnow()), self.status)

# ===================
# Web
# ===================

class WebStatus(db.Model):
    """
    This is the table that houses the front end
    web server status and service attributes.

    extends: db.Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'web_status'

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

    # Users stats
    user_stats      = db.Column(db.Integer,       db.ForeignKey('user_stats.id'))

    # Command stats
    command_stats   = db.Column(db.Integer,       db.ForeignKey('command_stats.id'))
    command_history = db.Column(db.Integer,       db.ForeignKey('command_history.id'))


    command_engine_stat  = db.relationship(
                        'CommandStats',
                        backref     = 'web_commands_stats',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandStats.command_type == COMMAND_SOURCE_WEB)
                        )

    command_engine_hist  = db.relationship(
                        'CommandHistory',
                        backref     = 'web_commands_history',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandHistory.command_type == COMMAND_SOURCE_WEB)
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self):
        """
        This is the default constructor for the class.
        It is never employed...
        """

        # Set creation attributes
        self.uuid = str(uuid.uuid4())
        self.created = datetime.utcnow()
        self.status = STATUS[WEB_STATUS_CREATED]
        return

    def push_update(self):
        """
        This updates the table contents.
        """

        # Set updates
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        self.status = STATUS[WEB_STATUS_UPDATED]
        db.session.commit()
        return

    def push_status(self, status):
        """
        This method updates the status of the record
        """

        # Update the record
        self.status = STATUS[status]
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        db.session.commit()
        return

    def __str__(self):
        """
        Override the internal string output.
        """
        return "<EngineStatus - date: %s - running: %s>" \
               % (str(datetime.utcnow()), self.status)

    def __repr__(self):
        """
        Override the internal repr output.
        """
        return "<EngineStatus - date: %s - running: %s>" \
               % (str(datetime.utcnow()), self.status)

# ===================
# Commands
# ===================

class CommandStats(db.Model):
    """
    This table houses the command stats within time
    and their return codes.

    extends: db.Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'command_stats'

    # ===================
    # Attributes
    # ===================

    # Generic
    id              = db.Column(db.Integer,       primary_key     = True)
    uuid            = db.Column(db.String,        unique          = True)
    created         = db.Column(db.DateTime)
    updated         = db.Column(db.DateTime)
    uptime          = db.Column(db.DateTime)

    count           = db.Column(db.Integer,       default         = 0)
    recent          = db.Column(db.String)

    command_type    = db.Column(db.String)
    command_history = db.relationship(
                        'CommandHistory',
                        backref     = 'command_history',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandHistory.command_type == command_type)
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self, command_type):
        """
        This is the default constructor for the class.

        :param command_type:            the command type
        """

        # Set creation attributes
        self.uuid = str(uuid.uuid4())
        self.created = datetime.utcnow()
        self.command_type = command_type
        return

    def push_update(self, command):
        """
        This updates the table contents.

        :param command:
        :return:
        """

        # Set updates
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        self.recent = command
        self.count = db.session.query(CommandHistory).count() + 1
        db.session.commit()
        return

    def __str__(self):
        """
        Override the internal string output.
        """
        return "<CommandStats - date: %s - type: %s>" \
               % (str(datetime.utcnow(), self.command_type))

    def __repr__(self):
        """
        Override the internal repr output.
        """
        return "<CommandStats - date: %s - type: %s>" \
               % (str(datetime.utcnow(), self.command_type))

class CommandHistory(db.Model):
    """
    This table houses the command history within time
    and their return codes.

    extends: db.Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'command_history'

    # ===================
    # Attributes
    # ===================

    # Generic
    id              = db.Column(db.Integer,       primary_key     = True)
    uuid            = db.Column(db.String,        unique          = True)
    created         = db.Column(db.DateTime)
    updated         = db.Column(db.DateTime)
    uptime          = db.Column(db.DateTime)

    command         = db.Column(db.String)
    command_user    = db.Column(db.String)
    command_type    = db.Column(db.String)
    command_time    = db.Column(db.Datetime)

    def __init__(self, command, type, user):
        """
        This is the default constructor for the class

        :param command:             the command executed
        :param type:                the command type
        """

        # Set creation attributes
        self.uuid = str(uuid.uuid4())
        self.created = datetime.utcnow()

        # Set command attributes
        self.command = command
        self.command_user = user
        self.command_type = type
        self.command_time = datetime.utcnow()
        return

    def push_update(self):
        """
        This updates the table contents.

        :param command:
        :return:
        """

        # Set updates
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        db.session.commit()
        return

    def __str__(self):
        """
        Override the internal string output.
        """
        return "<CommandHistory - date: %s - type: %s>" \
               % (str(datetime.utcnow(), self.command_type))

    def __repr__(self):
        """
        Override the internal repr output.
        """
        return "<CommandHistory - date: %s - type: %s>" \
               % (str(datetime.utcnow(), self.command_type))

# ===================
# Users
# ===================

class UserStats(db.Model):
    """
    This table houses the user stats within time
    and their return codes.

    extends: db.Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__   = 'user_stats'

    # ===================
    # Attributes
    # ===================

    # Generic
    id              = db.Column(db.Integer,       primary_key     = True)
    uuid            = db.Column(db.String,        unique          = True)
    created         = db.Column(db.DateTime)
    updated         = db.Column(db.DateTime)
    uptime          = db.Column(db.DateTime)

    user            = db.Column(db.String)

    user_history = db.relationship(
                        'CommandHistory',
                        backref     = 'command_history',
                        lazy        = 'dynamic',
                        primaryjoin = db.sql.and_(CommandHistory.user == user)
                        )

    # ===================
    # Sources
    # ===================

    def __init__(self, user):
        """
        This is the default constructor for the class.

        :param user:            the user
        """

        # Set creation attributes
        self.uuid = str(uuid.uuid4())
        self.created = datetime.utcnow()
        self.user = user
        return

    def push_update(self):
        """
        This updates the table contents.

        :param command:
        :return:
        """

        # Set updates
        self.updated = datetime.utcnow()
        self.uptime = self.created - datetime.utcnow()
        db.session.commit()
        return

    def __str__(self):
        """
        Override the internal string output.
        """
        return "<UserStats - date: %s - user: %s>" \
               % (str(datetime.utcnow(), self.user))

    def __repr__(self):
        """
        Override the internal repr output.
        """
        return "<UserStats - date: %s - user: %s>" \
               % (str(datetime.utcnow(), self.user))