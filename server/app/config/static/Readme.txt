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