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

from daemon import runner
from server.utils.engine.enginecli import *
from server.utils.logger.loggerengine import *
from server.utils.engine.core.controller import *
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


# Logging levels
LOGGING_LEVELS                  = [
                                    'CRITICAL',
                                    'ERROR',
                                    'WARNING',
                                    'INFO',
                                    'DEBUG'
                                    ]

"""
=============================================
Source
=============================================
"""

class esxiControllerDaemon(object):
    """
    The daemon definition.
    """

    # Host file
    host_file                       = None

    # Args
    args                            = None

    # Configs
    configs                         = None

    # The root logger
    logger                          = None

    # The verbosity
    log_level                       = None

    # The syslogs
    syslog_enable                   = None

    # The controller object
    controller_handle               = None

    def __init__(self, args):
        """
        Setup the app and run
        :param args:            the args
        :return:
        """

        # ===========================
        # Host Configs
        # ===========================

        # We check for the configs
        self.host_file = args.config
        self.args = args

        # Check the file
        exist = os.path.isfile(self.host_file)
        if exist:
            print("[+] Host file selected...")

        else:
            print("[-] Invalid host file location...")
            exit(1)

        # We read the logging configs
        self.configs = ConfigParser()
        self.configs.read(self.host_file)

        # ===========================
        # App config
        # ===========================
        self.__setup()
        return

    def __setup(self):
        """
        This sets up the engine and spawns all the necessary
        threads needed to operate.

        :param args:            the args
        :return:
        """

        # ===========================
        # Logging
        # ===========================
        # In here we setup the logger engine

        self.__setup_logging()

        # ===========================
        # Controller
        # ===========================
        # In here we setup the controller object

        # Create a controller object
        self.controller_handle = controller(self.host_file, self.log_level)
        self.logger.info("Controller object created successfully.")

        # Setup the object
        # This creates a network stager engine.
        self.controller_handle.setup()
        self.logger.info("Controller object setup complete.")
        return

    def __setup_logging(self):
        """
        Sets up the logging engine.

        :return:
        """

        self.args.verbose = self.configs.get('host', 'log_level')
        self.args.syslog = self.configs.get('host', 'syslogger_enable')
        self.args.splunk = self.configs.get('host', 'splunk_enable')

        # We switch to get them
        # We setup the verbosity
        if self.args.verbose.upper() in LOGGING_LEVELS:
            self.log_level = self.args.verbose.upper()
        else:
            print('[+] Verbosity Level not recognized... Setting to INFO.')
            self.log_level = logging.INFO


        # Default logging configs
        logging_configs = {
            'syslog' : None,
            'splunk' : None
        }

        # ===========================
        # Syslogger
        # ===========================

        # We setup the syslog
        if self.args.syslog == 'enable':
            # We get the logging configs
            logging_configs['syslog'] = (self.configs.get('host', 'syslogger_address'),
                                         self.configs.get('host', 'syslogger_port'))

        # ===========================
        # Splunk
        # ===========================

        if self.args.splunk == 'enable':
            # We setup the logging engine
            logging_configs['splunk'] = {
                'token'     : self.configs.get('host', 'splunk_token'),
                'project'   : self.configs.get('host', 'splunk_project'),
                'api'       : self.configs.get('host', 'splunk_api')
            }

        # Set the logging attributes
        set_logger(logging_configs['syslog'],
                   logging_configs['splunk'])

        # Root logger
        self.logger = logging.getLogger('EsxiController')
        self.logger.info("Logging engine setup complete.")
        return

    def run(self):
        """
        This runs the engine application.

        :param args:        the args in a dict
        :return:
        """

        # We try forking the process
        self.controller_handle.run()
        self.logger.info("The controller is now running.")
        return

if __name__ == '__main__':

    # Start the engine
    engine = esxiControllerDaemon(args)
    daemon = runner.DaemonRunner(engine)
    daemon.daemon_context.files_preserve = logging.getLogger('').handlers
    daemon.do_action()

