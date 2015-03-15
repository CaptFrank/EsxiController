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
from Queue import Queue
from server.server.libs.engine.enginecli import *
from server.server.libs.logger.loggerengine import *
from server.server.libs.engine.core.controller import *

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
 |    __)_   /  ___/ \  \/  / |  | /    \  \/   /  _ \   /    \  \   __\ \_  __ \  /  _ \  |  |   |  |   _/ __ \  \_  __ \
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

# =============================================================
# Variables
# =============================================================

# Host file
host_file                       = None

# The verbosity
log_level                       = None

# The syslogs
syslog_enable                   = None

# The controller object
controller                      = None

"""
=============================================
Source
=============================================
"""

def setup_logging(args, configs):
    """
    Sets up the logging engine.

    :return:
    """

    global log_level
    global syslog_enable

    # We switch to get them
    # We setup the verbosity
    if args.verbose.upper() in LOGGING_LEVELS:
        log_level = args.verbose.upper()
    else:
        print('[+] Verbosity Level not recognized... Setting to INFO.')
        log_level = logging.INFO

    logging_configs = {
        'syslog' : None,
        'splunk' : None
    }

    # We setup the syslog
    if args.syslog == 'enable':
        # We get the logging configs
        logging_configs['syslog'] = (configs.get('host', 'syslogger_address'),
                                       configs.get('host', 'syslogger_port')),

    if args.splunk == 'enable':
        # We setup the logging engine
        logging_configs['splunk'] = {
            'token'     : configs.get('host', 'splunk_token'),
            'project'   : configs.get('host', 'splunk_project'),
            'api'       : configs.get('host', 'splunk_api')
        }

    set_logger(logging_configs['syslog'],
               logging_configs['splunk'])

    return


def setup(args):
    """
    This sets up the engine and spawns all the necessary
    threads needed to operate.

    :param args:            the args
    :return:
    """

    # Global handles
    global host_file
    global log_level
    global syslog_enable
    global controller

    # ===========================
    # Host Configs
    # ===========================

    # We check for the configs
    host_file = args.config

    # Check the file
    exist = os.path.isfile(host_file)
    if exist:
        print("[+] Host file selected...")

    else:
        print("[-] Invalid host file location...")
        exit(1)

    # We read the logging configs
    configs = ConfigParser.ConfigParser()
    configs.read(host_file)

    # ===========================
    # Logging
    # ===========================


    # ===========================
    # Controller
    # ===========================
    return

def run():
    """
    This runs the engine application.

    :return:
    """

    return

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

    # We setup the engine
    setup(args)

    return

if __name__ == "__main__":
    main()