"""
Classes to represent mobs in the game world, and some useful constants
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"


import random
import cmath

from physical_thing import DynamicThing

MOB_DEFAULT_TEMPO = 40

BIRD_GRAVITY_FACTOR = 150
BIRD_X_SCALE = 1.61803


class Mob(DynamicThing):
    """An abstract representation of a creature in the sandbox game

    Can be friend, foe, or neither

    Should not be instantiated directly"""

    def __init__(self, mob_id, size, tempo=MOB_DEFAULT_TEMPO, max_health=20):
        """Constructor

        Parameters:
            mob_id (str): A unique id for this type of mob
            size (tuple<float, float>):
                    The physical (x, y) size of this mob
            tempo (float):
                    The movement tempo of this mob:
                      - zero indicates no movement
                      - further from zero means faster movement
                      - negative is reversed
            max_health (float): The maximum & starting health for this mob
        """
        super().__init__(max_health=max_health)

        self._id = mob_id
        self._size = size
        self._tempo = tempo

        self._steps = 0

    def get_id(self):
        """(str) Returns the unique id for this type of mob"""
        return self._id

    def get_size(self):
        """(str) Returns the physical (x, y) size of this mob"""
        return self._size

    def step(self, time_delta, game_data):
        """Advance this mob by one time step

        See PhysicalThing.step for parameters & return"""
        # Track time via time_delta would be more precise, but a step counter is simpler
        # and works reasonably well, assuming time steps occur at roughly constant time deltas
        self._steps += 1

    def __repr__(self):
        return f"{self.__class__.__name__}({self._id!r})"


class Bird(Mob):
    """A friendly bird, nonchalant with a dash of cheerfulness"""

    def step(self, time_delta, game_data):
        """Advance this bird by one time step

        See PhysicalThing.step for parameters & return"""
        # Every 20 steps; could track time_delta instead to be more precise
        if self._steps % 20 == 0:
            # a random point on a movement circle (radius=tempo), scaled by the percentage
            # of health remaining
            health_percentage = self._health / self._max_health
            z = cmath.rect(self._tempo * health_percentage, random.uniform(0, 2 * cmath.pi))

            # stretch that random point onto an ellipse that is wider on the x-axis
            dx, dy = z.real * BIRD_X_SCALE, z.imag

            x, y = self.get_velocity()
            velocity = x + dx, y + dy - BIRD_GRAVITY_FACTOR

            self.set_velocity(velocity)

        super().step(time_delta, game_data)

    def use(self):
        pass
