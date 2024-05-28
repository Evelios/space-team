"""
Event manager class handling (un)subscriptions and event calls for all events.

Notes: https://refactoring.guru/design-patterns/observer
"""

from typing import Dict, Any, Hashable, Callable, List
from enum import Enum


class Event(Enum):
    """
    Inheritable class for any event that is going to be added to the event manager.
    """


class EventManager:

    def __init__(self):
        """ Initialize the event manager. """

        """ All listeners to all events. """
        self.listeners: Dict[(Event, Any), Callable] = {}

    def subscribe(self, event_type: Hashable, listener: Any, callback: Callable) -> None:
        """
        The listener will subscribe to events and be notified in the future when those events are triggered.

        :param event_type: The event that is being listened to.
        :param listener: The class that is looking to be notified by a subscription event.
        :param callback: The callback that will be run when an event is triggered.
        """
        self.listeners[event_type, listener] = callback

    def unsubscribe(self, event_type: Hashable, listener: Any) -> None:
        """
        Unsubscribe the listener from this particular event.

        :param event_type: The event that the listener wants to be removed from.
        :param listener: The listener that wants to be removed from this subscription.
        """
        self.listeners.pop(event_type, listener)

    def notify(self, event: Hashable, data: Any) -> None:
        """
        Notify all subscribed listeners of a particular event. This triggers all the callable functions that were
        subscribed to be run based off the event happening.

        :param event: The event that was triggered.
        :param data: The data that is sent to the callable.
        """
        for (event_type, listener) in self.listeners:
            if event_type == event:
                self.listeners[event_type, listener](data)
