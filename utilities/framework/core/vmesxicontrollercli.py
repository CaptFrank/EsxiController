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

=== Notification:

        --test
        --send
"""


# =============================================================
# Imports
# =============================================================

import argparse

# =============================================================
# Source
# =============================================================
__author__ = 'GammaRay'

def build_arg_parser():
    """
    Builds a list or arguments and parses the console arguments
    passed to this application.

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
        description='This group of commands is used to directly'
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
    # Add the console group
    console = parser.add_argument_group(
        title='Console Commands',
        description='This group of commands is used to directly'
                    'control the esxicontroller console output.'
    )

    console.add_argument('-v', '--verbose',
                        required=True,
                        action='store',
                        default='info',
                        choices=['info', 'error', 'critical'],
                        help='Sets the level for the console logging.')

    console.add_argument('-l', '--syslog',
                        required=True,
                        action='store',
                        default='enable',
                        choices=['enable', 'disable'],
                        help='Enables or disables the syslogger engine.')

    # =============================================================
    # Add the source group

    config = parser.add_argument_group(
        title='Configuration Source Commands',
        description='This group of commands is used to directly'
                    'control the esxicontroller configuration source.'
    )

    config.add_argument('-C', '--printCollection',
                required=False,
                action='store',
                help='Prints the available collections.')

    config.add_argument('-p', '--printConfig',
                required=False,
                action='store',
                help='Prints the specified config.')

    config.add_argument('-P', '--printAllConfigs',
                required=False,
                action='store',
                help='Prints the configs in the specified collection.')

    config.add_argument('-x', '--printDbStats',
                required=False,
                action='store',
                help='Prints the stats from the specified db name.')

    config.add_argument('-T', '--printCollectionStats',
                required=False,
                action='store',
                help='Prints the stats from the specified collection name.')

    config.add_argument('-o', '--checkCollection',
                required=False,
                action='store',
                help='Check the integrity of a specified collection.')

    config.add_argument('-e', '--setSource',
                required=False,
                action='store',
                choices=['file', 'db'],
                help='Sets the source of the configs.')

    config.add_argument('-q', '--setCurrent',
                required=False,
                action='store',
                help='Sets the current configuration.')

    config.add_argument('-f', '--setFavorite',
                required=False,
                action='store',
                help='Sets the favorite configuration.')

    config.add_argument('-F', '--saveConfig',
                required=False,
                action='store',
                choices=['file', 'db'],
                help='Saves the config in the specified repo.')

    config.add_argument('-E', '--editConfig',
                required=False,
                action='store',
                help='Edits the file configuration.')

    config.add_argument('-R', '--removeConfig',
                required=False,
                action='store',
                help='Removes a configuration file.')

    config.add_argument('-D', '--diff',
                required=False,
                action='store',
                help='Diff 2 configs.')

    # =============================================================
    # Add the vcenter group
    vcenter = parser.add_argument_group(
        title='Vcenter Commands',
        description='This group of commands is used to directly'
                    'control the esxicontroller vcenter server.'
    )

    vcenter.add_argument('-c', '--createSnapshot',
                required=False,
                action='store',
                help='Creates a snapshot of a vm.')

    vcenter.add_argument('-d', '--deleteSnapshot',
                required=False,
                action='store',
                help='Deletes a snapshot from a vm history.')

    vcenter.add_argument('-L', '--listSnapshots',
                required=False,
                action='store',
                help='Lists the snapshots for a vm.')


    # =============================================================
    # Add the notification group
    notification = parser.add_argument_group(
        title='Notification Commands',
        description='This group of commands is used to directly'
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
    build_arg_parser().print_help()
