"""

    Engine
    ==========

    Start the engine module

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

from server.utils.engine.engineutils import *

"""
=============================================
Source
=============================================
"""

def start():
    """
    Start the engine
    :return:
    """

    # Call the app
    call('python %s/engine.py start' % os.getcwd())
    return

def stop():
    """
    Stop the engine
    :return:
    """

    # Stop daemon
    call('python %s/engine.py stop' % os.getcwd())
    return

def reset():
    """
    Reset the engine
    :return:
    """

    call('python %s/engine.py restart' % os.getcwd())
    return