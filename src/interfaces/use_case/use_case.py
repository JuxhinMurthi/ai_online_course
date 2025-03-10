from abc import ABC, abstractmethod


class UseCasePort(ABC):
    """ Use case port interface. """

    @abstractmethod
    def execute(self, *arg, **kwargs):
        """ Execute use case. """