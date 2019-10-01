"""
Classes to manage modelling & display of crafting
"""

__author__ = "Benjamin Martin and Paul Haley"
__version__ = "1.1.0"
__date__ = "26/04/2019"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk

from core import TK_MOUSE_EVENTS
from grid import Grid, SelectableGrid, ItemGridView
from core import get_modifiers



class GridCrafter:
    def __init__(self, recipes, rows=2, columns=2):
        """Initialises a row x column grid crafter with certain recipes

        Parameters:
            recipes (list<
                        tuple<
                            tuple<
                                tuple<
                                    str
                                >
                            >,
                            Stack
                        >
                    >):
                    A list of pairs of (ingredients & result)
                    See CRAFTING_RECIPES_2x2, etc. in app.py
            rows (int): The number of rows in the crafting input
            columns (int): The number of rows in the crafting output
        """
        self._input = SelectableGrid(rows=rows, columns=columns)
        self._output = None
        self._selected = None

        for recipe, result in recipes:
            if len(recipe) != rows or len(recipe[0]) != columns:
                raise ValueError(f"Wrong recipe dimensions; expecting {rows}x{columns} but "
                                 f"got {len(recipe)}x{len(recipe[0])} with {recipe}")

        self._recipes = recipes

    def find_match(self, ingredients):
        """Finds the first recipe that matches ingredients

        Parameters:
            ingredients (tuple<
                                tuple<
                                    str
                                >
                            >):
                    The ingredients to search for

        Return:
            tuple<
                tuple<
                    tuple<
                        str
                    >
                >,
                Stack
            >: The result of crafting with these ingredients, or None
            (Recipes parameter of __init__ is a list of these)
        """
        for recipe in self._recipes:
            if ingredients == recipe[0]:
                return recipe

        return None

    def craft(self):
        """Crafts the input to the output"""
        # get key
        ingredients = self._input.get_crafting_pattern()

        recipe = self.find_match(ingredients)

        if not recipe:
            print("No matching recipe")
        else:
            result = recipe[1].copy()
            print("Crafts to: ", result)

            if self._output is None:
                self._output = result
            elif self._output.matches(result) and self._output.get_space() > 0:
                self._output.absorb(result)
            else:
                print("Can't craft when output is full")
                return

            # consume ingredients
            self.consume()

    def consume(self):
        """Consumes 1 of each ingredient"""
        for key, stack in self._input.items():
            if stack is None:
                continue

            stack.decrement()

            if len(stack) == 0:
                self._input[key] = None

    def get_input_size(self):
        """(tuple<int, int>) Returns the (row, column) size of the input grid"""
        return self._input.get_size()

    def __getitem__(self, key):
        """(*) Returns the stack at the cell corresponding to key, or None
        Enables square bracket syntax:
        stack = self[key]
        """
        if key == "output":
            return self._output
        else:
            return self._input[key]

    def __setitem__(self, key, stack):
        """(*) Sets the stack at the cell corresponding to key to 'stack'
        Enables square bracket syntax:
        self[key] = stack
        """
        if key == "output":
            self._output = stack
        else:
            self._input[key] = stack

    def keys(self):
        """(*) Yields each key in this grid crafter"""
        yield from self._input

        yield "output"

    def values(self):
        """(Stack) Yields each value in this grid crafter, including None for empty cells"""
        for key in self.keys():
            yield self[key]

    def items(self):
        """(tuple<*, Stack>) Yields key, value pairs for each cell in this grid crafter,
        including None as a value for empty cells"""
        for key in self.keys():
            yield key, self[key]

    def get_selected(self):
        """(*) Returns the key of the selected cell, or None if no cell is selected"""
        return self._selected

    def get_selected_value(self):
        """(Stack) Returns the value of the selected cell, or None if no cell is selected"""
        if self._selected:
            return self[self._selected]
        else:
            return None

    def select(self, key):
        """Selects the cell corresponding to 'key'

        Parameters:
            key (*): A key corresponding to a cell in this grid crafter

        Raises:
            KeyError: if 'key' is not a valid key for this grid crafter
        """
        if key not in self:
            raise KeyError(f"Invalid key {key} for {self.__class__.__name__} crafter")

        self._selected = key

    def deselect(self):
        """Deselects the currently selected cell"""
        self._selected = None

    def toggle_selection(self, key):
        """Toggles the cell corresponding to 'key'
        (i.e. selects if deselected, and deselects if selected)

        Parameters:
            key (*): A key corresponding to a cell in this grid crafter

        Raises:
            KeyError: if 'key' is not a valid key for this grid crafter
        """
        if key not in self:
            raise KeyError(f"Invalid key {key} for {self.__class__.__name__} crafter")

        if self._selected == key:
            self._selected = None
        else:
            self._selected = key


