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
        self.listeners: Dict[(Event, Any), List[Callable]] = {}

    def subscribe(self, event_type: Hashable, listener: Any, ) -> None:
        """
        The listener will subscribe to events and be notified in the future when those events are triggered.

        :param event_type: The event that is being listened to
        :param listener: The class that is looking to be notified by a subscription event
        """

        if event_type not in self.listeners:
            self.listeners[event_type] = []

        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener) -> None:
        """
        Unsubscribe the listener from this particular event.

        :param event_type: The event that the listener wants to be removed from
        :param listener: The listener that wants to be removed from this subscription
        """
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
