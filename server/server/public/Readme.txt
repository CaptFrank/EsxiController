
    This is the site map for the REST Api Interface

        =================================
        ** General Operations
        **
        ** - Root directory listing:
        **    - /                                                 // Sends the API Urls below
        **    - /help                                             // Sends the API Urls below
        **
        ** - Login
        **    - /register       {username:username,
        **                        password:password}              // Create a user
        **    - /unregister     {username: username}              // Deletes a user
        **    - /login          {username:username}               // Login
        **    - /login/help
        **
        **    - /logout         {username:username}               // Logout
        **
        =================================
        ** Directory Listing
        **
        ** - Directory listings:
        **
        **    - /list/                                            // Sends how to
        **    - /list/all                                         // lists the registered configs
        **    - /list/<session>                                   // lists a session config
        **    - /list/<config>                                    // lists the config specified
        **    - /list/target/<target>                             // lists based on the target name
        **    - /list/arch/<architecture>                         // lists based on the target architecture
        **    - /list/platform/<platform>                         // lists based on the platform
        **
        **    - /list/type/<type>                                  // lists based on config type
        **    - /list/recent/                                      // lists the most recent
        **    - /list/access/<access>                              // lists on the accessed time
        **    - /list/date/<date>                                  // lists based on the date created
        **    - /list/user/<user>                                  // lists based on user
        **    - /list/favorites/                                   // lists the favorites
        **
        =================================
        ** Config Operations
        **
        ** - Registration of config
        **
        **    - /add/help                                         // Sends the how to
        **    - /add/favorite/<name>                              // Sets up a favorite record
        **    - /add/session/<name>                               // Adds a session
        **    - /add/session/config/<name>                        // Adds a session config
        **    - /add/config/<name>                                // Registers a config in global context
        **
        ** - Deleting a config
        **
        **    - /delete//help                                     // Sends the how to
        **    - /delete/session/<session>                         // Deletes a session
        **    - /delete/config/<config>                           // Deletes a config in global context
        **    - /delete/session/config/<config>                   // Deletes a config from a session
        **    - /delete/favorite/<favorite>                       // deletes a favorite
        **
        ** - Modify a config
        **
        **    - /modify//help                                     // Sends the how to
        **    - /modify/config/<config>                           // Modifies a config in global context
        **    - /modify/session/config/<config>                   // Modifies a config from a session
        **
        **
        ** - Favorite setting
        **
        **    - /favorite/help                                    // Sends how to
        **    - /favorite/set/config/<favorite>                   // Sets a global config
        **    - /favorite/set/session/<favorite>                  // Sets a session
        **
        =================================
        Server Operation

        - Run the backend engine

            - /run/                                             // Sends the how to
            - /run/<logging>/syslog/<syslog>/splunk/<splunk>    // Runs with the settings given

        - Kill the backend engine

            - /kill/                                            // Sends the how to
            - /kill/<reason>                                    // Kills with reason <logging>

        - Reset the backend engine

            - /reset/                                           // Sends the how to
            - /reset/<logging>/syslog/<syslog>/                 // Resets with the given variables
                    splunk/<splunk>/reason/<reason>

        - Status

            - /status/                                          // Sends the how to
            - /status/server/                                   // Sends backend server status
            - /status/web/                                      // Sends the web front end status

        =================================
        Task Operation

        - Adds a task to the backend server

            - /task/add/                                        // Sends the how to
            - /task/add/config/<config>                         // Sends a config task
            - /task/add/session/<session>/config/<config>       // Sends a session task
            - /task/add/session/<session>                       // Sends a session group to start

            - /task/add/favorite/config                         // Add the favorite config
            - /task/add/favorite/session                        // Add the favorite session

        - Deleting a task

            - /task/delete/                                     // Sends the how to
            - /task/delete/config/<config>                      // Deletes a config task
            - /task/delete/session/<session>/config/<config>    // Deletes a session task
            - /task/delete/session/<session>                    // Deletes a session group to start

            - /task/delete/favorite/config                      // Deletes the favorite config
            - /task/delete/favorite/session                     // Deletes the favorite session

        - Status

            - /task/status/                                     // Sends the how to
            - /task/status/config/<config>                      // Sends the task configs status
            - /task/status/session/<session>/config/<config>    // Sends the session configs status
            - /task/status/session/<session>                    // Sends the session configs status

            - /task/status/favorite/config                      // Sends the favorite config status
            - /task/status/favorite/session                     // Sends the favorite session status