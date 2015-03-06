
# =============================================================
# Imports
# =============================================================

from Cheetah.Template import Template


# =============================================================
# Constants
# =============================================================

COMPLETE_MESSAGE = \
    """
    <html>
        <head><title>EsxiController - <span style="color:#00FF00;">Complete</span> - [$time]</title></head>
        <h1 style="font-style: italic;"><strong><span style="color:#00FF00;">Complete </span></strong>Notification from Esxi Controller</h1>
        <body>
            <p>
                #####################################################
                <br>
                Hi this is a message from the Esxi Controller.  <br>
                This notification is sent out for the following <br>
                reason:                                         <br>
                <br>
                #####################################################
                <br>
                    - $reason                                   <br>
                <br>
                #####################################################
                <br>
                    - $configs                                  <br>
                <br>
                #####################################################
                <br>
                This request was officially executed at: $time  <br>
                <br>
                Thanks for using EsxiController Smtp Server.    <br>
                Sincerely,                                      <br>
                EsxiController
            </p>
        </body>
    </html>
    """

TEST_MESSAGE = \
    """
    <html>
        <head><title>EsxiController - <span style="color:#00FF00;">Test</span> - [$time]</title></head>
        <h1 style="font-style: italic;"><strong><span style="color:#00FF00;">Test </span></strong>Notification from Esxi Controller</h1>
        <body>
            <p>
                #####################################################
                <br>
                Hi this is a message from the Esxi Controller.  <br>
                This notification is sent out for the following <br>
                reason:                                         <br>
                <br>
                #####################################################
                <br>
                    - $reason                                   <br>
                <br>
                #####################################################
                <br>
                This request was officially executed at: $time  <br>
                <br>
                Thanks for using EsxiController Smtp Server.    <br>
                Sincerely,                                      <br>
                EsxiController
            </p>
        </body>
    </html>
    """

ERROR_MESSAGE = \
    """
    <html>
        <head><title>EsxiController - <span style="color:#FF0000;">Error</span> - [$time]</title></head>
        <h1 style="font-style: italic;"><strong><span style="color:#FF0000;">Error </span></strong>Notification from Esxi Controller</h1>
        <body>
            <p>
                #####################################################
                <br>
                Hi this is a message from the Esxi Controller.  <br>
                This notification is sent out for the following <br>
                reason:                                         <br>
                <br>
                #####################################################
                <br>
                    - $reason                                   <br>
                <br>
                #####################################################
                <br>
                    - $configs                                  <br>
                <br>
                #####################################################
                <br>
                This request was officially executed at: $time  <br>
                <br>
                Thanks for using EsxiController Smtp Server.    <br>
                Sincerely,                                      <br>
                EsxiController
            </p>
        </body>
    </html>
    """

# Message type mapped
MESSAGE_TYPES = {

    'error': ERROR_MESSAGE,
    'complete': COMPLETE_MESSAGE,
    'test': TEST_MESSAGE
}