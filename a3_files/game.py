"""
View classes for the sandbox game
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
from typing import Iterable

from instance_router import InstanceRouter
from physical_thing import PhysicalThing
from block import Block, TrickCandleFlameBlock
from dropped_item import DroppedItem
from player import Player
from physical_thing import BoundaryWall
from mob import Mob, Bird


class GameView(tk.Canvas):
    """A view class for the sandbox game, with convenience methods to draw various parts of the UI"""

    def __init__(self, master, size, physical_view_router: InstanceRouter):
        """Constructor

        Parameters:
            master (tk.Tk | tk.Toplevel | tk.Frame): The tkinter master widget
            size (tuple<int, int>): The (width, height) size of the view, in pixels
            physical_view_router (InstanceRouter):
                    View router that facilitates drawing of physical items through
                    calling route_and_call method with:
                        (physical thing, physical thing's shape, self (canvas))
        """
        width, height = size
        super().__init__(master, width=width, height=height)

        self._world_view_router = physical_view_router

    def show_target(self, player_position, target_position, cursor_position=None,
                    target_radius=14, target_thickness=2, crosshair_radius=4,
                    target_colour='purple', cursor_bg_colour='grey', cursor_fg_colour='white'):
        """Shows the target & cursor on screen

        A target outline will be drawn around 'target_position', with the centre of this
        outline exactly 'target_radius' away from 'target_position', and a thickness of
        'target_thickness' on each side.

        The cursor consists of a line and a crosshair. The line will be drawn from
        'player_position' to 'cursor_position'. A crosshair will be drawn at
        'cursor_position', with a radius of 'crosshair_radius'.

        If 'cursor_position' is None, it will default to 'target_position'.

        Parameters:
            player_position (tuple<int, int>): The position of the player
            target_position (tuple<int, int>): The position of the target cell (i.e. the centre of the block)
            cursor_position (tuple<int, int> | None): The position of the cursor crosshair, or None if this should be
                                                      the same as target_position
            target_radius (int): The radius from the target position to the centre of the target outline
            target_thickness (int): The thickness of the target outline
            crosshair_radius (int): The radius of the cursor crosshair
            target_colour (str): The colour of the target outline
            cursor_bg_colour (str): The background colour of the cursor crosshair & line
            cursor_fg_colour (str): The foreground colour of the cursor crosshair & line
        """
        x, y = target_position

        if cursor_position is None:
            cx, cy = target_position
        else:
            cx, cy = cursor_position

        coords = x - target_radius, y - target_radius, x + target_radius, y + target_radius
        self.create_rectangle(coords, fill='', width=target_thickness * 2, outline=target_colour,
                              tag=('block', 'target'))

        if cursor_bg_colour:
            self.create_line(player_position, (cx, cy), fill=cursor_bg_colour, tag='cursor', width=3)

        if cursor_fg_colour:
            self.create_line(player_position, (cx, cy), fill=cursor_fg_colour, tag='cursor')

        horizontal = (cx - crosshair_radius, cy), (cx + crosshair_radius, cy)
        vertical = (cx, cy - crosshair_radius), (cx, cy + crosshair_radius)

        if cursor_bg_colour:
            self.create_line(horizontal, fill=cursor_bg_colour, tag='cursor', width=3)
            self.create_line(vertical, fill=cursor_bg_colour, tag='cursor', width=3)

        if cursor_fg_colour:
            self.create_line(horizontal, fill=cursor_fg_colour, tag='cursor')
            self.create_line(vertical, fill=cursor_fg_colour, tag='cursor')

    def hide_target(self):
        """Removes the target & cursor from the screen"""
        self.delete('cursor', 'target')

    def draw_physical(self, things: Iterable[PhysicalThing]):
        """Draws all physical things, according to their draw method (on the view router)

        Parameters:
            things (iterable<PhysicalThing>): The physical things to draw.
        """
        for thing in things:
            shape = thing.get_shape()

            # QUERY: cache these?
            items = self._world_view_router.route_and_call(thing, shape, self)


class WorldViewRouter(InstanceRouter):
    """
    Magical (sub)class used to facilitate drawing of different physical things on a canvas

    For a large system, separate classes could be used for each thing,
    but for simplicity's sake, we've opted to use a single class with
    multiple similar methods
    """

    def __init__(self, block_colours, item_colours, player_colour='red'):
        """
        Constructor

        Parameters:
             block_colours (dict<str: str>): A mapping of block ids to their respective colours
             item_colours (dict<str: str>): A mapping of item ids to their respective colours
        """
        super().__init__()

        self._block_colours = block_colours
        self._item_colours = item_colours
        self._player_colour = player_colour

    # Instances of class, or its subclasses are drawn by method
    # I.e. _draw_block handles the drawing of Block & its subclasses
    # More specific subclasses take priority, so _draw_mayhem block will handle the drawing of TrickCandleFlameBlock
    _routing_table = [
        # (class, method name)
        (Block, '_draw_block'),
        (TrickCandleFlameBlock, '_draw_mayhem_block'),
        (DroppedItem, '_draw_physical_item'),
        (Player, '_draw_player'),
        (Bird, '_draw_bird'),
        (BoundaryWall, '_draw_undefined'),
        (None.__class__, '_draw_undefined')
    ]

    # All methods follow the following signature:
    #   instance (PhysicalThing): The physical thing to draw
    #   shape (pymunk.Shape): The physical thing's shape in the world
    #   view (tk.Canvas): The canvas on which to draw the thing
    def _draw_block(self, instance, shape, view):
        return [view.create_rectangle(shape.bb.left, shape.bb.top, shape.bb.right, shape.bb.bottom,
                                      fill=self._block_colours[instance.get_id()], tags='block')]

    def _draw_mayhem_block(self, instance, shape, view):
        return [view.create_rectangle(shape.bb.left, shape.bb.top, shape.bb.right, shape.bb.bottom,
                                      fill=instance.colours[instance._i], tags='block')]

    def _draw_physical_item(self, instance, shape, view):
        return [view.create_rectangle(shape.bb.left, shape.bb.top, shape.bb.right, shape.bb.bottom,
                                      fill=self._item_colours[instance.get_item().get_id()],
                                      tags='physical_item')]

    def _draw_player(self, instance, shape, view):
        return [view.create_oval(shape.bb.left, shape.bb.top, shape.bb.right, shape.bb.bottom,
                                 fill=self._player_colour, tags='player')]

    def _draw_bird(self, instance, shape, view):
        # Man I wish there were object destructuring in python
        bb = shape.bb

        centre_x = (bb.left + bb.right) // 2
        centre_y = (bb.top + bb.bottom) // 2

        return [
            view.create_polygon((centre_x, bb.top), (bb.right, centre_y), (centre_x, bb.bottom), (bb.left, centre_y),
                                fill='#87CEEB', tags=('mob', 'bird'))]

    def _draw_undefined(self, instance, shape, view):
        return [view.create_rectangle(shape.bb.left, shape.bb.top, shape.bb.right, shape.bb.bottom,
                                      fill='black', tag='undefined')]



