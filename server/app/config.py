
# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/db.db'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 1

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "haligonia123!"

# Secret key for signing cookies
SECRET_KEY = "haligonia123!"

from datetime import timedelta

# Change the duration of how long the Remember Cookie is valid on the users
# computer.  This can not really be trusted as a user can edit it.
REMEMBER_COOKIE_DURATION = timedelta(days = 14)