'''
Created on Nov 19, 2014

@author: fpapinea
'''

# =============================================================
# Imports
# =============================================================

import time
import logging

# =============================================================
# Constants
# =============================================================
LOGGER_LEVEL = logging.INFO
LOG_FILE_NAME = 'log/labcontroller-%s.log'

# =============================================================
# Source
# =============================================================

def set_logger():
    ''' 
    This method sets the LOGGER for the context of the 
    program.
    
    param test:                the test name
    '''
    
    # We set the file name
    filename = LOG_FILE_NAME % time.strftime('%d-%m-%y')

    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s]: %(name)-20s %(levelname)-20s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
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
    return
