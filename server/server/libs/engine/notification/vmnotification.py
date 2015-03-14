# =============================================================
# Imports
# =============================================================

import time
import pprint
from email.mime.text import MIMEText

from server.server.libs.engine.notification.vmnotificationtemplates import *

# =============================================================
# Source
# =============================================================


class VmNotification(object):
    """
    This is the notification engine for the framework. It
    houses the possible messages that can be sent and the formatting
    of each message.
    """

    @staticmethod
    def get(notification):
        """
        This gets the message type that is requested

        :param notification:    the message type
        :return:
        """

        # We get the message
        return MESSAGE_TYPES[notification]

    @staticmethod
    def format(destination, message, reason, configs):
        """
        This formats the passed message with the configs passed.

        :param message:         the message to send
        :param reason:          the reason why we send the message
        :param configs:         the configs to record
        :return:
        """

        # We need the following:
        # Time, Reason, Configs
        namespace = {
            'time': time.strftime('%y-%m-%d %H:%M:%S'),
            'configs': pprint.pprint(configs),
            'reason': reason
            }
        message = Template(message, searchList=[namespace])

        # Setup message
        structure = MIMEText(message, 'html')
        structure['Subject'] = 'EsxiController - Notification'
        structure['From'] = 'EsxiController'
        structure['To'] = destination

        return structure