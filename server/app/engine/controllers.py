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
from flask_login import login_required
from server.app.engine.models import *
from server.utils.engine import *
from server.utils.error.enginehandler import *

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'engine/static/'

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

@engine.route('/',                              methods = ['GET', 'POST'])
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
    This runs the backend engine.

    The args passed to the REST API are as follows:

    args    = {

        'log_level'     :   <level>,
        'splunk'        :   {
                            'enable'    :   False,
                            'settings'  :   <settings>
                            },
        'syslog'        :   {
                            'enable'    :   False,
                            'settings'  :   <settings>
                            },
            }
    }

    """

    # We check if we have all the needed attributes.
    if request.json is not None:

        # We get the user attributes
        logger = request.json.get('log_level')
        splunk = request.json.get('splunk')
        syslog = request.json.get('syslog')

        # Get the engine object
        engine_db = EngineStatus.query.all().first_or_404()
        engine_db.push_engine_attributes(logger, syslog, splunk)

        # Push a running status
        engine_db.push_status(ENGINE_STATUS_RUNNING)

    else:
        raise EngineException("Not a valid json packet.")

    # Start the engine
    start()
    return

@engine.route('/kill',                          methods = ['PUT', 'POST'])
@login_required
def kill():
    """
    This kills the backend engine
    :return:
    """
    engine_db = EngineStatus.query.all().first_or_404()
    # Push a running status
    engine_db.push_status(ENGINE_STATUS_STOPPED)
    stop()
    return

@engine.route('/reset',                         methods = ['PUT', 'POST'])
@login_required
def reset():
    """
    This resets the backend engine.
    :return:
    """
    engine_db = EngineStatus.query.all().first_or_404()
    # Push a running status
    engine_db.push_status(ENGINE_STATUS_RUNNING)
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