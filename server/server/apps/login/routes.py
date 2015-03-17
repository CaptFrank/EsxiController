"""

    routes.py
    ==========

    This is the flask routes to the REST Api that conform to
    the login interface app.

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

from flask import *
from server.server.server import db, auth, app
from server.server.apps.login.models import *
from server.server.utils.error.loginhandler import *
from flask_login import login_user, logout_user, current_user, login_required

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201

"""
=============================================
Source
=============================================
"""

@app.route('/register' , methods=['POST'])
def register():
    """
    Register a new user
    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        username = request.json.get('username')
        password = request.json.get('password')

        # Check the attributes
        if (username is None) or (password is None):
            raise LoginException("Null username or password.")

        # Get the db entry
        user = User.query.filter_by(username = username).first()

        # Check the db for the user
        if user is not None:
            raise LoginException("Username already registered.")

        # Otherwise the user needs to be added
        user = User(username, password)

        # Add the user
        db.session.add(user)
        db.session.commit()

        # Return the response
        return jsonify({ 'username'  : user.username}), \
               SUCCESS_RESPONSE, \
               {'location'  : url_for('get_user', id = user.id, _external = True)}
    else:
        raise LoginException("Message empty.")

@app.route('/unregister' , methods=['DELETE'])
def unregister():
    """
    Unregister a user
    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        username = request.json.get('username')

        # Check the attributes
        if username is None:
            raise LoginException("Null username.")

        # Get the db entry
        user = User.query.filter_by(username = username).first()

        # Check the db for the user
        if user is None:
            raise LoginException("Username not registered.")

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        # Return the response
        return jsonify({ 'username'  : user.username}), \
               SUCCESS_RESPONSE
    else:
        raise LoginException("Message empty.")

@app.route('/login',methods=['POST'])
def login():
    """
    Login the user.

    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        username = request.json.get('username')
        password = request.json.get('password')

        # Check the attributes
        if (username is None) or (password is None):
            raise LoginException("Null username or password.")

        # Create a user
        user = User(username, password)

        # Get the db entry
        hashed = User.query.filter_by(username = username).first()

        # Check for existance
        if hashed is None:
            raise LoginException("Not a valid username.")

        # Check the hashes
        if user.password_hash == hashed['password_hash']:

            # We have a good match so we login
            login_user(user, remember = True)

            # Update the login record
            hashed.update_login_record()
            db.session.commit()

            return jsonify({ 'username'  : user.username}), \
               SUCCESS_RESPONSE, \
               {'location'  : url_for('get_user', id = user.id, _external = True)}

        else:
            raise LoginException("Not a valid login credential.")


