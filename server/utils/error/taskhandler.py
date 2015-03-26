"""

    task.py
    ==========

    This is the task handler for the error handler.

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

from server.utils.error.basehandler import *
from server.app.engine.models import *
from server.app import app
from flask import *

"""
=============================================
Source
=============================================
"""

class TaskException(BaseHandler):
    """
    This class provides a base class to the error handlers that
    will later be implemented to tell the user that there
    has been a problem with the REST API transaction.
    """

    # The base error status code
    status_code = 400

    def __init__(self, message, status_code = None, payload = None):
        """
        This is the base default constructor.

        :param message:                 the message to print
        :param status_code:             the status code to send
        :param payload:                 the payload to send
        :return:
        """

        # Override the Exception class
        Exception.__init__(self)

        # Set the message
        self.message = message

        # Set the status code
        if status_code is not None:
            self.status_code = status_code

        # Set the payload
        self.payload = payload
        return

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