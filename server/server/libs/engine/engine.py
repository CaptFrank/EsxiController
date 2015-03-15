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
import multiprocessing

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

# Child process attributes
JOBS                            = []

# =============================================================
# Variables
# =============================================================

# Host file
host_file                       = None

# The root logger
logger                          = None

# The verbosity
log_level                       = None

# The syslogs
syslog_enable                   = None

# The controller object
controller_handle               = None

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

    global logger
    global log_level
    global syslog_enable

    # We switch to get them
    # We setup the verbosity
    if args.verbose.upper() in LOGGING_LEVELS:
        log_level = args.verbose.upper()
    else:
        print('[+] Verbosity Level not recognized... Setting to INFO.')
        log_level = logging.INFO


    # Default logging configs
    logging_configs = {
        'syslog' : None,
        'splunk' : None
    }

    # ===========================
    # Syslogger
    # ===========================

    # We setup the syslog
    if args.syslog == 'enable':
        # We get the logging configs
        logging_configs['syslog'] = (configs.get('host', 'syslogger_address'),
                                     configs.get('host', 'syslogger_port')),

    # ===========================
    # Splunk
    # ===========================

    if args.splunk == 'enable':
        # We setup the logging engine
        logging_configs['splunk'] = {
            'token'     : configs.get('host', 'splunk_token'),
            'project'   : configs.get('host', 'splunk_project'),
            'api'       : configs.get('host', 'splunk_api')
        }

    # Set the logging attributes
    set_logger(logging_configs['syslog'],
               logging_configs['splunk'])

    # Root logger
    logger = logging.getLogger('EsxiController')
    logger.info("Logging engine setup complete.")
    return


def setup(args):
    """
    This sets up the engine and spawns all the necessary
    threads needed to operate.

    :param args:            the args
    :return:
    """

    # Global handles
    global logger
    global host_file
    global log_level
    global controller_handle

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
    # In here we setup the logger engine

    setup_logging(args, configs)

    # ===========================
    # Controller
    # ===========================
    # In here we setup the controller object

    # Create a controller object
    controller_handle = controller(host_file, log_level)
    logger.info("Controller object created successfully.")

    # Setup the object
    # This creates a network stager engine.
    controller_handle.setup()
    logger.info("Controller object setup complete.")
    return

def run(args):
    """
    This runs the engine application.

    :param args:        the args in a dict
    :return:
    """



    # We try forking the process
    try:

        pid = multiprocessing.Process(target=process, args=(args,))
        if pid > 0:
            JOBS.append(pid)
            pid.start()

    except OSError, e:
        print("[-] Forking child process failed: %d (%s)" % (e.errno, e.strerror))
        print("[-] Exiting the main context.")
        exit(1)
    return

def process(args):
    """
    The process

    :return:
    """

    global logger
    global controller_handle

    # We setup the child process
    setup(args)

    # We run the main thread
    controller_handle.run()
    logger.info("The controller is now running.")
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
    run(args)
    return

if __name__ == "__main__":
    main()