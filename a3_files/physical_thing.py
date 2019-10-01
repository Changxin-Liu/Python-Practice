"""
High-level abstract classes to represent physical things in the game world
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

import pymunk

from typing import Tuple, List
from core import EffectID


class PhysicalThing:
    """The highest-level abstract representation of a physical thing in the game world

    Should not be instantiated directly"""

    def __init__(self):
        self._shape: pymunk.Shape = None

    def is_mineable(self) -> bool:
        """(bool) Returns True iff this thing is able to be mined"""
        raise NotImplementedError("A PhysicalThing subclass must implement an is_mineable method")

    def is_useable(self) -> bool:
        """(bool) Returns True iff this thing is able to be used"""
        raise NotImplementedError("A PhysicalThing subclass must implement an is_useable method")

    def use(self) -> List[EffectID]:
        """Uses this thing

        Return:
            list<tuple<str, tuple>>:
                    Returns a list of effects; each effect is a pair of (type, sub_id), where
                    type is a str, and sub_id is a tuple uniquely identifying this effect within
                    its effect type (usually sub_id comprises of strings, but not necessarily)

                    See core.py for more information
        """
        raise NotImplementedError("A PhysicalThing subclass must implement a use method")

    def set_shape(self, shape: pymunk.Shape):
        self._shape = shape

    def get_shape(self) -> pymunk.Shape:
        return self._shape

    def get_position(self) -> Tuple[float, float]:
        """(tuple<float, float>) Returns the (x, y) position of this thing in the world"""
        position = self._shape.body.position
        return position.x, position.y

    def step(self, time_delta: float, game_data):
        """Advance this thing by one time-step

        Parameters:
            time_delta (float): The amount of time that has passed since the last step, in seconds
            game_data (app.GameData): Arbitrary data supplied by the app class
        """

    def __repr__(self):
        raise NotImplementedError("A PhysicalThing subclass must implement a __repr__ method")


class DynamicThing(PhysicalThing):
    """A physical thing that can move

    Should not be instantiated directly"""

    def __init__(self, max_health=20):

        super().__init__()

        self._health = self._max_health = max_health

    def get_max_health(self):
        """(float) Returns the dynamic thing's maximum health"""
        return self._max_health

    def change_health(self, change):
        """Increases the dynamic thing's health by 'change (float)'"""
        self._health += change

        if self._health < 0:
            self._health = 0
        elif self._health > self._max_health:
            self._health = self._max_health

    def get_health(self):
        """(float) Returns the dynamic thing's health"""
        return self._health

    def is_dead(self):
        """(bool) Returns True iff this thing is dead"""
        return self._health <= 0

    def is_mineable(self):
        """(bool) Returns False, since dynamic thing's can't be mined"""
        return False

    def get_velocity(self):
        """Returns the velocity of this dynamic thing

        Return:
            tuple<float, float>: The (x, y) components of the velocity
        """
        return self.get_shape().body.velocity

    def set_velocity(self, velocity: Tuple[float, float]):
        """Sets the velocity of this dynamic thing to 'velocity'

        Parameters:
            velocity (tuple<float, float>):
                    The (x, y) components of the new velocity
        """
        self.get_shape().body.velocity = velocity


class BoundaryWall(PhysicalThing):
    """A boundary wall to prevent movement off the edge of the game world"""

    def __init__(self, wall_id: str):
        """Constructor

        Parameters:
            wall_id (str): The unique id of this wall (e.g. 'left', 'top', etc.)
        """
        super().__init__()

        self._id = wall_id

    def get_id(self) -> str:
        """(str) Returns the unique id of this wall"""
        return self._id

    def is_mineable(self) -> bool:
        """(bool) Returns False, since walls cannot be mined"""
        return False

    def is_useable(self) -> bool:
        """(bool) Returns False, since walls cannot be used"""
        return False

    def use(self):
        pass

    def get_position(self) -> Tuple[float, float]:
        """(tuple<float, float>) Returns the position of the centre of this wall"""
        x, y = self.get_shape().bb.center()
        return x, y

    def __repr__(self):
        return f"BoundaryWall({self._id!r})"
