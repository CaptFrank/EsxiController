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

from sqlalchemy import *
from datetime import datetime
from flask_sqlalchemy import *
from flask_login import UserMixin
from server.server.server import app
from itsdangerous import URLSafeTimedSerializer
from passlib.apps import custom_app_context as pwd_context

"""
=============================================
Variables
=============================================
"""

login_serializer = URLSafeTimedSerializer(app.secret_key)

"""
=============================================
Source
=============================================
"""

# ===================
# User
# ===================
class User(UserMixin, Model):
    """
    This user table is where we host all the usernames and
    their associated passwords hashed.

    extends Model
    """

    # ===================
    # Table name
    # ===================

    __tablename__ = 'users'

    # ===================
    # Attributes
    # ===================

    id              = Column(Integer,       primary_key         = True)
    username        = Column(String,        index               = True)
    password_hash   = Column(String)
    last_login      = Column(DateTime)
    login_count     = Column(Integer)
    created         = Column(DateTime)
    age             = Column(DateTime)

    # ===================
    # Sources
    # ===================

    def __init__(self, username, password):
        """
        The default constructor

        :param username:            the username
        :param password:            the password
        :return:
        """

        # Set internals
        self.username = username
        self.hash_password(password)
        self.created = datetime.utcnow()
        return


    def hash_password(self, password):
        """
        Hashes a password passed to this method.

        :param password:            the password to hash
        :return:
        """

        salted_password = password + app.secret_key
        self.password_hash = pwd_context.encrypt(salted_password)
        return

    def update_login_record(self):
        """
        Updates the login record.

        :return:
        """
        self.login_count += 1
        self.last_login = datetime.utcnow()
        self.age = datetime.utcnow() - self.created
        return

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.username), self.password_hash]
        return login_serializer.dumps(data)

    def __str__(self):
        """
        Override the str method.

        :return:
        """
        return '<User %s - ' % self.username

    def __repr__(self):
        """
        Override the repr method.

        :return:
        """

        return '<User %r - favorite %r>' % self.username