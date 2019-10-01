from physical_thing import DynamicThing
from item import Item

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"


class DroppedItem(DynamicThing):
    """A physical representation of an Item"""

    def __init__(self, item: Item):
        """Constructor

        Parameters:
            item (Item): The conceptual item that this DroppedItem represents physically
        """
        super().__init__()

        self._item = item

    def get_item(self) -> Item:
        """(Item) Returns the conceptual Item this DroppedItem represents"""
        return self._item

    # The following methods do not require documentation as their purpose is
    # obvious/defined in the super class
    def __repr__(self):
        return f"{self.__class__.__name__}({self._item!r})"

    def use(self):
        pass

    def is_useable(self):
        return False

    def is_mineable(self):
        return False


