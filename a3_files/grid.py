"""
Classes to manage modelling & displaying the hotbar & inventory
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
from typing import Tuple, Generator
import json

from core import TK_MOUSE_EVENTS
from item import Item


class Stack(object):
    """Stacks are used to store Items with a stack quantity. Stacks appear in the inventory (and
    similar) as to combine items of the same size up to a maximum limit defined by the Item"""

    def __init__(self, item: Item, quantity: int):
        """Constructor of Stack

        Parameters:
            item (Item): Item this Stack will contain
            quantity (int): Stack size

        Pre-condition:
            0 < quantity <= item.get_max_stack_size()"""

        assert 0 <= quantity <= item.get_max_stack_size(), \
            (f"Stack creation attempted with quantity of {quantity} for Item {item.get_id()!r} "
             f"that has a maximum stack size of {item.get_max_stack_size()}")

        self._item = item
        self._quantity = quantity

    def copy(self):
        """(Stack) Returns a copy of this stack"""
        return self.__class__(self.get_item(), self.get_quantity())

    def matches(self, other: "Stack"):
        """(bool) Returns True iff other contains the same item as this stack"""
        return self._item.get_id() == other._item.get_id()

    def absorb(self, other: "Stack", maximum=None):
        """Absorbs another stack into this stack, as much as possible (stops when either other is
        depleted or this is full).
        No action if Stacks are of different types.

        Parameters:
            other (Stack): stack to absorb

        Return (bool): True iff the other stack was fully absorbed by this one"""

        if other.get_item().get_id() == self.get_item().get_id():
            if maximum is None:
                quantity = other.get_quantity()
            else:
                quantity = maximum
            other.subtract(self.add(quantity))
            if other._quantity <= 0:
                return True
        return False

    def split(self, count=None):
        """Split this stack quantity in two and return the new Stack. The quantity of the new Stack
        and updated self is equal to the original Stack size.


        Parameters:
            count (int): The number to split off, defaults to half the stack size (rounded down)

        return (Stack): new Stack with half the size of the original"""

        if count is None:
            count = self.get_quantity() // 2
        else:
            count = min(self.get_quantity(), count)

        new = self.__class__(self.get_item(), count)
        self.subtract(new.get_quantity())
        return new

    def add(self, quantity: int) -> int:
        """Add to this stack without needing to worry about overflow.

        Parameter:
            quantity (int): Quantity of item to be added to this stack
        return (int): amount added to this stack"""

        to_add = min(self._quantity + quantity, self._item.get_max_stack_size()) - self._quantity
        self._quantity += to_add
        return to_add

    def subtract(self, quantity: int) -> int:
        """Remove quantity from stack. If stack size is smaller than quantity being subtracted,
        quantity will be set to 0.

        Parameters:
            quantity (int): quantity to remove if possible

        Return (int): positive amount remaining after subtracting to maintain a non-negative Stack
        size"""

        remainder = self._quantity - quantity
        self._quantity = max(0, remainder)
        return abs(remainder) if remainder > 0 else 0

    def decrement(self):
        """Decrement Stack by one

        Return:
             bool: True iff stack becomes depleted"""

        self.subtract(1)
        return bool(self._quantity)

    def get_item(self) -> Item:
        """(Item) Returns the item held in this stack"""
        return self._item

    def get_quantity(self) -> int:
        """(int) Returns the quantity of items in this stack"""
        return self._quantity

    def is_empty(self):
        """(bool) Returns True iff this stack is empty"""
        return self._quantity == 0

    def get_space(self):
        """(int) Returns number of items this stack is short of being full"""
        return self._item.get_max_stack_size() - self._quantity

    def __len__(self):
        """(int) Returns the quantity of items in this stack"""
        return self._quantity

    def __repr__(self):
        return "Stack(" + self._item.get_id() + ", " + str(self._quantity) + ")"


class ItemGridView(tk.Canvas):
    """Class defining constants and draw methods for rendering item orientated views. The methods
    in in this class allow for a grid view of items to be easily drawn and be added to the master
    view given.

    This class is intended to be extended upon when defining specific item view contexts."""

    BORDER = 100  # BORDER//2 + |item grid| + BORDER//2
    CELL_LENGTH = 64  # pixel width of grid cell
    CELL_SPACING = 5  # pixel spacing between grid cells

    CONTENT_GAP = CELL_LENGTH // 20  # gap between cell outside border and where to render contents

    def __init__(self, master, size,
                 deselected_colour='#e6e8ed',
                 selected_colour='#6CB2D1',
                 major_font=("Arial", 14),
                 minor_font=("Arial", 10),
                 **kwargs):
        """Constructor for item based views.

        Parameters:
            master: Container to add this view to
            size (tuple<int, int>): Number of (rows, columns) for the grid
            kwargs: kwargs (key word arguments) to be given to the tk.Canvas on creation
        """

        self._major_font = major_font
        self._minor_font = minor_font

        rows, columns = size

        height = rows * (self.CELL_LENGTH + self.CELL_SPACING) + self.BORDER
        width = columns * (self.CELL_LENGTH + self.CELL_SPACING) + self.BORDER

        super().__init__(master, width=width, height=height, **kwargs)

        self._selected_colour = selected_colour
        self._deselected_colour = deselected_colour

        self._slots = Grid(rows=rows, columns=columns)

        for key in self._slots:
            self._slots[key] = self.create_oval(self.grid_to_xy_centre(key), self.grid_to_xy_centre(key))

    def grid_to_xy_box(self, grid_position):
        """Returns the coordinates of the bounding box of the cell at 'grid_position'

        Parameters:
            grid_position (tuple<int, int>): Cell's (row, column) grid position

        Return:
            (tuple<float, float, float, float>):
                    The (left, top, right, bottom) coordinates of the bounding box
        """
        row, column = grid_position

        x0 = self.BORDER // 2 + (self.CELL_LENGTH + self.CELL_SPACING) * column
        y0 = self.BORDER // 2 + (self.CELL_LENGTH + self.CELL_SPACING) * row

        x1 = x0 + self.CELL_LENGTH
        y1 = y0 + self.CELL_LENGTH

        return x0, y0, x1, y1

    def grid_to_xy_centre(self, grid_position):
        """Returns the coordinates of the centre of the cell at 'grid_position'

        Parameters:
            grid_position (tuple<int, int>): Cell's (row, column) grid position

        Return:
            (tuple<float, float>): The (x, y) coordinates of the centre
        """
        x0, y0, x1, y1 = self.grid_to_xy_box(grid_position)

        return (x0 + x1) // 2, (y0 + y1) // 2

    def xy_to_grid(self, xy_position):
        """Returns the grid position of the cell that contains the 'xy_position'

        Parameters:
            xy_position (tuple<float, float>):
                    (x, y) coordinates contained by some cell

        Return:
            (tuple<int, int>): The (row, column) grid position of the cell
        """
        x, y = xy_position

        column = (x - self.BORDER // 2) // (self.CELL_LENGTH + self.CELL_SPACING)
        row = (y - self.BORDER // 2) // (self.CELL_LENGTH + self.CELL_SPACING)

        return row, column

    def draw_cell(self, grid_position, stack, active=False):
        """Draws a stack in a cell

        Parameters:
            grid_position (tuple<int, int>):
                    The (row, column) position of the cell to draw on
            stack (Stack): The stack to draw, or None for empty
            active (bool): Whether the cell is active or not
        """
        box = self.grid_to_xy_box(grid_position)

        text = stack.get_item().get_id().replace('_', '\n') if stack else ""

        colour = self._selected_colour if active else self._deselected_colour

        centre = self.grid_to_xy_centre(grid_position)
        left, top, right, bottom = self.grid_to_xy_box(grid_position)

        self.create_rectangle(box, fill=colour, tag='cell')

        if stack:
            item = stack.get_item()

            self.create_text(centre, text=text, font=self._major_font, tag='cell')

            if item.is_stackable():
                sub_text = f"{len(stack)}"
                x = right
                anchor = tk.SE
            else:
                sub_text = f"{item.get_durability()}/{item.get_max_durability()}"
                x = left
                anchor = tk.SW

            self.create_text(x, bottom, text=sub_text, anchor=anchor, font=self._minor_font, tag='cell')

    def bind_for_id(self, event, callback):
        """Binds to tkinter mouse event and also provides position of
        cell where event was triggered to callback

        Callback is called similarly to callbacks to tk.bind, except grid_position of
        relevant cell is also inserted:
            tk_callback(mouse_event)
            =>
            callback(grid_position, mouse_event),
                where 'grid_position' is the (row, column) position of the cell where
                the event was triggered

        Parameters:
             event (str): The tkinter mouse event to bind to
             callback (function): The callback to bind
        """
        if event not in TK_MOUSE_EVENTS:
            return

        self.bind(event, lambda e: callback(self.xy_to_grid((e.x, e.y)), e))

    def render(self, items, active_position):
        """Re-render the Hot Bar

        Parameters:
            items list<Stack>: items to be displayed in Hot Bar
            active_position (int): id of currently active cell
        """
        self.delete(tk.ALL)
        for position, stack in items:
            self.draw_cell(position, stack, position == active_position)


class Grid:
    """A 2d grid to hold items"""

    def __init__(self, rows=4, columns=5):
        self._items = [
            [
                None for j in range(columns)
            ] for i in range(rows)
        ]

    def __repr__(self):
        return json.dumps([[repr(stack) for stack in row] for row in self._items], indent=4)

    def get_crafting_pattern(self):
        """Returns the crafting pattern that this grid forms

        Return:
            tuple<
                tuple<
                    str:
                    ...
                >,
                ...
            >: A 2d-tuple that matches the dimensions of this grid, with each inner element being
               the item id of the stack, else None if there is no stack
        """
        return tuple(tuple(stack.get_item().get_id() if stack else None for stack in row) for row in self._items)

    def get_size(self):
        """(int, int) Returns the (row, column) size of this inventory"""

        rows = len(self._items)
        columns = len(self._items[0])

        return rows, columns

    def __getitem__(self, position) -> Stack:
        """(Stack) Returns the stack at position, or None"""
        row, column = position
        return self._items[row][column]

    def __setitem__(self, position, stack: Stack):
        """Sets the stack at position to 'stack'

        Parameters:
            stack (Stack): The stack to set, or None
        """
        row, column = position
        self._items[row][column] = stack

    def __len__(self):
        """(int) Returns the total number of elements in this grid"""
        rows, columns = self.get_size()
        return rows * columns

    def items(self) -> Generator[Tuple[Tuple[int, int], Stack], None, None]:
        """Yields position, cell pairs for each cell in this grid

        cell will either be a Stack, or None if its empty
        Similar to dict.items"""
        for i, row in enumerate(self._items):
            for j, cell in enumerate(row):
                yield (i, j), cell

    def keys(self):
        """Yields the position each cell in this grid
        Similar to dict.keys"""
        yield from self

    def values(self):
        """Yields the cell value of each cell in this grid

        cell value will either be a Stack, or None if the cell is empty
        Similar to dict.items"""
        for i, row in enumerate(self._items):
            for j, cell in enumerate(row):
                yield cell

    def __iter__(self):
        """Alias to .items()"""
        for i, row in enumerate(self._items):
            for j, cell in enumerate(row):
                yield (i, j)

    def pop(self, position):
        """(Stack) Removes & returns the stack at 'position', or None if there is no stack"""
        value = self[position]
        self[position] = None
        return value

    def __contains__(self, position):
        """(bool) Returns True iff 'position' is a position on this grid"""
        row, column = position
        rows, columns = self.get_size()

        return 0 <= row < rows and 0 <= column < columns

    def add_item(self, item: Item):
        """Add a single item to the inventory, to an existing stack of its type of the first
        available empty.

        Parameters:
            item (Item): item to add to the inventory

        Return:
             bool: True iff the item was be added"""
        return self.add_items(Stack(item, 1)) is None

    def add_items(self, stack: Stack):
        """Add a stack to the inventory. The insertion method will first try combining existing
        stacks before placing the remaining new stack into the first empty cell (if any). The
        return of this method must be checked to verify the given stack does not have remaining
        quantity.

        Parameters:
            stack (Stack): stack to add to the inventory

        Return:
             Stack: Remaining (sub-)stack that could not be added, or None if all was added"""

        # fill existing stacks
        for position, this_stack in self.items():
            if this_stack and this_stack.matches(stack):  # stacks match
                this_stack.absorb(stack)
                if stack.get_quantity() == 0:
                    break

        # fill empty stacks, if necessary
        if stack:
            for position, this_stack in self.items():
                if this_stack is None:
                    self[position] = this_stack = Stack(stack.get_item(), 0)
                    this_stack.absorb(stack)
                if stack.get_quantity() == 0:
                    break

        if stack and stack.get_quantity() > 0:
            return stack


class SelectableGrid(Grid):
    """A grid that can have a single cell selected"""

    def __init__(self, rows=4, columns=5):
        super().__init__(rows=rows, columns=columns)

        self._selected = None

    def get_selected(self):
        """(tuple<int, int>) Returns the position of the selected cell, or None if no cell is selected"""
        return self._selected

    def get_selected_value(self):
        """(*) Returns the value in the selected cell, or None if no cell is selected"""
        if self._selected:
            return self[self._selected]
        else:
            return None

    def select(self, position):
        """Selects the cell at 'position'

        Raises:
            KeyError if position does not exist on this grid
        """
        if position not in self:
            raise KeyError(f"Invalid position {position} on {self.get_size()} grid")

        self._selected = position

    def deselect(self):
        """Deselects the currently selected cell"""
        self._selected = None

    def toggle_selection(self, position):
        """Toggles the selection of the cell at 'position'
        I.e. if the cell is selected, it is deselected; vice-versa

        Raises:
            KeyError if position does not exist on this grid
        """
        if position not in self:
            raise KeyError(f"Invalid position {position} on {self.get_size()} grid")

        if self._selected == position:
            self._selected = None
        else:
            self._selected = position