class GridCrafterView(tk.Frame):
    """A tkinter widget used to display crafting with a grid as input and a single cell as output"""

    def __init__(self, master, input_size):
        """Constructor

        Parameters:
            master (tk.Frame | tk.Toplevel | tk.Tk): Tkinter parent widget
            input_size (tuple<int, int>):
                    The (row, column) size of the grid crafter's input grid
        """
        super().__init__(master)

        # Task 2.2 Crafting: Create widgets here
        # ...
        # create input/output/button wedgets
        self._input_widget = ItemGridView(self, input_size)
        self._crafting_button = tk.Button(self, text=" => Craft => ")
        self._output_widget = ItemGridView(self, (1,1))
        self._input_widget.pack(side=tk.LEFT)
        self._crafting_button.pack(side=tk.LEFT)
        self._output_widget.pack(side=tk.TOP)


    def render(self, key_stack_pairs, selected):
        """Renders the stacks at appropriate cells, as determined by 'key_stack_pairs'

        Parameters:
            key_stack_pairs (tuple<*, Stack>):
                    (key, stack) pairs, where each stack should be drawn at the cell
                    corresponding to key
            selected (*): The key that is currently selected, or None if no key is selected
        """
        # Task 2.2 Crafting: Render widgets here
        # ...

        print(f"{selected} is selected")
        for key, stack in key_stack_pairs:
            print(f"Redrawing {stack} at {key}")
            if key == "output":
                # Task 2.2 Crafting: Draw output cell
                # ...
                self._output_widget.draw_cell((0,0),stack,key==selected)

            else:
                # Task 2.2 Crafting: Draw input cells
                # ...

                self._input_widget.draw_cell(key,stack,key==selected)

    def bind_for_id(self, event, callback):
        """Binds callback to tkinter mouse event

        Callback accept parameters: callback(key, event), where
          - key (*) is the key of the cell clicked, etc.
          - mouse_event (tk.MouseEvent) is the original mouse event from tkinter
        """
        if event not in TK_MOUSE_EVENTS:
            return

        # Task 2.2 Crafting: Bind to tkinter widgets here
        # When a cell is clicked, we need to call the callback. Tkinter's bind does
        # this for us, but not exactly how we want. Tkinter bound callbacks have a single
        # parameter, the mouse event containing useful information about the click (i.e.
        # the x & y coordinates)
        #
        # However, x & y coordinates aren't that useful. The class controlling this widget
        # (i.e. CraftingWindow) only needs to know which cell was clicked. It's not
        # concerned with where it was clicked, just that it was. This is so it can easily
        # interact with the crafter model (i.e. GridCrafter) and move stacks around or
        # select/deselect them.
        #
        # To integrate with CraftingWindow, you will need to transform the callback
        # provided to tk.bind, exactly as is done in ItemGridView.bind_for_id, except
        # the first argument may not necessarily be a (row, column) position, but
        # simply an arbitrary key (for basic 2x2 crafting, the 5 keys are:
        #    "output", (0, 0), (0, 1), (1, 0), (1, 1)
        #
        # ...
        self._input_widget.bind(event, lambda e: callback(self._input_widget.xy_to_grid((e.x, e.y)), e))
        self._output_widget.bind(event, lambda e: callback("output",e))
        self._crafting_button.bind(event, lambda e: callback("craft", e))
    # Task 2.2 Crafting: You may add additional methods here
    # ...


