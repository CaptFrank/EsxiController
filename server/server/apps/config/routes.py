"""

    routes.py
    ==========

    This is the flask routes to the REST Api that conform to
    the configuration database app.

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

import os

from flask import *
from flask_login import login_required
from server.server.apps.config.models import *
from server.server.utils.error.confighandler import *
from server.server.server import db, app, login_manager, storage

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'apps/config/static/'

"""
=============================================
Variables
=============================================
"""


"""
=============================================
Source
=============================================
"""

# ===========
# Help
# ===========

@app.route('/add/help',                 methods = ['GET', 'POST'])
@app.route('/diff/help',                methods = ['GET', 'POST'])
@app.route('/delete/help',              methods = ['GET', 'POST'])
@app.route('/modify/help',              methods = ['GET', 'POST'])
@app.route('/config/help',              methods = ['GET', 'POST'])
@app.route('/favorite/help',            methods = ['GET', 'POST'])
def config_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.md')

# ===========
# Add
# ===========

@app.route('/add/config/',              methods = ['PUT', 'POST'])
@app.route('/add/session/config/',      methods = ['PUT', 'POST'])
@login_required
def config_add():
    """
    This adds a config to the database.
    Adds a file to the database.

    Here we look for a file name in the config dict:

        args = {
            'config'        : <config name>,
            'config_dict'   : <config dict>
            }

    Once we have the temp config file,
    we read it with a config parser and dump the dict in
    the database.

    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        session = request.json.get('session')
        config = request.json.get('config')
        config_dict = json.loads(request.json.get('config_dict'))

        # We check if the session is valid
        if config is None:
            raise ConfigException("Config name cannot be null when adding.")
        elif config_dict is None:
            raise ConfigException("Config dict cannot be null when adding.")
        else:

            # We have a non null config
            # Check the session

            # We add the config file only
            # Get the db entry
            config_db = Configuration.query.filter_by(name = config).first()

            # Check the db for the user
            if config_db is not None:
                raise Configuration("Configurations already registered.")

            # Otherwise we create a new one
            config_db = Configuration(name = config,
                                      configs = config_dict,
                                      favorite = config_dict['attributes']['favorite'],
                                      config_type = config_dict['attributes']['type'])

            # Commit
            db.session.add(config_db)
            db.session.commit()

            # Return the response
            return jsonify({
                    'name'          : config_db.name,
                    'favorite'      : config_db.favorite,
                    'created'       : config_db.date,


                }), \
                SUCCESS_RESPONSE, \
                {
                    'location'  : url_for(
                        'get_user',
                        id = config_db.name,
                        _external = True
                    )
                }
    else:
        raise ConfigException("Not a valid json packet.")

@app.route('/add/session/',             methods = ['PUT', 'POST'])
@login_required
def session_add():
    """
    This adds a session id to bind with other configs.

        args = {
            'session'       : 'session',
            'session_type'  : 'session_type',
            'session_fav'   : 'favorite'
            }

    :return:
    """
    # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        session = request.json.get('session')
        session_type = request.json.get('session_type')
        session_favorite = request.json.get('session_fav')

        # We check if the session is valid
        if session is None:
            raise ConfigException("Session name cannot be null when adding.")
        elif session_type is None:
            raise ConfigException("Session type cannot be null when adding.")
        elif session_favorite is None:
            raise ConfigException("Session favorite should not be null.")
        else:

            # We add the session and create
            # a link to the session from the config.

            # We add the config file only
            # Get the db entry
            session_db = Session.query.filter_by(name = session).first()

            # Check the db for the user
            if session_db is not None:
                raise Configuration("Session already registered.")

            # Otherwise we create a new one
            session_db = Session(
                                name = session,
                                favorite = session_favorite,
                                config_type = session_type)

            # Commit
            db.session.add(session_db)
            db.session.commit()

            # Return the response
            return jsonify({
                    'name'          : session_db.name,
                    'favorite'      : session_db.favorite,
                    'created'       : session_db.date,

                }), \
                SUCCESS_RESPONSE, \
                {
                    'location'  : url_for(
                        'get_user',
                        id = session_db.name,
                        _external = True
                    ),
                }
    else:
        raise ConfigException("Not a valid json packet.")

