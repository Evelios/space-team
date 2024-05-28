from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    # Needed to be nested into the Observer class to prevent cyclic dependencies
    from .subject import Subject

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass
