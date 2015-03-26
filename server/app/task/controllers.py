"""

    controller.py
    ==========

    This is the controller to the task manager.

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

from server.app import client_th
from flask_login import login_required
from server.app.config.models import *
from server.utils.error.confighandler import *

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'app/task/static/'

"""
=============================================
Variables
=============================================
"""

# Configs object
tasks = Blueprint('task', __name__, url_prefix='/task')

"""
=============================================
Source
=============================================
"""

@tasks.route('/help',                          methods = ['GET', 'POST'])
def login_help():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

@tasks.route('/add',                           methods = ['PUT', 'POST'])
@login_required
def add_task(config = None):
    """
    Adds a task

    args = {
            'name' : <name>
            }
    :return:
    """

    if config is None:
        # Check if the json is not none
        if request.json is not None:
            config = request.json.get('name')

            if config is None:
                raise ConfigException('Config name cannot be null.')

    elif config is not None:

        # Get the config
        config_db = Configuration.query.filter_by(name = config).first_or_404()

        # Check the config
        if config_db is None:
            raise ConfigException('Config name not registered.')

        # We then take the config and get its configs string
        config_dict = dict(config_db)
        configs = json.dumps(config_dict['configs'])

        # Create a task record
        task_db = TaskStatus(name = config)
        db.session.add(task_db)
        db.session.commit()

        # Send the configs
        client_th.send_config(configs)
        task_db.push_update()
        return

    else:
        raise ConfigException("Message empty.")

@tasks.route('/add/favorite',                  methods = ['PUT', 'POST'])
@login_required
def add_favorite_task():
    """
    Gets the favorite config and sends it the interpreter

    args = {
            command type :  type
            }
    :return:
    """

    # Check if the json is not none
    if request.json is not None:
        config = request.json.get('command_type')

        if config is None:
            raise ConfigException('Config name cannot be null.')

        # Query the fav
        favorite = Favorite.query.filter_by(config_type = config).first_or_404()
        add_task(favorite.fav_config)

    return

@tasks.route('/delete',                        methods = ['PUT', 'POST'])
@login_required
def delete_task(config = None):
    """
    Deletes a task
    args = {
            'name' : <name>
            }
    :return:
    """

    if config is None:
        # Check if the json is not none
        if request.json is not None:
            config = request.json.get('name')

            if config is None:
                raise ConfigException('Config name cannot be null.')

    elif config is not None:

        # Get the config
        config_db = Configuration.query.filter_by(name = config).first_or_404()

        # Check the config
        if config_db is None:
            raise ConfigException('Config name not registered.')

        # We then take the config and get its configs string
        config_dict = dict(config_db)
        configs = json.dumps(config_dict['configs'])

        # Update a task record
        task_db = TaskStatus.query.filter_by(name = config).first_or_404()
        task_db.push_status(STATUS[ENGINE_STATUS_DELETED])

        # Send the configs
        client_th.delete_config(configs)
        return

    else:
        raise ConfigException("Message empty.")

@tasks.route('/delete/favorite',               methods = ['PUT', 'POST'])
@login_required
def delete_favorite_task():
    """
    Gets the favorite config and sends it the interpreter

    args = {
        command type :  type
        }
    :return:
    """

    # Check if the json is not none
    if request.json is not None:
        config = request.json.get('command_type')

        if config is None:
            raise ConfigException('Config name cannot be null.')

        # Query the fav
        favorite = Favorite.query.filter_by(config_type = config).first_or_404()
        delete_task(favorite.fav_config)
    return

@tasks.route('/status',                        methods = ['GET', 'POST'])
@login_required
def status_task():
    """
    Gets the status of a task

    args = {
            'name' : <name>
            }
    :return:
    """

    # Check if the json is not none
    if request.json is not None:
        config = request.json.get('name')

        if config is None:
            raise ConfigException('Config name cannot be null.')

        # Update a task record
        task_db = TaskStatus.query.filter_by(name = config).first_or_404()

        return jsonify({
            'task'  : task_db.name,
            'status': task_db.status
        }), \
        SUCCESS_RESPONSE
    else:
        raise ConfigException("Message empty.")