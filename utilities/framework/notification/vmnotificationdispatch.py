
# =============================================================
# Imports
# =============================================================

import logging
import smtplib

from utilities.framework.notification.vmnotification import VmNotification

# =============================================================
# Constant
# =============================================================

MAIL_SERVER = 'mail.haligonia.home.com'
ESXI_CONTROLLER_ADDRESS = 'esxicontroller@mail.haligonia.home.com'

# =============================================================
# Source
# =============================================================

class VmNotificationDispatch(object):
    """
    This is the message dispatcher for the ESXI controller
    framework.
    """

    # The destination address
    __destination = None

    # The message type
    __msg_type = None

    # The message to send
    __message = None

    # Logger
    __logger = None

    def __init__(self, log_level=logging.INFO):
        """
        This is the default constructor for the class
        :return:
        """

        self.__logger = logging.getLogger("ESXiController - VmNotificationDispatch")
        self.__logger.setLevel(log_level)
        return

    def send_notification(self, dest_address, msg_type, reason, configs):
        """
        This sends out the message object.

        :param dest_address:            the destination address
        :param msg_type:                the message type to send
        :param reason:                   the reason to notify
        :param configs:                  the configs
        :return:
        """

        # Set internals
        self.__destination = dest_address
        self.__msg_type = msg_type

        # We create an smtp server on our mail server
        server = smtplib.SMTP(MAIL_SERVER)

        # Create the message
        self.__setup_message(reason, configs)

        # Send the message
        server.sendmail(ESXI_CONTROLLER_ADDRESS, self.__destination, self.__message.as_string())
        server.quit()
        return

    def __setup_message(self, reason, configs):
        """
        This is the message setup routine that is called when writing the
        notification email.

        :param reason:                  the reason
        :param configs:                 the vm configs
        :return:
        """

        # We get the message type
        self.__message = VmNotification.get(self.__msg_type)
        self.__message = VmNotification.format(self.__destination,
                                               self.__message,
                                               reason,
                                               configs)
        return