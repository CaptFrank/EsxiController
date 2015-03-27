
    This is the site map for the REST Api Interface

        =================================
        ** General Operations
        **
        ** - Root directory listing:
        **    - /
        **    - /help
        **
        ** - Login
        **    - app/register
        **    - app/unregister
        **    - app/login
        **    - app/logout
        **

        =================================
        ** Directory Listing
        **
        ** - Directory listings:
        **
        **    - /listings/all
        **    - /listings/
        **    - /listings/config/
        **    - /listings/session/config/
        **    - /list/favorites/
        **    - /list/favorite/
        **

        =================================
        ** Config Operations
        **
        ** - Registration of config
        **
        **    - /configs/help
        **    - /configs/add/favorite/<name>
        **    - /configs/add/session/<name>
        **    - /configs/add/session/config/<name>
        **    - /configs/add/config/<name>
        **
        ** - Deleting a config
        **
        **    - /configs/delete/session/<session>
        **    - /configs/delete/config/<config>
        **    - /configs/delete/session/config/<config>
        **    - /configs/delete/favorite/<favorite>
        **
        ** - Modify a config
        **
        **    - /configs/modify/config/<config>
        **    - /configs/modify/session/config/<config>
        **
        **
        ** - Favorite setting
        **
        **    - /configs/favorite/set/config/<favorite>
        **    - /configs/favorite/set/session/<favorite>
        **    - /configs/favorite/get/config/<favorite>
        **    - /configs/favorite/get/session/<favorite>
        **

        =================================
        ** Server Operation
        **
        **    - /engine/help
        **
        ** - Run the backend engine
        **
        **    - /engine/run/
        **
        ** - Kill the backend engine
        **
        **    - /engine/kill/
        **
        ** - Reset the backend engine
        **
        **    - /engine/reset/
        **
        ** - Status
        **
        **    - /status/
        **    - /status/server/
        **    - /status/web/
        **    - /status/users/
        **    - /status/command_history/
        **
        =================================
        ** Task Operation
        **
        ** - Adds a task to the backend server
        **
        **    - /task/add/
        **    - /task/add/favorite/
        **
        ** - Deleting a task
        **
        **    - /task/delete/
        **    - /task/delete/favorite/
        **
        ** - Status
        **
        **    - /task/status/