"""

    help.py
    ==========

    This module contains all the help text needed to send to
    the client when ever there is an error.

    :copyright: (c) 2015 by GammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         GammaRay
    Version:        1.0
    Date:           3/11/2015

"""

LOGIN_HELP      = """

    Login help
    ==========

        Possible commands:

            **  Registers a user with a specific username and
                password

                - /register/     + { username    : <username>,
                                    password    : <password> }

            **  Unregisters a user with a specific username

                - /unregister/   + { username    : <username> }

            **  Login a user based on a username and a password

                - /login/        + { username    : <username>,
                                    password    : <password> }

            **  Logout a user based on a username

                - /logout/       + { username    : <username> }
"""