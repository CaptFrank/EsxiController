"""

    Engine
    ==========

    This module is the request engine for the backend of this
    application. It handles all the requests done by the webserver.

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
from subprocess import call
from server.utils.engine.enginecli import *
from server.utils.notification.notificationdispatch import *


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


___________                   .__  _________                       __                      .__    .__
\_   _____/   ______ ___  ___ |__| \_   ___ \    ____     ____   _/  |_  _______    ____   |  |   |  |     ____   _______
 |    __)_   /  ___/ \  \/  / |  | /    \  \/   /  _ \   /    \  \   __\ \_  __ \  /  _ \  |  |   |  |   _/ __ \  \_  __ \\
 |        \  \___ \   >    <  |  | \     \____ (  <_> ) |   |  \  |  |    |  | \/ (  <_> ) |  |__ |  |__ \  ___/   |  | \/
/_______  / /____  > /__/\_ \ |__|  \______  /  \____/  |___|  /  |__|    |__|     \____/  |____/ |____/  \___  >  |__|
        \/       \/        \/              \/                \/                                               \/

"""

# Application prologue
APP_PROLOGUE                    = """

Author:     {author}
Version:    {version}
Date:       {date}

"""

# Logging levels
LOGGING_LEVELS                  = [
                                    'CRITICAL',
                                    'ERROR',
                                    'WARNING',
                                    'INFO',
                                    'DEBUG'
                                    ]

# Confirm options
CONFIRM_OPTIONS                 = ['Yes', 'yes', 'YES', 'Y', 'y']
DENY_OPTIONS                    = ['No', 'no', 'NO', 'n', 'N']

# Message types
MESSAGE_TYPE                    = ['error', 'complete', 'test']

"""
=============================================
Source
=============================================
"""

def main():
    """
    This is the main context of the application.

    :return:
    """

    # Print the banner
    print(APP_TITLE)
    print(APP_PROLOGUE.format(author=__author__,
                              version=__version__,
                              date=__date__))

    # Get the args
    args = get_args()

    # ===========================
    # Notifications
    # ===========================

    # We send a test notification
    if args.test:

        # Create a notification dispatcher
        dispatcher = notificationDispatch()

        # Get inputs
        destination = input("[+] Destination address: ")
        dispatcher.send_notification(destination, 'test', 'test', None)
        return

    elif args.send:

        # Create a notification dispatcher
        dispatcher = notificationDispatch()

        # Get inputs
        destination = input("[+] Destination address: ")

        print('[+] Message types:')
        for item in MESSAGE_TYPE:
            print('[+]\t - %s' % item)

        msg_type = input("[+] Message Type: ")
        reason = input('[+] Reason: ')
        dispatcher.send_notification(destination, msg_type, reason, None)
        return

    # ===========================
    # Configs
    # ===========================

    # We print the configs
    if args.printConfig:
        call('more %s' % args.printConfigs)
        return

    # We diff the 2 configs
    elif args.diff:
        names = args.diff.remove("'")
        name1 = names.diff.split(" ")[0]
        name2 = names.diff.split(" ")[1]
        call('diff %s %s' %(name1, name2))
        return

    # ===========================
    # Operations
    # ===========================

    # Start Option
    if args.start:
        # Call the app
        call('python ./engine.py start')

    # Stop Option
    elif args.stop:
        # Stop daemon
        call('python ./engine.py stop')

    return

if __name__ == "__main__":
    main()