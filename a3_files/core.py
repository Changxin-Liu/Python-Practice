"""
Some core mechanisms & miscellany for the sandbox game
"""

from typing import Tuple

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

# Typically, one would use the enum type to represent a set of possible values, but
# to make it easier for students we've opted to instead use simple strings

# An EffectType is the type of effect produced by something (a unique string)
# An EffectSubID is the unique identifier for an effect of a particular type (a unique tuple of strings)
# An EffectID is pair of (EffectType, EffectSubID)
# Note: EffectType determines the range of possible EffectSubIDs
#
# For example, with the EffectID: ('item', ('pickaxe', 'wood')),
#   - the EffectType is 'item'
#   - the EffectSubID is ('pickaxe', 'wood'), which uniquely identifies the effect when paired with the EffectType
#
# Similarly, with the EffectID: ('block', ('dirt',)),
#   - the EffectType is 'block'
#   - the EffectSubID is ('dirt', ), which uniquely identifies the effect when paired with the EffectType
#       (note that ('dirt', ) is a one-tuple)

EffectSubID = Tuple[str, ...]
EffectType = str
EffectID = Tuple[EffectType, EffectSubID]


TK_MOUSE_EVENTS = {
    "<Button-1>",
    "<ButtonPress-1>",
    "<1>",
    "<B1-Motion>",
    "<ButtonRelease-1>",
    "<Double-Button-1>",
    "<Button-2>",
    "<ButtonPress-2>",
    "<2>",
    "<B2-Motion>",
    "<ButtonRelease-2>",
    "<Double-Button-2>",
    "<Button-3>",
    "<ButtonPress-3>",
    "<3>",
    "<B3-Motion>",
    "<ButtonRelease-3>",
    "<Double-Button-3>",
}

# Bitmasks for modifier keys in tkinter mouse event's state
MODIFIER_KEYS = {
    2 ** 0: 'shift',
    2 ** 2: 'ctrl',
}


def get_modifiers(state):
    """Gets the modifier keys stored in state

    Parameters:
        state (int): State from tkinter.MouseEvent.state

    Return:
        set<str>: A subset of the values of MODIFIER_KEYS
    """
    return {modifier for mask, modifier in MODIFIER_KEYS.items() if state & mask}


def euclidean_square_distance(position1: (float, float), position2: (float, float)):
    """(tuple<float, float>) Returns the euclidean (straight-line) distance between 'position1' & 'position2'

    Parameters:
        position1 (tuple<float, float>): The first point
        position2 (tuple<float, float>): The second point
    """
    x1, y1 = position1
    x2, y2 = position2

    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def positions_in_range(position1, position2, max_distance):
    """(bool) Returns True iff position1 & position2 are within 'max_distance' from each other, in terms
    of euclidean distance

    Parameters:
        position1 (tuple<float, float>): The first point
        position2 (tuple<float, float>): The second point
        max_distance (float): The maximum distance between position1 & position2
    """
    return euclidean_square_distance(position1, position2) <= max_distance ** 2