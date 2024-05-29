"""
Debugging the pubsub library to get better tracking messages during operation.

https://pypubsub.readthedocs.io/en/v4.0.3/usage/usage_advanced_debug.html
"""
import pubsub as pub
import pubsub.utils


class PubSubLogger(pubsub.utils.INotificationHandler):
    """
    Track all the messages that are published through the pubsub package.
    """

    def __init__(self):
        pub.addNotificationHandler(PubSubLogger())

    def onSendMessage(self, message):
        pass
