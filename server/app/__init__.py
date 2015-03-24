
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

from server.db.db import *
from flask_sqlalchemy import *
from datetime import timedelta
from flask_login import LoginManager
from server.utils.client.client import *
from server.utils.logger.loggerengine import *


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

CLIENT_TITLE                    = 'CONTROLLER_CLIENT'
LOCALHOST                       = ''
DB_PATH                         = 'db/controllerClient.db'
CLIENT_PORT                     = 9999


"""
=============================================
Source
=============================================
"""

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

# ===================
# Application
# ===================

# Flask app
app = Flask(SERVER_NAME)
app.debug = True

# Change the duration of how long the Remember Cookie is valid on the users
# computer.  This can not really be trusted as a user can edit it.
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days = 14)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_ACCESS
app.config['SECRET_KEY'] = SECRET

# Import a module / component using its blueprint handler variable
from ..app.config.controllers import configs as config_module
from ..app.listing.controllers import listings as list_module
from ..app.login.controllers import login as login_module

# Register blueprint(s)
app.register_blueprint(config_module)
app.register_blueprint(list_module)
app.register_blueprint(login_module)

# ==================
# Database
# ==================

# Wrap the db to the app
db = setup_db(app)

# Init the db
init_db(db)

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

# Hook the app to the client
client_th.setup(app)

# Run the task
client_th.start()

# Run the app
app.run(debug = True)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 404

@app.before_request
def register_command():
    """
    In here we get the request info to store in the
    database.

    :return:
    """

    # Import the command history table def
    from server.app.engine.models import CommandHistory

    # Add a record
    db.session.add(CommandHistory(command = request.url_rule,
                                  type = 'Web',
                                  user = g.user))
    # Commit the record
    db.session.commit()
    return

@app.route('/help',             methods = ['GET'])
def index():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.txt')

