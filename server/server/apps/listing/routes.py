"""

    routes.py
    ==========

    This is the flask routes to the REST Api that conform to
    the listing database app.

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

print('[+] Adding route: ' + '/list/help')

@app.route('/list/help',                 methods = ['GET', 'PUT', 'POST'])
def list_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

# ===========
# List
# ===========

print('[+] Adding route: ' + '/list/all')

@app.route('/list/all',                 methods = ['GET', 'PUT', 'POST'])
@login_required
def list_all():
    """
    List all the configs in the database.

    :return:
    """

    # Get all configs in db and return them
    configs = Configuration.query.all()
    configs_dict = dict(configs)

    return jsonify(
        {
            'configs'   :   configs_dict,
            'count'     :   configs.count(),
            'date'      :   datetime.utcnow()
        }
    ), SUCCESS_RESPONSE


print('[+] Adding route: ' + '/list/config/')
print('[+] Adding route: ' + '/list/session/config/')

@app.route('/list/config/',             methods = ['GET', 'PUT', 'POST'])
@app.route('/list/session/config/',     methods = ['GET', 'PUT', 'POST'])
@login_required
def list_config():
    """
    List a specific config or group of configs.

    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        config = request.json.get('name')

        # We check if the session is valid
        if config is None:
            raise ConfigException("Config name cannot be null.")
        else:

            # We have a non null config
            # Check the session

            # We add the config file only
            # Get the db entry
            config_db = Configuration.query.filter_by(name = config).first_or_404()

            # Return the response
            return jsonify({
                    'name'          : config_db.name,
                    'favorite'      : config_db.favorite,
                    'created'       : config_db.date,
                    'configs'       : dict(config_db)

                }), \
                SUCCESS_RESPONSE
    else:
        raise ConfigException("Not a valid json packet.")


print('[+] Adding route: ' + '/list/')

@app.route('/list/',                    methods = ['GET', 'PUT', 'POST'])
@login_required
def list_attribute():
    """
    Lists configs based on their attributes.

    args = {

            filters : {

                'name'  : name,
                'date'  : date,
                etc....
                }
            }

    :return:
    """

        # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        filters = request.json.get('filters')

        # We check if the session is valid
        if filters is None:
            raise ConfigException("Filters cannot be null.")
        else:

            # We have a non null config
            # Check the session

            filter_dict = json.loads(filters)


            # We add the config file only
            # Get the db entry
            filtered_db = Configuration.query.filter_by(**filter_dict).first_or_404()

            # Return the response
            return jsonify({
                    'name'          : filtered_db.name,
                    'created'       : filtered_db.date,
                    'configs'       : dict(filtered_db)

                }), \
                SUCCESS_RESPONSE
    else:
        raise ConfigException("Not a valid json packet.")


print('[+] Adding route: ' + '/list/favorite/')

@app.route('/list/favorite/',           methods = ['GET', 'PUT', 'POST'])
@login_required
def list_favorite():
    """
    Lists the favorites.
    :return:
    """

    # Check if the json is not none
    if request.json is not None:

        # We get the content of the request
        fav = request.json.get('name')

        # We check if the session is valid
        if fav is None:
            raise ConfigException("Favorite name cannot be null.")
        else:

            # We have a non null config
            # Check the session

            # We add the config file only
            # Get the db entry
            fav_db = Configuration.query.filter_by(name = fav).first_or_404()

            # Return the response
            return jsonify({
                    'name'          : fav_db.name,
                    'created'       : fav_db.date,
                    'favorite'      : dict(fav_db)

                }), \
                SUCCESS_RESPONSE
    else:
        raise ConfigException("Not a valid json packet.")

print('[+] Adding route: ' + '/list/favorites')

@app.route('/list/favorites',           methods = ['GET', 'PUT', 'POST'])
@login_required
def list_favorites():
    """
    Lists the favorites.
    :return:
    """

    # Get all configs in db and return them
    favorites = Favorite.query.all()
    favorite_dict = dict(favorites)

    return jsonify(
        {
            'favorites'     :   favorite_dict,
            'count'         :   favorites.count(),
            'date'          :   datetime.utcnow()
        }
    ), SUCCESS_RESPONSE