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

import os

from flask import Flask
from ..server.db.db import *
from flask_httpauth import *

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

"""

# Server name
SERVER_NAME                     = "EsxiServer"

# Vcenter Handle
server                          = None

# Flask app
app                           = None

# The db
db                              = None

# The authentication interface
auth                            = None

"""
=============================================
Source
=============================================
"""

def setup():
    """
    Thi sets up the objects needed to start the REST api.

    :return:
    """

    return

def run_web_server():
    """
    This runs the application and its components.

    :return:
    """

    return

def run_service_server():
    """
    This is the service server entry point...

    :return:
    """

    return

def main():
    """
    We create a flask app here and create necessary
    objects to access the EsxiController (Vcenter)

    :return:
    """

    # Get global access
    global server
    global app
    global db
    global auth

    # ===================
    # Application
    # ===================

    # Create a flask app
    app         = Flask(SERVER_NAME)
    # Set debug
    app.debug   = True

    # ==================
    # Database
    # ==================

    # Wrap the db to the app
    db          = setup_db(app)
    # Init the db
    init_db(db)

    return

if __name__ == "__main__":
    main()

