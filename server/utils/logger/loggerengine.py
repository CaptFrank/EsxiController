'''
Created on Nov 19, 2014

@author: fpapinea
'''

"""
=============================================
Imports
=============================================
"""

import os
import time
import logging
import logging.handlers
from splunk_logger import SplunkLogger

"""
=============================================
Constant
=============================================
"""

LOGGER_LEVEL = logging.INFO
LOG_FILE_DIR = '/var/log/esxicontroller/'
LOG_FILE_NAME = '/var/log/esxicontroller/labcontroller-%s.log'

"""
=============================================
Source
=============================================
"""

def set_logger(syslog_address=None, splunk_configs=None):
    """
    This method sets the LOGGER for the context of the 
    program.

    The splunk api logging struct is as followed:

        splunk_configs = {

            'token' : < access token >,
            'project' : < project id >,
            'api' : < api domain >
            }
    
    :param syslog_address:                the syslog server address
    :param splunk_configs:                the configs for the splunk logging engine
    """

    # Check to see if the dir is existent
    if not os.path.isdir(LOG_FILE_DIR):
        print('[-] Logging directory does not exist, creating.')

        # We create a dir
        os.makedirs(LOG_FILE_DIR)
        print('[+] Logging directory created: %s.' % LOG_FILE_DIR)

    # We set the file name
    filename = LOG_FILE_NAME % time.strftime('%d-%m-%y')

    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s]: %(name)-20s %(levelname)-20s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename=filename,
                        filemode='a')

    # We create the root LOGGER for console
    logger_console = logging.StreamHandler()
    logger_console.setLevel(LOGGER_LEVEL)

    # Create a formatter
    logger_formatter = logging.Formatter('[%(asctime)s]: %(name)-50s: %(levelname)-20s %(message)s')

    # We set the formatters
    logger_console.setFormatter(logger_formatter)

    # We set the root handlers
    logging.getLogger('').addHandler(logger_console)
    print('[+] Added a console logging engine...')

    if syslog_address:
        add_syslogger(syslog_address)

    if splunk_configs:
        add_splunklogger(splunk_configs)
    return

def add_syslogger(address):
    """
    This adds a syslogger instance to the root logger
    instance.

    :param address:             the address of the syslog server
    :return:
    """

    # Add the syslogger
    syslogger = logging.handlers.SysLogHandler(address=address)  #('syslog.haligonia.home.com',514))
    logging.getLogger('').addHandler(syslogger)
    print('[+] Added a syslog logging engine...')
    return

def add_splunklogger(configs):
    """
    This adds a splunk logger instance to the root logger
    instance.

    :param configs:             the dict containing the configs
    :return:
    """

    # Add the splunk logger
    splunk = SplunkLogger(access_token=configs['token'],
                          project_id=configs['project'],
                          api_domain=configs['api'])
    logging.getLogger('').addHandler(splunk)
    print('[+] Added a splunk logging engine...')
    return
