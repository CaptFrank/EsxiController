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
from server.server.apps.login.models import *
from server.server.utils.error.loginhandler import *
from server.server.server import db, app, login_manager

"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201

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

