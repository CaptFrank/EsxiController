"""

=== Notification:

        --test
        --send

"""

# =============================================================
# Imports
# =============================================================

import time
import logging

from utilities.framework.notification.vmnotificationdispatch import *


def test_notifications(destinations):
    """
    This sends a test message

    :param destinations:        the destinations to send the test emails
    :return:
    """

    dispatch = VmNotificationDispatch()
    dispatch.send_notification(destinations,
                               'test',
                               'testing',
                               'testing')
    return

def send_notifications(destinations, reason, message):
    """
    This sends a test message

    :param destinations:        the destinations to send the test emails
    :param reason:              the reason to send the message
    :param message:             the message to send
    :return:
    """

    dispatch = VmNotificationDispatch()
    dispatch.send_notification(destinations,
                               'test',
                               reason,
                               message)
    return