@app.route('/add/favorite/',            methods = ['PUT', 'POST'])
@login_required
def favorite_add():
    """
    This adds a favorite filter entry.

        args = {
            'favorite' : <name>
            }
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        favorite = request.json.get('favorite')

        # We check if the session is valid
        if favorite is None:
            raise ConfigException("Favorite name cannot be null when adding.")
        else:
            # We add the session and create
            # a link to the session from the config.

            # We add the config file only
            # Get the db entry
            fav_db = Favorite.query.filter_by(name = favorite).first()

            # Check the db for the user
            if fav_db is not None:
                raise Configuration("Session already registered.")

            # Otherwise we create a new one
            fav_db = Favorite(name = favorite)

            # Commit
            db.session.add(fav_db)
            db.session.commit()

            # Return the response
            return jsonify({
                    'name'          : fav_db.name,
                }), \
                SUCCESS_RESPONSE, \
                {
                    'location'  : url_for(
                        'get_user',
                        id = fav_db.name,
                        _external = True
                    ),
                }
    else:
        raise ConfigException("Not a valid json packet.")

# ===========
# Delete
# ===========

@app.route('/delete/config/',           methods = ['DELETE'])
@app.route('/delete/session/config/',   methods = ['DELETE'])
@login_required
def config_delete():
    """
    Delete a config

    :return:
    """
    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        name = request.json.get('name')

        # Check the attributes
        if name is None:
            raise ConfigException("Null name.")

        # Get the db entry
        config = Configuration.query.filter_by(name = name).first_or_404()

        # Check the db for the user
        if config is None:
            raise ConfigException("Name not registered.")

        # Delete the user
        db.session.delete(config)
        db.session.commit()

        # Return the response
        return jsonify({
            'configuration'  : config.name
        }), \
        SUCCESS_RESPONSE

    else:
        raise ConfigException("Message empty.")

@app.route('/delete/session/',          methods = ['DELETE'])
@login_required
def session_delete():
    """
    Delete a session

    :return:
    """
    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        name = request.json.get('name')

        # Check the attributes
        if name is None:
            raise ConfigException("Null name.")

        # Get the db entry
        session = Session.query.filter_by(name = name).first_or_404()

        # Check the db for the user
        if session is None:
            raise ConfigException("Name not registered.")

        # Delete the user
        db.session.delete(session)
        db.session.commit()

        # Return the response
        return jsonify({
            'session'  : session.name
        }), \
        SUCCESS_RESPONSE

    else:
        raise ConfigException("Message empty.")

@app.route('/delete/favorite/',         methods = ['DELETE'])
@login_required
def favorite_delete():
    """
    Delete a session

    :return:
    """
    # Check if the json is not none
    if request.json is not None:

        # We get the user attributes
        name = request.json.get('name')

        # Check the attributes
        if name is None:
            raise ConfigException("Null name.")

        # Get the db entry
        favorite = Favorite.query.filter_by(name = name).first_or_404()

        # Check the db for the user
        if favorite is None:
            raise ConfigException("Name not registered.")

        # Delete the user
        db.session.delete(favorite)
        db.session.commit()

        # Return the response
        return jsonify({
            'favorite'  : favorite.name
        }), \
        SUCCESS_RESPONSE

    else:
        raise ConfigException("Message empty.")

# ===========
# Modify
# ===========

def config_modify():
    """
    Modify a config.

    args = {
            'config'    : <config name>,
            'section'   : <section name>,
            'attribute' : {
                    'name'  : <name>,
                    'value' : <value>,
                        }
        }
    """


    return

def config_diff():

    return

def config_favorite():

    return

"""
=============================================
Utilities
=============================================
"""




