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
from configparser import ConfigParser
from flask import request, session, redirect, url_for, abort

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
SERVER                          = None

# Flask app
FLASK                           = None

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
    global SERVER
    global FLASK

    # Create a flask app
    FLASK = Flask(SERVER_NAME)

    # Setup the app
    setup()

    # Run the app
    run_service_server()
    run_web_server()
    return

if __name__ == "__main__":
    main()

