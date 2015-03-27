
"""

    EsxiServer
    ==========

    This module is meant to be the base point for the REST
    API server that will serve the internal network.

    It will offer the ability to GET, POST, HEAD, PUT, DELETE
    and OPTIONS to the server. This will allow for a cleaner more
    universal entry point to the task spawning from the EsxiController
    application.

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
from flask_login import LoginManager
from flask_sqlalchemy import *
from server.utils.client.client import *
from server.utils.logger.loggerengine import *
from server.utils.error.confighandler import *
from server.utils.error.enginehandler import *
from server.utils.error.listinghandler import *
from server.utils.error.loginhandler import *
from server.utils.error.taskhandler import *

"""
=============================================
Constants
=============================================
"""

# Program Attributes
__author__                      = "GammaRay"
__version__                     = "1.0"
__date__                        = "3/11/2015"

# Application Title
APP_TITLE                       = """

 ____|           _)  ___|             |             | |             ___|
 __|    __|\ \  / | |      _ \  __ \  __|  __| _ \  | |  _ \  __| \___ \   _ \  __|\ \   / _ \  __|
 |    \__ \ `  <  | |     (   | |   | |   |   (   | | |  __/ |          |  __/ |    \ \ /  __/ |
_____|____/ _/\_\_|\____|\___/ _|  _|\__|_|  \___/ _|_|\___|_|    _____/ \___|_|     \_/ \___|_|


"""

# The app static directory
APP_STATIC_DIRECTORY            = 'public/'

# Server name
SERVER_NAME                     = "EsxiServer"

# Debugging
DEBUG                           = True

# Threads
THREADS                         = 2

# Secrets
SECRET                          = 'haligonia123!'


"""
=============================================
Source
=============================================
"""

# =====================
# Database
# =====================

def setup_db(app):
    """
    Returns a hanlde to a sql database.

    The database config must be in the app.config dict

        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_ACCESS

    :param app:             the web app and its configs
    :return:
    """

    return SQLAlchemy(app)

def init_db(db):
    """
    Import all modules here that might define models so that
    they will be registered properly on the metadata. Otherwise
    you will have to import them first before calling init_db()

    :param db:              the database handle
    :return:
    """

    # Create all models
    db.create_all()
    db.session.commit()
    return

# ===================
# Application
# ===================

# Flask app
app = Flask(SERVER_NAME)
app.config.from_pyfile('config.py')

# ==================
# Database
# ==================

# Wrap the db to the app
db = setup_db(app)

# ==================
# Login
# ==================

# The authentication interface
login_manager = LoginManager()

# Tell the login manager where to redirect users to display the login page
login_manager.login_view = "/login/"

# Init the application context
login_manager.init_app(app)

# ==================
# Backend connection
# ==================

# Create a client thread object
client_th = client()

# Import a module / component using its blueprint handler variable
from server.app.config.controllers import configs as config_module
from server.app.listing.controllers import listings as list_module
from server.app.login.controllers import login_engine as login_module
from server.app.engine.controllers import engine as engine_module
from server.app.task.controllers import tasks as task_module

# Register blueprint(s)
app.register_blueprint(config_module)
app.register_blueprint(list_module)
app.register_blueprint(login_module)
app.register_blueprint(engine_module)
app.register_blueprint(task_module)


@app.route('/',                 methods = ['GET', 'POST'])
@app.route('/help',             methods = ['GET', 'POST'])
def index():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')


'''@app.errorhandler(ListingException)
@app.errorhandler(LoginException)
@app.errorhandler(ConfigException)
def handle_web_exception(error):
    """
    The handler function to call from the context.

    :param error:                       the error to send
    :return:
    """

    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    statuses = db.session.query(WebStatus).all()
    for item in statuses:
        item.push_update()
        item.push_status(WEB_STATUS_ERROR)
    return response

@app.errorhandler(EngineException)
def handle_engine_exception(error):
    """
    The handler function to call from the context.

    :param error:                       the error to send
    :return:
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    statuses = db.session.query(EngineStatus).all()
    for item in statuses:
        item.push_update()
        item.push_status(ENGINE_STATUS_ERROR)
    return response


@app.errorhandler(TaskException)
def handle_task_exception(error, name):
    """
    The handler function to call from the context.

    :param error:                       the error to send
    :return:
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    statuses = db.session.query(WebStatus).all()
    for item in statuses:
        item.push_update()
        item.push_status(WEB_STATUS_ERROR)

    task_status = TaskStatus.query.filter_by(name = name).first_or_404()
    task_status.push_status(ENGINE_STATUS_ERROR)
    return response
'''

'''@app.before_request
def register_command():
    """
    In here we get the request info to store in the
    database.

    :return:
    """

    # Import the command history table def
    from server.app.engine.models import CommandHistory, CommandStats

    # Add a record
    db.session.add(
        CommandHistory(
            command = request.url_rule,
            type = COMMAND_SOURCE_WEB,
            user = g.user
        )
    )

    # Commit the record
    db.session.commit()

    # Update the queries
    temp = CommandStats.query.filter_by(
        command_type = COMMAND_SOURCE_WEB
    ).first()

    temp.push_update(command = request.url_rule)
    return'''

if __name__ == '__main__':


    # Print the banner
    print(APP_TITLE)
    print('Author:  \t\t' + __author__)
    print('Date:    \t\t' + __date__)
    print('Version: \t\t' + __version__)
    time.sleep(2)

    # ===================
    # Logging
    # ===================

    # Create the logging engine
    set_logger()

    # Hook the app to the client
    client_th.setup(app)

    # Init the db
    init_db(db)

    # Run the task
    client_th.start()

    # Run the app
    app.run()


