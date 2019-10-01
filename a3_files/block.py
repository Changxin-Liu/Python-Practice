"""
Classes to represent blocks in the game world, and some useful constants
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

from physical_thing import PhysicalThing

# Mappings of block_id to its break table
# A break table is a mapping of item_ids to (time, correct) pairs, where
#   - time: higher time increases the difficulty to mine (break) a block
#           with the item
#   - correct: is True iff the item is the correct item for breaking the block
#                (usually this indicates whether the block should drop an item
#                 form of itself)
BREAK_TABLES = {
    "dirt": {
        "hand": (.75, True),
        "wood_shovel": (.4, True),
        "stone_shovel": (.2, True),
        "iron_shovel": (.15, True),
        "diamond_shovel": (.1, True),
        "golden_shovel": (.1, True)
    },

    "wood": {
        "hand": (3, True),
        "wood_axe": (1.5, True),
        "stone_axe": (.75, True),
        "iron_axe": (.5, True),
        "diamond_axe": (.4, True),
        "golden_axe": (.25, True)
    },

    "stone": {
        "hand": (7.5, False),
        "wood_pickaxe": (1.15, True),
        "stone_pickaxe": (0.6, True),
        "iron_pickaxe": (0.4, True),
        "diamond_pickaxe": (0.3, True),
        "golden_pickaxe": (0.2, True)
    }
}


class Block(PhysicalThing):
    """One of the building blocks in the sandbox game"""
    # The unique identifier for this block
    _id = None

    _break_table = {
    }

    def __init__(self, hitpoints=20):
        """Constructor

        Parameters:
            hitpoints (float): The maximum & starting hitpoints for this block
        """
        super().__init__()

        self._hitpoints = self._max_hitpoints = hitpoints

        if self._id is None:
            raise NotImplementedError("A Block subclass must define an _id attribute")

        if not self._break_table:
            raise NotImplementedError("A Block subclass must define an _break_table attribute")

    def get_id(self) -> str:
        """(str) Returns the unique id of this block"""
        return self._id

    def get_hitpoints(self) -> float:
        """(float) Returns the block's remaining hitpoints"""
        return self._hitpoints

    def get_position(self):
        """(float, float) Returns the (x, y) position of the block's centre"""
        x, y = self.get_shape().bb.center()
        return x, y

    def is_mineable(self):
        """(bool) Returns True, since blocks are always mineable"""
        return True

    def get_drops(self, luck, correct_item_used):
        """
        Returns the things this block drops

        Parameters:
            luck (float): The player's current luck factor, a random number between [0, 1)
            correct_item_used (bool): Whether the item used to mine was correct (most
                                      often this is taken from the break table)

        Return:
            list<
                tuple<
                    str,
                    tuple<str, ...>
                >
            >: A list of effects dropped by this block. See core.py for more information

        Pre-conditions:
            0 <= luck < 1
        """
        return [('item', (self._id,))]

    def get_damage_by_tool(self, item):
        """(float) Returns the amount of damage caused by a given item (usually a tool)

        Parameters:
            item (Item): The item that would cause the damage
                         (this is usually a tool, but can be any item)
        """
        id_ = item.get_id() if item.get_id() in self._break_table else "hand"

        return self._break_table[id_]


    def mine(self, effective_item, actual_item, luck):
        """Attempts to mine the block
        Mine is synonymous with break, damage, attack

        Parameters:
            effective_item (Item):
                        The item used to calculate damage; this will be the
                        'actual_item' unless it cannot attack, in which case
                        this will most often be the hands.
            actual_item (Item): The actual item causing the damage
            luck (float): The player's current luck factor, a random number between 0 & 1

        Return:
            tuple<bool, bool>:
                A pair of:
                    - correct_item (bool): True iff the effective item is the correct type
                                           to mine this block
                    - is_mined (bool): True iff this block is now completely mined
        """
        time, correct_item = self.get_damage_by_tool(effective_item)

        damage = 10 / time
        self._hitpoints -= damage

        print(f"Did {damage} damage with {effective_item} (correct? {correct_item})")

        return correct_item, self.is_mined()

    def is_mined(self):
        """(bool) Returns True iff this block is completely mined"""
        return self._hitpoints <= 0

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class LeafBlock(Block):
    """Swaying in the breeze, perhaps it hides a tasty surprise"""
    _id = 'leaves'

    _break_table = {
        "hand": (.35, False),
        "shears": (.4, True),
        "sword": (.2, False)
    }

    def can_use(self):
        """(bool) Returns False, since LeafBlocks cannot be used"""
        return False

    def use(self):
        """Does nothing, since LeafBlocks cannot be used"""
        print("Kayn't nobudy use a leaf blahk foo")

    def get_drops(self, luck, correct_item_used):
        """Drops an apple 30% of the time if the wrong tool was used

        See Block.get_drops for parameters & return"""
        if not correct_item_used:
            if luck < 0.3:
                return [('item', ('apple',))]

    def __repr__(self):
        return f"LeafBlock()"


class ResourceBlock(Block):
    """A simple block content with a simple life that drops an
    item form itself when mined"""

    def __init__(self, block_id, break_table):
        """Constructor

        Parameters:
            block_id (str): The unique id of this block
            break_table (dict<str, tuple<float, bool>>):
                    The block's break table; see comment on BREAK_TABLES above
        """
        self._id = block_id
        self._break_table = break_table

        super().__init__()

    def get_drops(self, luck, correct_item_used):
        """Drops a itself in item form 5 times

        See Block.get_drops for parameters & return"""

        if correct_item_used:
            # Drop 5 of itself in item form
            return [('item', (self._id,))] * 5

    # The following methods have not been commented, and their comments
    # are inherited from Block
    def can_use(self):
        return False

    def use(self):
        pass

    def __repr__(self):
        return f"ResourceBlock({self._id!r})"


class TrickCandleFlameBlock(Block):
    """Just when you thought you've blown it out, it comes back again"""

    _id = "mayhem"

    _break_table = {
        "hand": (5, True),
    }

    colours = ['#F47C7C', '#F7F48B', '#70A1D7']

    def __init__(self, stage):
        """Constructor

        Parameters:
            stage (int): The stage of this block (0 <= stage < len(colours))
        """
        super().__init__()
        self._i = stage

    def get_drops(self, luck, correct_item_used):
        """Drops the next stage of itself (block form)

        See Block.get_drops for parameters & return"""
        return [('block', ('mayhem', (self._i + 1) % len(self.colours)))]

    # The following methods have not been commented, and their comments
    # are inherited from Block
    def use(self):
        pass

    def __repr__(self):
        return f"TrickCandleFlameBlock({self._i!r})"
