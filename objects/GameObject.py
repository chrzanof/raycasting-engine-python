from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    abstract class for every object (entity) in a game.
    Implemented according to Update Method design pattern
    """
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, canvas):
        pass
