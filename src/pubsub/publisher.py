from typing import Callable, Dict, Any

from loggers.log import Log


class Publisher:
    """
    Publisher class responsible for publishing messages and sending them to all their subscribers. The publisher sends
    out messages as string typed variables that subscribers are able to receive.


    ... code-block:: python
        class Listener:
            def callback(self, message):
                print(f'Listener received: {message}')

        listener = Listener()

        publisher = Publisher()
        publisher.subscribe('Unique.Message'. listener.callback)


        publisher.publish('Unique.Message', 'Published Message')

        >>> 'Listener received: Published Message'
    """

    subscribers: Dict[(int, str), Callable[[Any], Any]]
    """
    Subscriber dictionary containing the listener hash and the callback string as the keys. The value stored
    in the dictionary contains the callback listener function that subscribed to the event.
    """

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, message: str, listener: Callable) -> None:
        """
        Subscribe to a given message and callback the listener function

        :param message:
        :param listener:
        """
        key = hash(listener), message
        if key in self.subscribers:
            Log.info(f'Subscription failed, listener already subscribed: {key}.')
            return

        self.subscribers[key] = listener
        Log.info(f'Subscribed to event: {key}')

    def unsubscribe(self, message: str, listener: Callable) -> None:
        key = hash(listener), message
        if key not in self.subscribers:
            Log.info(f'Unable to unsubscribe from message, instance not found: {key}')
            return

        self.subscribers.pop(key)
        Log.info(f'Unsubscribed from event: {key}')

    def send_message(self, message: str, **kwargs) -> None:
        """
        Send a message and serve all callbacks that are registers.

        :param message: The message that is being sent. All listeners tied to this message will be called.
        :param kwargs: All the parameters that will be passed to the callback functions.
        """
        messages_sent = 0

        for callback, key in self.subscribers.items():
            if key == message:
                messages_sent = messages_sent + 1
                callback(**kwargs)

        Log.info(f'Sending message to {messages_sent} recipients: {message}')
