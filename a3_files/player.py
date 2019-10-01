from physical_thing import DynamicThing

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"


class Player(DynamicThing):
    """A player in the game"""

    def __init__(self, name: str = "Allan", max_food: float = 20, max_health: float = 20):
        """Constructor

        Parameters:
            name (str): The player's name
            max_food (float): The player's maximum & starting food
            max_health (float): The player's maximum & starting health
        """
        super().__init__(max_health=max_health)

        self._name = name

        self._food = self._max_food = max_food

    def get_name(self):
        """(str)Returns the name of the player"""


    def get_max_food(self):
        """(float) Returns the player's maximum food"""
        return self._max_food

    def get_food(self):
        """(float) Returns the value of the player's food bar"""
        return self._food

    def change_food(self, change: float):
        """Increases the player's food bar by 'change (float)'"""
        self._food += change

        if self._food < 0:
            self._food = 0
        elif self._food > self._max_food:
            self._food = self._max_food

    # The following methods do not require documentation as their purpose is
    # obvious/defined in the super class
    def __repr__(self):
        return f"Player({self._name!r})"

    def use(self):
        pass

    def is_useable(self):
        return False

    def is_mineable(self):
        return False