class CraftingWindow(tk.Toplevel):
    """Tkinter widget to manage a the three relevant widgets for a crafting window:
        crafter, inventory, and hotbar"""

    def __init__(self, master, title, hot_bar: Grid, inventory: Grid, crafter: GridCrafter):
        """Constructor

        Parameters:
            master (tk.Tk | tk.Toplevel): Tkinter parent widget
            title (str): The title of the window
            hotbar (Grid): The hotbar to show at the bottom of the window
            inventory (Grid): The inventory to show above the hotbar, below the crafting widget
            crafter (GridCraft): The crafter that powers the crafting widget
        """
        super().__init__(master)

        self.title(title)

        self._sources = {
            'hot_bar': hot_bar,
            'inventory': inventory,
            'crafter': crafter
        }

        self._source_views = {}

        self._load_crafter_view()

        self._selection = None

        for widget_key in ('inventory', 'hot_bar'):
            widget = self._sources[widget_key]
            self._source_views[widget_key] = view_widget = ItemGridView(self, widget.get_size())
            view_widget.pack()

            view_widget.bind_for_id("<Button-1>",
                                    lambda key, e, widget_key=widget_key: self._handle_left_click(widget_key, key, e))
            view_widget.bind_for_id("<Button-2>",
                                    lambda key, e, widget_key=widget_key: self._handle_right_click(widget_key, key, e))

        self.redraw()

    def _load_crafter_view(self):
        """Loads the appropriate crafter view"""
        self._source_views['crafter'] = crafter_view = GridCrafterView(self, self._sources['crafter'].get_input_size())

        crafter_view.pack()
        crafter_view.bind_for_id("<Button-1>", lambda key, e: self._handle_left_click("crafter", key, e))
        crafter_view.bind_for_id("<Button-2>", lambda key, e: self._handle_right_click("crafter", key, e))
        crafter_view.bind_for_id("<Button-3>", lambda key, e: self._handle_right_click("crafter", key, e))
    def redraw(self):
        """Redraws all widgets (i.e. crafter, inventory, & hotbar)"""
        selected_widget, selected_position = self._selection if self._selection else (None, None)

        for key, widget in self._sources.items():
            view_widget = self._source_views[key]
            view_widget.render(widget.items(), selected_position if selected_widget == key else None)

    def get_source(self, widget, key):
        """(Stack) Returns the stack at the cell corresponding to 'key' in 'widget'"""
        return self._sources[widget][key]

    def set_source(self, widget, key, stack):
        """Makes 'stack' the stack at the cell corresponding to 'key' in 'widget'"""
        self._sources[widget][key] = stack

    def attempt_split(self, from_widget, from_key, to_widget, to_key):
        """Attempts to split the stack at (from_widget, from_key) in half
        into the stack at (to_widget, to_key)"""

        from_stack = self._sources[from_widget][from_key]
        to_stack = self._sources[to_widget][to_key]

        if from_stack is None or to_stack is not None:
            return False

        to_stack = from_stack.split()

        if to_stack.is_empty():
            return False

        self._sources[to_widget][to_key] = to_stack
        return True

    def move1(self, selection, key_modifiers):
        """Processes primary movement to 'selection'

        Parameters:
            selection (tuple<str, *>): A (widget, key) pair, corresponding to the
            exact cell being moved to
            key_modifiers (set<str>): A set of all relevant keyboard modifiers
                                      (see get_modifiers in core.py)
        """
        # I know this is a behemoth, but deadlines :(
        if self._selection:
            if selection == self._selection:
                self._selection = None

            else:
                from_stack = self.get_source(*self._selection)
                to_stack = self.get_source(*selection)

                if to_stack is None:
                    # Destination is empty
                    if 'ctrl' in key_modifiers:
                        # All
                        self.set_source(*self._selection, to_stack)
                        self.set_source(*selection, from_stack)

                        self._selection = None
                    else:
                        # One at a time
                        to_stack = from_stack.split(count=1)

                        self.set_source(*selection, to_stack)
                else:
                    # Destination is non-empty
                    if to_stack.matches(from_stack) and from_stack.get_item().is_stackable():
                        # Source & Destination match
                        to_stack.absorb(from_stack, maximum=None if 'ctrl' in key_modifiers else 1)
                    else:
                        # Source & Destination don't match
                        self._selection = selection

                if from_stack.is_empty():
                    self.set_source(*self._selection, None)
                    self._selection = None
        elif self.get_source(*selection) is not None:
            self._selection = selection

    def move2(self, selection, key_modifiers):
        """Processes secondary movement to 'selection'

        Parameters:
            selection (tuple<str, *>): A (widget, key) pair, corresponding to the
            exact cell being moved to
            key_modifiers (set<str>): A set of all relevant keyboard modifiers
                                      (see get_modifiers in core.py)
        """
        if self._selection is None:
            return

        if self.attempt_split(*self._selection, *selection):
            self._selection = None
        else:
            from_stack = self.get_source(*self._selection)
            to_stack = self.get_source(*selection)
            self.set_source(*selection, from_stack)
            self.set_source(*self._selection, to_stack)

    def _handle_left_click(self, widget_key, key, mouse_event):
        """Handles a left click on any cell in any widget

        Parameters:
            widget_key (str): The key of the widget clicked (e.g. 'inventory', etc.)
            key (*): The unique key of the cell in the widget that was clicked (e.g.
                     'output', (0, 0), etc.)
            mouse_event (tk.MouseEvent): The original tkinter mouse event
        """
        print(f"Left clicked on {widget_key} @ {key}")
        selection = widget_key, key

        if selection == ('crafter', 'craft'):
            self._sources['crafter'].craft()
        else:
            self.move1(selection, get_modifiers(mouse_event.state))

        self.redraw()

    def _handle_right_click(self, widget_key, key, mouse_event):
        """Handles a right click on any cell in any widget

        Parameters:
            widget_key (str): The key of the widget clicked (e.g. 'inventory', etc.)
            key (*): The unique key of the cell in the widget that was clicked (e.g.
                     'output', (0, 0), etc.)
            mouse_event (tk.MouseEvent): The original tkinter mouse event
        """
        print(f"Right clicked on {widget_key} @ {key}")
        selection = widget_key, key

        if selection == ('crafter', 'craft'):
            return
        else:
            self.move2(selection, get_modifiers(mouse_event.state))

        self.redraw()
