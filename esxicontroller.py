"""
This is the main access to get all the programmed features of the
esxicontroller class. We define all command line access variables in this
file.

The possible commands are as follows:

=== Operations:

        --start
        --stop
        --reset
        --kill

=== Console:

        --verbose=[info, critical, error]
        --syslog=[enable, disable]

=== Configuration:

        * Print:
            --printCollection
            --printConfig
            --printAllConfigs
            --printDbStats
            --printCollectionStats

        * Check:
            --checkCollection

        * Set:
            --setSource
            --setCurrent
            --setFavorite
            --saveConfig
            --editConfig

        * Remove:
            --removeConfig

        * Diff Configs:
            --diff

=== VCenter:

        * Snapshots:
            --createSnapshot
            --deleteSnapshot
            --listSnapshots
            --powerOn
            --powerOff

=== Notification:

        --test
        --send
"""


# =============================================================
# Imports
# =============================================================

import time
import logging
import configparser

from utilities.framework.core.vmloggerengine import *
from utilities.framework.core.vmesxicontrollercli import *
from utilities.framework.core.vmesxicontrollerbase import *

# =============================================================
# Constants
# =============================================================

APP_TITLE = """
__________             ______________            _____             ___________
___  ____/__________  ____(_)_  ____/______________  /________________  /__  /____________
__  __/  __  ___/_  |/_/_  /_  /    _  __ \_  __ \  __/_  ___/  __ \_  /__  /_  _ \_  ___/
_  /___  _(__  )__>  < _  / / /___  / /_/ /  / / / /_ _  /   / /_/ /  / _  / /  __/  /
/_____/  /____/ /_/|_| /_/  \____/  \____//_/ /_/\__/ /_/    \____//_/  /_/  \___//_/

"""

# App attributes
__version__ = '1.0'
__date__ = '3/6/2015'
__author__ = 'GammaRay'
__contact__ = 'pgammarayq@gmail.com'

# Logging levels
LOGGING_LEVELS = [
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG'
]

# Default host file location
DEFAULT_HOST_LOCATION = "configurations/host.conf"

# Confirm options
CONFIRM_OPTIONS = [
    'yes',
    'YES'
]

# =============================================================
# Variables
# =============================================================

# Host file
host_file = None

# The verbosity
log_level = None

# The syslogs
syslog_enable = None

# The VmEsxiController
vm_controller = None


# =============================================================
# Source
# =============================================================

def main():
    """
    This is the main function for the application.
    """

    print(APP_TITLE)
    print('Date: ' + __date__)
    print('Version: ' + __version__)
    print('Author: ' + __author__)
    print('Contact: ' + __contact__)
    time.sleep(1)

    global host_file
    global vm_controller

    # Read the configs
    configs = configparser.ConfigParser()
    host_file = raw_input("Please enter the host config file path or [yes] to confirm\n"
                          "[default: configurations/host.conf]: ")

    if host_file in CONFIRM_OPTIONS:
        host_file = DEFAULT_HOST_LOCATION

    configs.read(host_file)

    # We get the arguments passed to the application
    args = get_args()

    # ===========================
    # Logging
    # ===========================
    setup_logging(args, configs)

    # ===========================
    # Controller Base
    # ===========================
    vm_controller = VmEsxiControllerBase(host_file, log_level)

    return

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

    # We setup the syslog
    if args.syslog == 'enable':
        set_logger((configs.get('host', 'syslogger_address'),
                    configs.get('host', 'syslogger_port')))
    else:
        set_logger(None)
    return

if __name__ == '__main__':
    main()