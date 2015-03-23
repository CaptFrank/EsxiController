"""

    controller.py
    ==========

    This is the controller to the enigne.

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
from server.utils.error.confighandler import *



"""
=============================================
Constant
=============================================
"""

SUCCESS_RESPONSE            = 201
APP_STATIC_DIRECTORY        = 'app/listing/static/'

"""
=============================================
Variables
=============================================
"""

# Configs object
listings = Blueprint('listings', __name__, url_prefix='/listings')

"""
=============================================
Source
=============================================
"""