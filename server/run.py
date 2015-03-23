"""

    run.py
    ==========

    Runs a test server

    :copyright: (c) 2015 by GammaRay.
    :license: BSD, see LICENSE for more details.

    Author:         GammaRay
    Version:        1.0
    Date:           3/11/2015

"""

# Run a test server.
from server.app import app
app.run(host='0.0.0.0', port=8080, debug=True)