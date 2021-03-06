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

from server.app import app, db
from datetime import datetime
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

class User(db.Model):
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

    id              = db.Column(db.Integer,       primary_key         = True)
    username        = db.Column(db.String,        index               = True)
    password_hash   = db.Column(db.String)
    last_login      = db.Column(db.DateTime)
    login_count     = db.Column(db.Integer)
    created         = db.Column(db.DateTime)
    age             = db.Column(db.DateTime)
    authenticated   = db.Column(db.Boolean,       default             = False)

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
        db.session.commit()
        return

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.username), self.password_hash]
        return login_serializer.dumps(data)

    def is_active(self):
        """
        True, as all users are active.
        """
        return True

    def get_id(self):
        """
        Return the email address to satisfy Flask-Login's requirements.
        """
        return self.username

    def is_authenticated(self):
        """
        Return True if the user is authenticated.
        """
        return self.authenticated

    def is_anonymous(self):
        """
        False, as anonymous users aren't supported.
        """
        return False

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