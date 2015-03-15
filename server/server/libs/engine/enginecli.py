"""

    Engine Cli
    ==========

    This module is the CLI interface to the process spawner.

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

import argparse

"""
=============================================
Source
=============================================
"""

def build_arg_parser():
    """
    This builds the parser engine.

    :return:
    """

    # =============================================================
    # Description

    parser = argparse.ArgumentParser(
        prog='EsxiController',
        description='Argument list to control the Esxi Lab Controller.'
    )

    # =============================================================
    # Add the control group
    control = parser.add_argument_group(
        title='Control Commands',
        description='This group of commands is used to directly '
                    'control the esxicontroller script.'
    )

    control.add_argument('-s', '--start',
                        required=False,
                        action='store',
                        help='Starts the session with the provided host configurations.')

    control.add_argument('-S', '--stop',
                        required=False,
                        default=True,
                        help='Stops the current session gracefully.')

    control.add_argument('-r', '--reset',
                        required=False,
                        default=True,
                        help='Resets a session.')

    control.add_argument('-k', '--kill',
                        required=False,
                        default=True,
                        help='Stops the current session viciously.')

    # =============================================================
    # Add the source group
    config = parser.add_argument_group(
        title='Configuration Source Commands',
        description='This group of commands is used to directly '
                    'control the esxicontroller configuration source.'
    )

    config.add_argument('-p', '--printConfig',
                required=False,
                action='store',
                help='Prints the specified config.')

    config.add_argument('-c', '--config',
                required=True,
                action='store',
                help='Sets the configs.')

    config.add_argument('-D', '--diff',
                required=False,
                action='store',
                help='Diff 2 configs.')

    # =============================================================
    # Add the console group
    console = parser.add_argument_group(
        title='Console Commands',
        description='This group of commands is used to directly '
                    'control the esxicontroller console output.'
    )

    console.add_argument('-v', '--verbose',
                        required=True,
                        action='store',
                        default='info',
                        choices=['info', 'debug', 'warning', 'error', 'critical'],
                        help='Sets the level for the console logging.')

    console.add_argument('-l', '--syslog',
                        required=True,
                        action='store',
                        default='enable',
                        choices=['enable', 'disable'],
                        help='Enables or disables the syslogger engine.')
    console.add_argument('-L', '--splunk',
                        required=True,
                        action='store',
                        default='enable',
                        choices=['enable', 'disable'],
                        help='Enables or disables the splunk engine.')

    # =============================================================
    # Add the notification group
    notification = parser.add_argument_group(
        title='Notification Commands',
        description='This group of commands is used to directly '
                    'control the esxicontroller notification server.'
    )

    notification.add_argument('-t', '--test',
                    required=False,
                    help='Tests the notification engine.')

    notification.add_argument('-A', '--send',
                required=False,
                action='store',
                help='Sends a message through the notification engine.')
    return parser

def get_args():
    """
    Supports the command-line arguments needed to form a connection to vSphere.
    """
    parser = build_arg_parser()
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    exit(0)