"""Routes instances to specific methods for classes & their subclasses

Primarily used to concisely define individual methods (i.e. functions) for drawing physical things in the SandboxGame.

Ideally, there would be a view class for each individual thing (each item, each block, each creature, etc.), inheriting
from a super class (i.e. AbstractView) with a more complicated file structure. However, for simplicity's
sake, this has been avoided in favour of a single view class with methods for each kind of unit.

If you wish to add additional types of visuals for units, simply inherit from the appropriate class
and set the corresponding keyword argument in view.GameView
"""

__author__ = "Benjamin Martin"
__copyright__ = "Copyright 2019, The University of Queensland"
__license__ = "MIT"
__version__ = "1.0.0"

#
#                         /-------------\
#                        /               \
#                       /                 \
#                      /                   \
#                      |   XXXX     XXXX   |
#                      |   XXXX     XXXX   |
#                      |   XXX       XXX   |
#                      \         X         /
#                       --\     XXX     /--
#                        | |    XXX    | |
#                        | |           | |
#                        | I I I I I I I |
#                        |  I I I I I I  |
#                         \              /
#                           --         --
#                             \-------/
#                     XXX                    XXX
#                   XXXXX                  XXXXX
#                   XXXXXXXXX         XXXXXXXXXX
#                           XXXXX   XXXXX
#                             XXXXXXX
#                           XXXXX   XXXXX
#                   XXXXXXXXX         XXXXXXXXXX
#                   XXXXX                  XXXXX
#                     XXX                    XXX
#                           **************
#                           *  BEWARE!!  *
#                           **************
#                       All ye who enter here:
#                  Most of the code in this module
#                      is twisted beyond belief!
#                         Tread carefully
#                  If you think you understand it,
#                             You Don't,
#                           So Look Again
#

import math
import tkinter as tk


class InstanceRouter:
    """
    Routes an instance to a call to the specific method intended to handle it. More specific classes take priority (i.e.
    a child class takes precedence over its parent(s))

    _routing_table is a list of (class, method name) pairs; e.g. (literal order doesn't matter - more specific classes
    take precedence over parents)
    [
        (Block, '_draw_block'),
        (Creature, '_draw_creature'),
        (Sheep, '_draw_sheep'),
        (PhysicalItem, '_draw_physical_item')
    ]

    Assumes no inheritance relationship, except that Sheep inherits from Creature, routing would occur as follows:
      - Any instance of Block, or its subclasses, will be handled by the _draw_block method
      - Any instance of Creature, or its subclasses, except Sheep, will be handled by the _draw_creature method
      - Any instance of PhysicalItem, or its subclasses, will be handled by the _draw_physical_item method
      - Any instance of Sheep, or its subclasses, will be handled by the _draw_sheep method

    Reordering this literal list would not affect the above definition.

    Without the line `(Sheep, '_draw_sheep')`, _draw_creature would also handle Sheep and its subclasses.
    """
    _routing_table = []

    def __init__(self):
        self._route_cache = {}

        if not self._routing_table:
            raise AttributeError("ViewRouter subclass must define _route_table, as per comment in this file")

        # Sorts routing table by number of classes in inheritance tree, in descending order
        # => Children will precede parents
        self._routing_table = sorted(self._routing_table, key=lambda i: len(i[0].mro()), reverse=True)

    def _get_method(self, key):
        #print(f'getting method for {key}')
        for class_, method in self._routing_table:
            #print(f' => {class_}')

            if issubclass(key, class_):
                return getattr(self, method)

        raise NotImplementedError(f"No method for {class_} (or any of its parents)")

    def route_and_call(self, instance, *args, **kwargs):
        if instance.__class__ not in self._route_cache:
            self._route_cache[instance.__class__] = self._get_method(instance.__class__)

        return self._route_cache[instance.__class__](instance, *args, **kwargs)