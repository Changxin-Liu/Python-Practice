"""
Classes to represent abstract (conceptual, non-physical) items in the game.

Note that abstract here refers to something not existing physically in the game
world, not abstract in the object-oriented sense
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

from core import EffectID


class Item:
    """A conceptual, non-physical item in the game"""

    def __init__(self, id_: str, max_stack: int = 64, attack_range: float = 10):
        """Constructor

        Parameters:
            id_ (str): The unique id of this item
            max_stack (int): The maximum stack size of this item
            attack_range (float): The item's range when attacking, in block spans
        """
        self._id = id_
        self._max_stack_size = max_stack
        self._range = attack_range

    def get_id(self) -> str:
        """(str) Returns the unique id of this item"""
        return self._id

    def __repr__(self):
        return f"{self.__class__.__name__}({self._id!r})"

    def can_attack(self):
        raise NotImplementedError("An Item subclass must implement a can_attack method")

    def attack(self, successful) -> EffectID:
        """Records an attack against a thing in the world

        Return:
            [tuple<str, tuple<str, ...>>]:
                    A list of EffectIDs resulting from the attack. Each EffectID is a pair
                    of (effect_type, effect_sub_id) pair, where:
                      - effect_type is the type of the effect ('item', 'block', etc.)
                      - effect_sub_id is the unique identifier for an effect of a particular type
        """
        raise NotImplementedError("An Item subclass must implement an attack method")

    def place(self) -> EffectID:
        """Places the item into the world

        Return:
            [tuple<str, tuple<str, ...>>]:
                    A list of EffectIDs resulting from placing this item. Each EffectID is a pair
                    of (effect_type, effect_sub_id) pair, where:
                      - effect_type is the type of the effect ('item', 'block', etc.)
                      - effect_sub_id is the unique identifier for an effect of a particular type
        """
        raise NotImplementedError("An Item subclass must implement a place method")

    def get_max_stack_size(self):
        """(int) Returns the maximum stack size of this item in the inventory/hotbar

        Unstackable items must have a stack size of 1, whereas stackable items typically have a stack
        size of 64 (but not always)"""
        return self._max_stack_size

    def is_stackable(self) -> bool:
        """(bool) Returns True iff this item is stackable in the inventory/hotbar"""
        return self._max_stack_size != 1

    def get_attack_range(self) -> float:
        """(float) Returns the basic range at which this item's attack can reach, in block spans"""
        return self._range

    def get_durability(self):
        """(float) Returns the item's durability (effectively its health). For items that cannot
        attack, this value is irrelevant"""
        raise NotImplementedError("An Item subclass must implement a get_durability method")

    def get_max_durability(self):
        """(float) Returns the item's maximum durability"""
        raise NotImplementedError("An Item subclass must implement a get_max_durability method")


class HandItem(Item):
    """The player's hands, infinitely durable and the item used to attack by default"""

    def __init__(self, id_):
        super().__init__(id_, max_stack=1)

    # The following methods have not been documented, as their purpose is simple
    # and their docstrings are inherited from Item's methods
    def get_durability(self):
        return float("inf")

    def get_max_durability(self):
        return float("inf")

    def can_attack(self):
        return True

    def place(self):
        pass

    def attack(self, successful):
        pass


class SimpleItem(Item):
    """An item that drops a Block form of itself when used"""

    # The following methods have not been documented, as their purpose is simple
    # and their docstrings are inherited from Item's methods
    def can_attack(self) -> bool:
        return False

    def place(self):
        pass

    def get_durability(self):
        pass

    def get_max_durability(self):
        pass

    def attack(self, successful):
        pass


class BlockItem(Item):
    """An item that drops a Block form of itself when used"""

    def can_attack(self) -> bool:
        """(bool) Returns False, since BlockItems cannot be used to attack"""
        return False

    def place(self):
        """Places the item into the world in its block form

        Return:
            [tuple<str, tuple<str, ...>>]:
                    A list of EffectIDs resulting from placing this item. Each EffectID is a pair
                    of (effect_type, effect_sub_id) pair, where:
                      - effect_type is the type of the effect ('item', 'block', etc.)
                      - effect_sub_id is the unique identifier for an effect of a particular type
        """

        return [('block', (self._id,))]

    # The following methods have not been documented, as their purpose is simple
    # and their docstrings are inherited from Item's methods
    def get_durability(self):
        pass

    def get_max_durability(self):
        pass

    def attack(self, successful):
        pass


# Default mapping of resource to durability for tools crafted from a given resource
TOOL_DURABILITIES = {
    "wood": 60,
    "stone": 132,
    "iron": 251,
    "gold": 33,
    "diamond": 1562
}

# Types of tools that can be made from a resource (material)
MATERIAL_TOOL_TYPES = {"axe", "shovel", "hoe", "pickaxe", "sword"}
