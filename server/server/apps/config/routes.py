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

from flask import *
from flask_login import login_required
from apps.config.models import *
from utils.error.confighandler import *
from server import db, app

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

print('[+] Adding route: ' + '/add/help')
print('[+] Adding route: ' + '/diff/help')
print('[+] Adding route: ' + '/delete/help')
print('[+] Adding route: ' + '/modify/help')
print('[+] Adding route: ' + '/config/help')
print('[+] Adding route: ' + '/favorite/help')

@app.route('/add/help',                 methods = ['GET', 'PUT', 'POST'])
@app.route('/diff/help',                methods = ['GET', 'PUT', 'POST'])
@app.route('/delete/help',              methods = ['GET', 'PUT', 'POST'])
@app.route('/modify/help',              methods = ['GET', 'PUT', 'POST'])
@app.route('/config/help',              methods = ['GET', 'PUT', 'POST'])
@app.route('/favorite/help',            methods = ['GET', 'PUT', 'POST'])
def config_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

# ===========
# Add
# ===========

print('[+] Adding route: ' + '/add/config/')
print('[+] Adding route: ' + '/add/session/config/')

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


print('[+] Adding route: ' + '/add/session/')

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

print('[+] Adding route: ' + '/add/favorite/')

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

print('[+] Adding route: ' + '/delete/config/')
print('[+] Adding route: ' + '/delete/session/config/')

@app.route('/delete/config/',           methods = ['DELETE', 'UPDATE'])
@app.route('/delete/session/config/',   methods = ['DELETE', 'UPDATE'])
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


print('[+] Adding route: ' + '/delete/session/')

@app.route('/delete/session/',          methods = ['DELETE', 'UPDATE'])
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

print('[+] Adding route: ' + '/delete/favorite/')

@app.route('/delete/favorite/',         methods = ['DELETE', 'UPDATE'])
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

print('[+] Adding route: ' + '/modify/config/')
print('[+] Adding route: ' + '/modify/session/config/')

@app.route('/modify/config/',         methods = ['PUT', 'UPDATE', 'POST'])
@app.route('/modify/session/config/', methods = ['PUT', 'UPDATE', 'POST'])
@login_required
def config_modify():
    """
    Modify a config.

    args = {
            'config'    : <config name>,
            'section'   : <section name>,
            'attribute' : [{
                    'name'  : <name>,
                    'value' : <value>,
                        }]
        }
    """

    # We check if we have all the needed attributes.
    if request.json is not None:

        # We get the user attributes
        config = request.json.get('config')
        section = request.json.get('section')
        attributes = json.loads(request.json.get('attributes'))

        if config is None:
            raise ConfigException("Null config name.")
        elif section is None:
            raise ConfigException("Null section name.")
        elif attributes is None:
            raise ConfigException("Null attribute structure.")

        # We get the config
        config_db = Configuration.query.filter_by(name = config).first_or_404()

        # We load the structure
        config_dict = dict(config_db)

        # cycle through the attributes to change
        for attribute in attributes:
            config_dict[attribute['name']] = attribute['value']

        # We commit
        db.session.commit()

        # Return the response
        return jsonify({
            'before'    : dict(config_db),
            'after'     : config_dict

        }), \
        SUCCESS_RESPONSE

    return

# ============
# Favorite Set
# ============

print('[+] Adding route: ' + '/favorite/set/config/')
print('[+] Adding route: ' + '/favorite/set/session/')

@app.route('/favorite/set/config/',         methods = ['PUT', 'UPDATE', 'POST'])
@app.route('/favorite/set/session/',        methods = ['PUT', 'UPDATE', 'POST'])
@login_required
def config_favorite_set():
    """
    Sets the favorite config or session

        args    = {
                    'name' : name
                    'config' : config
                    }
    """

    # We check if we have all the needed attributes.
    if request.json is not None:

        # We get the user attributes
        name = request.json.get('name')
        favorite = request.json.get('favorite')

        if name is None:
            raise ConfigException("Favorite name is null.")
        elif favorite is None:
            raise ConfigException("Favorite config type is null.")
        else:

            # We have a non null config
            # Check the session

            # We add the config file only
            # Get the db entry
            fav_db = Favorite.query.filter_by(name = name).first()

            # Check the db for the user
            if fav_db is not None:
                raise Configuration("Favorite already registered.")

            # Create a favorite to commit
            favorite_db = Favorite(name, favorite)

            # Add and commit
            db.session.add(favorite_db)
            db.session.commit()


            # Return the response
            return jsonify({
                    'name'          : favorite_db.name,
                    'favorite'      : favorite_db.config_type,
                    'created'       : favorite_db.date,


                }), \
                SUCCESS_RESPONSE, \
                {
                    'location'  : url_for(
                        'get_user',
                        id = favorite_db.name,
                        _external = True
                    )
                }
    else:
        raise ConfigException("Not a valid json packet.")

# ============
# Favorite Get
# ============

print('[+] Adding route: ' + '/favorite/get/config/')
print('[+] Adding route: ' + '/favorite/get/session/')

@app.route('/favorite/get/config/',         methods = ['GET', 'POST'])
@app.route('/favorite/get/session/',        methods = ['GET', 'POST'])
@login_required
def config_favorite_get():
    """
    Gets the favorite config or session
    :return:
    """

    # We check if we have all the needed attributes.
    if request.json is not None:

        # We get the user attributes
        name = request.json.get('name')

        if name is None:
            raise ConfigException("Favorite name is null.")
        else:

            # We have a non null config
            # Check the session

            # We add the config file only
            # Get the db entry
            fav_db = Favorite.query.filter_by(name = name).first_or_404()

            # Check the db for the user
            if fav_db is None:
                raise Configuration("Favorite not registered.")


            # Return the response
            return jsonify({
                    'name'          : fav_db.name,
                    'favorite'      : fav_db.config_type,
                    'created'       : fav_db.date,

                }), \
                SUCCESS_RESPONSE, \
                {
                    'location'  : url_for(
                        'get_user',
                        id = fav_db.name,
                        _external = True
                    )
                }
    else:
        raise ConfigException("Not a valid json packet.")



