from abc import ABC
from typing import NoReturn


class GameObject(metaclass=ABC):
    def get_name(self):
        pass


class Displayable(GameObject, metaclass=ABC):
    def get_position(self):
        pass

    def update(self, graphics: Graphics) -> NoReturn:
        pass


class Collidable(Displayable, metaclass=ABC):
    def collide_with(self, other: Collidable) -> bool:
        pass


class Effect(GameObject, metaclass=ABC):
    def activate(self) -> NoReturn:
        pass


class Player(Collidable):
    def get_name(self):
        pass

    def collide_with(self, other: Collidable) -> bool:
        pass

    def get_position(self):
        pass

    def update(self, graphics: Graphics) -> NoReturn:
        pass


class Monster(Collidable):
    def get_name(self):
        pass

    def collide_with(self, other: Collidable) -> bool:
        pass

    def get_position(self):
        pass

    def update(self, graphics: Graphics) -> NoReturn:
        pass


class Sound(Effect):
    def get_name(self):
        pass

    def activate(self) -> NoReturn:
        pass


class Explosion(Displayable, Effect):
    def get_name(self):
        pass

    def get_position(self):
        pass

    def update(self, graphics: Graphics) -> NoReturn:
        pass

    def activate(self) -> NoReturn:
        pass
