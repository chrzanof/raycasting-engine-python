from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, surface):
        pass
