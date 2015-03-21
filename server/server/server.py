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

from datetime import timedelta

from flask import *
from flask_login import LoginManager

from server.server.db.db import *
from server.server.utils.client.client import *


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

CLIENT_TITLE                    = 'CONTROLLER_CLIENT'
LOCALHOST                       = ''
DB_PATH                         = 'db/controllerClient.db'

CLIENT_PORT                     = 9999

"""
=============================================
Variables
=============================================
"""

# Vcenter Handle
server                          = None

# Flask app
app                             = None

# The db
db                              = None

# The authentication interface
login_manager                   = None

# The storage engine
storage                         = None

# Client messager
client_th                       = None

"""
=============================================
Source
=============================================
"""

@app.route('/',                 methods = ['GET'])
@app.route('/help',             methods = ['GET'])
def index():
    """
    This method returns a jasonified help dict for
    for the login app.

    :return:
    """
    return send_from_directory(APP_STATIC_DIRECTORY, 'Readme.md')

def main():
    """
    We create a flask app here and create necessary
    objects to access the EsxiController (Vcenter)

    :return:
    """

    # Print the banner
    print(APP_TITLE)
    print('Author:  \t\t' + __author__)
    print('Date:    \t\t' + __date__)
    print('Version: \t\t' + __version__)
    time.sleep(2)

    # Get global access
    global login_manager
    global storage
    global server
    global client_th
    global app
    global db

    # ===================
    # Application
    # ===================

    # Create a flask app
    app = Flask(SERVER_NAME)
    # Set debug
    app.debug = True

    # Change the duration of how long the Remember Cookie is valid on the users
    # computer.  This can not really be trusted as a user can edit it.
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days = 14)

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

    # Flask-Login Login Manager
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
    client_th.run()
    return

if __name__ == "__main__":
    main()

