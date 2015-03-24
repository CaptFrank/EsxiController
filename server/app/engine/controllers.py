"""

    controller.py
    ==========

    This is the controller to the engine.

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
from server.app import app
from flask_login import login_required
from server.app.engine.models import *
from server.utils.engine import *

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'app/engine/static/'

"""
=============================================
Variables
=============================================
"""

# Configs object
engine = Blueprint('engine', __name__, url_prefix='/engine')

"""
=============================================
Source
=============================================
"""

@engine.route('/help',                          methods = ['GET', 'POST'])
def login_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

@engine.route('/run',                           methods = ['PUT', 'POST'])
@login_required
def run():
    """
    This runs the backend engine

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


    start()
    return

@engine.route('/kill',                          methods = ['PUT', 'POST'])
@login_required
def kill():
    """
    This kills the backend engine
    :return:
    """
    stop()
    return

@engine.route('/reset',                         methods = ['PUT', 'POST'])
@login_required
def reset():
    """
    This resets the backend engine.
    :return:
    """
    reset()
    return

@engine.route('/status/server',                 methods = ['GET', 'POST'])
@login_required
def status_server():
    """
    This gets the server status
    :return:
    """
    return EngineStatus.query.all()

@engine.route('/status/web',                    methods = ['GET', 'POST'])
@login_required
def status_web():
    """
    This gets the web server status
    :return:
    """
    return WebStatus.query.all()

@engine.route('/status/users',                  methods = ['GET', 'POST'])
@login_required
def status_users():
    """
    This is the users status
    :return:
    """
    return UserStats.query.all()

@engine.route('/status/command_history',        methods = ['GET', 'POST'])
@login_required
def status_command_history():
    """
    This is the command history
    :return:
    """
    return CommandHistory.query.all()