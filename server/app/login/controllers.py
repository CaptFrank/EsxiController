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
from server.app.login.models import *
from server.app import app, db, login_manager
from server.utils.error.loginhandler import *
from flask_login import login_user, logout_user

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'app/login/static/'

"""
=============================================
Variables
=============================================
"""

current_users               = {}

# Login object
login = Blueprint('login', __name__, url_prefix='/app')

"""
=============================================
Source
=============================================
"""

@login.route('/help',    methods = ['GET', 'POST'])
def login_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

@login.route('/register/',     methods = ['POST'])
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
        if (user is not None) or (user is not None):
            raise LoginException("Username already registered.")

        # Otherwise the user needs to be added
        user = User(username, password)

        # We also create a user stat db record for that user
        user_stats = UserStats(user = username)

        # Add the user
        db.session.add(user)
        db.session.add(user_stats)
        db.session.commit()

        # Return the response
        return jsonify({
            'username'  : user.username
            }), \
            SUCCESS_RESPONSE, \
            {
                'location'  : url_for(
                    'get_user',
                    id = user.username,
                    _external = True
                )
            }

    else:
        raise LoginException("Message empty.")

@login.route('/unregister/',   methods = ['DELETE'])
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
        user = User.query.filter_by(username = username).first_or_404()
        user_stats = UserStats.query.filter_by(user = username).firs_or_404()

        # Check the db for the user
        if (user is None) and (user_stats is None):
            raise LoginException("Username not registered.")

        # Delete the user
        db.session.delete(user)
        db.session.delete(user_stats)
        db.session.commit()

        # Return the response
        return jsonify({
            'username'  : user.username
        }), \
        SUCCESS_RESPONSE

    else:
        raise LoginException("Message empty.")

@login.route('/login/',        methods = ['POST'])
def login():
    """
    Login the user.

    :return:
    """

    # global handle
    global current_users

    # temp dict
    temp = dict()

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
        hashed = User.query.filter_by(username = username).first_or_404()
        hashed_stats = UserStats.filter_by(user = username).first_or_404()

        # Check for existence
        if (hashed is None) and (hashed_stats is None):
            raise LoginException("Not a valid username.")

        # Check the hashes
        if user.password_hash == hashed.password_hash:

            # Authenticate the user
            user.authenticated = True

            temp['user'] = user
            temp['stats'] = user

            current_users[username] = temp
            db.session.commit()

            # We have a good match so we login
            login_user(user, remember = True)

            # Update the login record
            hashed.update_login_record()
            hashed_stats.push_update()

            return jsonify({
                'username'     : hashed.username,
                'login_count'  : hashed.login_count,
                'last_login'   : hashed.last_login,
                'created'      : hashed.age
                }), \
               SUCCESS_RESPONSE

        else:
            raise LoginException("Not a valid login credential.")

@login.route('/logout/',       methods = ['POST'])
def logout():
    """
    This logs out the user.

    :return:
    """

    # global handle
    global current_users

    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        username = request.json.get('username')

        # Check the attributes
        if username is None:
            raise LoginException("Null username.")
    else:
        raise LoginException("Not a valid request.")

    # Get from the session
    user = current_users[username]['user']

    # Authenticate the user
    user.authenticated = False
    db.session.commit()

    # Logout the cookie
    logout_user()
    return redirect('/')


"""
=============================================
Utilities
=============================================
"""

@login_manager.user_loader
def load_user(username):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.
    user_loader stores the returned User object in current_user during every
    flask request.
    """
    return User.query.filter_by(username = username).first_or_404()

@login_manager.token_loader
def load_token(token):
    """
    Flask-Login token_loader callback.
    The token_loader function asks this function to take the token that was
    stored on the users computer process it to check if its valid and then
    return a User Object if its valid or None if its not valid.
    """

    # The Token itself was generated by User.get_auth_token.  So it is up to
    # us to known the format of the token data itself.

    # The Token was encrypted using itsdangerous.URLSafeTimedSerializer which
    # allows us to have a max_age on the token itself.  When the cookie is stored
    # on the users computer it also has a exipry date, but could be changed by
    # the user, so this feature allows us to enforce the exipry date of the token
    # server side and not rely on the users cookie to exipre.
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age = max_age)

    # Find the User
    user = User.query.filter_by(username = data[0]).first_or_404()

    # Check Password and return user or None
    if user and data[1] == user.password_hash:
        return user
    return None
