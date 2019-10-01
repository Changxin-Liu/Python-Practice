"""
Simple 2d world where the player can interact with the items in the world.
"""

__author__ = "Changxin Liu   45245008"
__date__ = "24/05/2019"
__version__ = "1.1.0"
__copyright__ = "The University of Queensland, 2019"

import tkinter as tk
from tkinter import messagebox
from tkinter import *

import random
from collections import namedtuple

import pymunk

from block import Block, ResourceBlock, BREAK_TABLES, LeafBlock, TrickCandleFlameBlock
from grid import Stack, Grid, SelectableGrid, ItemGridView
from item import Item, SimpleItem, HandItem, BlockItem, MATERIAL_TOOL_TYPES, TOOL_DURABILITIES
from player import Player
from dropped_item import DroppedItem
from crafting import GridCrafter, CraftingWindow
from world import World
from core import positions_in_range
from game import GameView, WorldViewRouter
from mob import Bird, Mob


BLOCK_SIZE = 2 ** 5
GRID_WIDTH = 2 ** 5
GRID_HEIGHT = 2 ** 4

# Task 3/Post-grad only:
# Class to hold game data that is passed to each thing's step function
# Normally, this class would be defined in a separate file
# so that type hinting could be used on PhysicalThing & its
# subclasses, but since it will likely need to be extended
# for these tasks, we have defined it here
GameData = namedtuple('GameData', ['world', 'player'])


class FoodItem(Item):
    """An item that can increase the player's food/health"""
    def __init__(self, id_, strength):
        """ Constructor.

            Parameters:
            id_ (str): The unique id of this item
            strength(float): The increase of food/health
        """
        super().__init__(id_)
        self._strength = strength

    def can_attack(self) -> bool:
        """(bool) Returns False, since FoodItems cannot be used to attack"""
        return False

    def get_strength(self):
        """float: Returns the amount of food/health to be recovered by the player by when used"""
        return self._strength

    def place(self):
        """float: Returns an effect that represents an increase in the player's food/health

        Return:
            [tuple<str, tuple<str, ...>>]:
                    A list of EffectIDs resulting from placing this item. Each EffectID is a pair
                    of (effect_type, effect_sub_id) pair, where:
                      - effect_type is the type of the effect ('item', 'block', etc.)
                      - effect_sub_id is the unique identifier for an effect of a particular type
        """

        return [('effect', ("food", self._strength))]


class ToolItem(Item):
    """An item that can be used as a tool"""
    def __init__(self,id_, tool_type, durability):
        """ Constructor.

            Parameters:
                    id_ (str): The unique id of this item
                    tool_type(str): The type of this tool
                    durability(float): The durability of this tool
         """
        super().__init__(id_ ,max_stack=1, attack_range=10)
        self._tool_type = tool_type
        self._durability = durability
        self._current_durability = self._durability

    def can_attack(self) -> bool:
        """(bool) Returns False, since when the durability reaches 0, the tool cannot be used to attack"""
        if self._current_durability > 0:
            return True
        return False

    def get_type(self):
        """(str) Returns the tool's type"""
        return self._tool_type

    def get_durability(self):
        """(float) Returns the tool's remaining durability."""
        return self._current_durability

    def attack(self, successful:bool):
        """Attacks with the tool; if the attack was not successful, the tool's durability should be reduced by one."""
        if successful == False:
            self._current_durability = self._current_durability - 1

    def get_max_stack_size(self):
        """(int) Returns the max stack size of a tool"""
        return 1

    def get_max_durability(self):
        """(int) Returns the max durability of a tool"""
        return self._durability





class CraftingTableBlock(ResourceBlock):
    """A block content with a simple life that drops an
        item form itself when mined and can be used to access crafting window"""

    def __init__(self):
        """Constructor"""
        # A break table for CraftingTable
        _break_table = {
            "hand": (7.5, False),
            "wood_pickaxe": (1.15, True),
            "stone_pickaxe": (0.6, True),
            "iron_pickaxe": (0.4, True),
            "diamond_pickaxe": (0.3, True),
            "golden_pickaxe": (0.2, True)
        }
        super().__init__('crafting_table', _break_table)

    def get_drops(self, luck, correct_item_used):
        """Drops a itself in item form 1 time

        See Block.get_drops for parameters & return"""

        if correct_item_used:
            # Drop 1 of itself in item form
            return [('item', (self._id,))] * 1
    def can_use(self):
        """(bool) Returns True since this block can be used."""
        return True

    def use(self):
        """A method to use this block"""
        return ('crafting', 'crafting_table')

    def __repr__(self):
        return f"CraftingTableBlock({self._id!r})"




def create_block(*block_id):
    """(Block) Creates a block (this function can be thought of as a block factory)

    Parameters:
        block_id (*tuple): N-length tuple to uniquely identify the block,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_block("leaf")
        LeafBlock()
        >>> create_block("stone")
        ResourceBlock('stone')
        >>> create_block("mayhem", 1)
        TrickCandleFlameBlock(1)
    """
    if len(block_id) == 1:
        block_id = block_id[0]
        if block_id == "leaf":
            return LeafBlock()
        elif block_id in BREAK_TABLES:
            return ResourceBlock(block_id, BREAK_TABLES[block_id])
        elif block_id not in BREAK_TABLES:
            # create a crafting_table block here
            return CraftingTableBlock()

    elif block_id[0] == 'mayhem':
        return TrickCandleFlameBlock(block_id[1])

    raise KeyError(f"No block defined for {block_id}")


def create_item(*item_id):
    """(Item) Creates an item (this function can be thought of as a item factory)

    Parameters:
        item_id (*tuple): N-length tuple to uniquely identify the item,
        often comprised of strings, but not necessarily (arguments are grouped
        into a single tuple)

    Examples:
        >>> create_item("dirt")
        BlockItem('dirt')
        >>> create_item("hands")
        HandItem('hands')
        >>> create_item("pickaxe", "stone")  # *without* Task 2.1.2 implemented
        Traceback (most recent call last):
        ...
        NotImplementedError: "Tool creation is not yet handled"
        >>> create_item("pickaxe", "stone")  # *with* Task 2.1.2 implemented
        ToolItem('stone_pickaxe')
    """
    if len(item_id) == 2:

        if item_id[0] in MATERIAL_TOOL_TYPES and item_id[1] in TOOL_DURABILITIES:
            # Create different tools with different materials
            return ToolItem(item_id[1]+'_'+item_id[0],item_id[0],TOOL_DURABILITIES[item_id[1]])


    elif len(item_id) == 1:

        item_type = item_id[0]

        if item_type == "hands":
            return HandItem("hands")

        elif item_type == "dirt":
            return BlockItem(item_type)

        # Task 1.4 Basic Items: Create wood & stone here
        # ...
        elif item_type == "wood":
            return BlockItem(item_type)
        elif item_type == "stone":
            return BlockItem(item_type)
        elif item_type == "leave":
            return BlockItem(item_type)
        elif item_type == "stick":
            return BlockItem(item_type)
        elif item_type == "crafting_table":
            return BlockItem(item_type)
        elif item_type == "apple":
            return FoodItem(item_type, 2.0)






    raise KeyError(f"No item defined for {item_id}")
#Crafting recipes
CRAFTING_RECIPES_3x3 = {

            (
                (
                    (None, None, None),
                    (None, 'wood', None),
                    (None, 'wood', None)
                ),
                Stack(create_item('stick'), 16)
            ),
            (
                (
                    ('wood', 'wood', 'wood'),
                    (None, 'stick', None),
                    (None, 'stick', None)
                ),
                Stack(create_item('pickaxe', 'wood'), 1)
            ),
            (
                (
                    ('wood', 'wood', None),
                    ('wood', 'stick', None),
                    (None, 'stick', None)
                ),
                Stack(create_item('axe', 'wood'), 1)
            ),
            (
                (
                    (None, 'wood', None),
                    (None, 'stick', None),
                    (None, 'stick', None)
                ),
                Stack(create_item('shovel', 'wood'), 1)
            ),
            (
                (
                    (None, 'stone', None),
                    (None, 'stone', None),
                    (None, 'stick', None)
                ),
                Stack(create_item('sword', 'wood'), 1)
            ),
            (
                (
                    ('stone','stone','stone'),
                    (None,    None,   None  ),
                    ('wood','wood','wood')
                ),
                Stack(create_item('sword', 'stone'),1)
            ),
            (
                (
                    ('dirt','dirt','dirt'),
                    (None,None,None),
                    ('stone','stone','stone')
                ),
                Stack(create_item('axe','stone'),1)
            ),
            (
                (
                    ('wood','wood','wood'),
                    (None,None,None),
                    ('stone','stone','stone')
                ),
                Stack(create_item('axe','wood'),1)
            )
        }

CRAFTING_RECIPES_2x2 = [
            (
                (
                    (None, 'wood'),
                    (None, 'wood')
                ),
                Stack(create_item('stick'), 4)
            ),
            (
                (
                    (None,'dirt'),
                    (None,'wood')
                ),
                Stack(create_item('stone'), 4)
            ),
            (
                (
                    (None,'dirt'),
                    (None,'dirt')
                ),
                Stack(create_item('wood'),4)
            ),
            (
                (
                    ('stone',None),
                    (None,'stick')
                ),
                Stack(create_item('stick'),4)
            ),
            (
                (
                    ('wood', 'wood'),
                    ('wood', 'wood')
                ),
                Stack(create_item('crafting_table'), 1)
            )
        ]





# Task 1.3: Implement StatusView class here
# ...
class StatusView(tk.Frame):
    """
    To display information to the player about their status in the game.

    """
    def __init__(self, master):
        """Constructor"""
        super().__init__(master)
        # Health label
        self._heart_image = tk.PhotoImage(file='heart.png')
        self._heart_image = self._heart_image.subsample(10)
        self._heart = tk.Label(self, image=self._heart_image)
        self._heart.pack(side=tk.LEFT)
        self._health_label = tk.Label(self, text='Health:')
        self._health_label.pack(side=tk.LEFT)
        # Food label
        self._drumstick_image = tk.PhotoImage(file='drumstick.png')
        self._drumstick_image = self._drumstick_image.subsample(70)
        self._drumstick = tk.Label(self, image=self._drumstick_image)
        self._drumstick.pack(side=tk.LEFT)
        self._food_label = tk.Label(self, text='Food:')
        self._food_label.pack(side=tk.LEFT)

    def set_health(self, health):
        """Show the player's health"""
        self._health_label.config(text='Health:{}'.format(health))


    def set_food(self,food):
        """Show the player's food"""
        self._food_label.config(text='Food:{}'.format(food))



BLOCK_COLOURS = {
    'diamond': 'blue',
    'dirt': '#552015',
    'stone': 'grey',
    'wood': '#723f1c',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
}

ITEM_COLOURS = {
    'diamond': 'blue',
    'dirt': '#552015',
    'stone': 'grey',
    'wood': '#723f1c',
    'apple': '#ff0000',
    'leaves': 'green',
    'crafting_table': 'pink',
    'furnace': 'black',
    'cooked_apple': 'red4'
}


def load_simple_world(world):
    """Loads blocks into a world

    Parameters:
        world (World): The game world to load with blocks
    """
    block_weights = [
        (100, 'dirt'),
        (30, 'stone'),
    ]

    cells = {}

    ground = []

    width, height = world.get_grid_size()

    for x in range(width):
        for y in range(height):
            if x < 22:
                if y <= 8:
                    continue
            else:
                if x + y < 30:
                    continue

            ground.append((x, y))

    weights, blocks = zip(*block_weights)
    kinds = random.choices(blocks, weights=weights, k=len(ground))

    for cell, block_id in zip(ground, kinds):
        cells[cell] = create_block(block_id)

    trunks = [(3, 8), (3, 7), (3, 6), (3, 5)]

    for trunk in trunks:
        cells[trunk] = create_block('wood')

    leaves = [(4, 3), (3, 3), (2, 3), (4, 2), (3, 2), (2, 2), (4, 4), (3, 4), (2, 4)]

    for leaf in leaves:
        cells[leaf] = create_block('leaf')

    for cell, block in cells.items():
        # cell -> box
        i, j = cell

        world.add_block_to_grid(block, i, j)

    world.add_block_to_grid(create_block("mayhem", 0), 14, 8)

    world.add_mob(Bird("friendly_bird", (12, 12)), 400, 100)






class Ninedraft:
    """High-level app class for Ninedraft, a 2d sandbox game"""

    def __init__(self, master):
        """Constructor

        Parameters:
            master (tk.Tk): tkinter root widget
        """

        self._master = master
        self._world = World((GRID_WIDTH, GRID_HEIGHT), BLOCK_SIZE)

        load_simple_world(self._world)

        self._player = Player()
        self._world.add_player(self._player, 250, 150)

        self._world.add_collision_handler("player", "item", on_begin=self._handle_player_collide_item)

        self._hot_bar = SelectableGrid(rows=1, columns=10)
        self._hot_bar.select((0, 0))

        starting_hotbar = [
            Stack(create_item("dirt"), 20),
            Stack(create_item("apple"), 4),
            Stack(create_item("pickaxe","diamond"),1),
            Stack(create_item("axe","iron"),1),
            Stack(create_item("crafting_table"),1)

        ]



        for i, item in enumerate(starting_hotbar):
            self._hot_bar[0, i] = item

        self._hands = create_item('hands')

        starting_inventory = [
            ((1, 5), Stack(create_item('dirt'), 10)),
            ((0, 2), Stack(create_item('wood'), 10)),
            ((2, 5), Stack(create_item('stick'), 4)),
            ((0, 0), Stack(create_item('stone'), 10)),
        ]
        self._inventory = Grid(rows=3, columns=10)
        for position, stack in starting_inventory:
            self._inventory[position] = stack



        self._crafting_window = None
        self._master.bind("e",
                          lambda e: self.run_effect(('crafting', 'basic')))



        self._view = GameView(master, self._world.get_pixel_size(), WorldViewRouter(BLOCK_COLOURS, ITEM_COLOURS))
        self._view.pack()

        # Task 1.2 Mouse Controls: Bind mouse events here
        # ...
        self._view.bind('<Motion>', self._mouse_move)
        self._view.bind('<Leave>', self._mouse_leave)
        self._view.bind('<Button-1>', self._left_click)
        # For a Macbook, without a mouse to do a right click
        self._view.bind('<Button-2>', self._right_click)
        # For normal devices, with a mouse to do a right click
        self._view.bind('<Button-3>', self._right_click)
        # Task 1.3: Create instance of StatusView here
        # ...
        self._status_view = StatusView(self._master)
        self._status_view.pack(side=tk.TOP)


        self._hot_bar_view = ItemGridView(master, self._hot_bar.get_size())
        self._hot_bar_view.pack(side=tk.TOP, fill=tk.X)

        # Task 1.5 Keyboard Controls: Bind to space bar for jumping here
        # ...
        self._master.bind("<space>", lambda e: self._jump())


        self._master.bind("a", lambda e: self._move(-1,0))
        self._master.bind("<Left>", lambda e: self._move(-1, 0))
        self._master.bind("d", lambda e: self._move(1, 0))
        self._master.bind("<Right>", lambda e: self._move(1, 0))
        self._master.bind("s", lambda e: self._move(0, 1))
        self._master.bind("<Down>", lambda e: self._move(0, 1))

        # Task 1.5 Keyboard Controls: Bind numbers to hotbar activation here
        # ...
        # Do selection or deselection with keys from 1 to 9.
        for key_number in range(1,10):
            self._master.bind(str(key_number),lambda e ,key=key_number: self._activate_item(key-1))
        # 0 controls the last cell of the hotbar
        self._master.bind("0",lambda e:self._activate_item((9)))



        # Task 1.6 File Menu & Dialogs: Add file menu here
        # ...
        self._menubar = tk.Menu(master)
        master.config(menu=self._menubar)
        self._filemenu = tk.Menu(self._menubar)
        # restart or exit the game through the menu
        self._filemenu.add_command(label="New Game",command = self.message_box_restart)
        self._filemenu.add_command(label="Exit",command = self.message_box_exit)
        self._menubar.add_cascade(label="File", menu = self._filemenu)
        # exit the game when trying to close the window
        self._master.protocol("WM_DELETE_WINDOW", self.message_box_exit)

        self._target_in_range = False
        self._target_position = 0, 0

        self.redraw()

        self.step()

    def message_box_exit(self):
        """Exit the game if you choose yes and do nothing if you choose no."""
        exit = messagebox.askyesno("Exit","Would you like to exit the game?")
        if exit == True:
            self._master.destroy()


    def restart_the_game(self):
        """Reset the game"""
        # reset the world
        self._world = World((GRID_WIDTH, GRID_HEIGHT), BLOCK_SIZE)
        load_simple_world(self._world)
        # reset the player
        self._player = Player()
        self._world.add_player(self._player, 250, 150)

        self._world.add_collision_handler("player", "item", on_begin=self._handle_player_collide_item)
        # reset the hotbar
        self._hot_bar = SelectableGrid(rows=1, columns=10)
        self._hot_bar.select((0, 0))

        starting_hotbar = [
            Stack(create_item("dirt"), 20),
            Stack(create_item("apple"), 4),
            Stack(create_item("pickaxe", "diamond"), 1),
            Stack(create_item("axe", "iron"), 1),
            Stack(create_item("crafting_table"), 1)
            
        ]

        for i, item in enumerate(starting_hotbar):
            self._hot_bar[0, i] = item

        self._hands = create_item('hands')
        # reset the inventory
        starting_inventory = [
            ((1, 5), Stack(create_item('dirt'), 10)),
            ((0, 2), Stack(create_item('wood'), 10)),
            ((2, 5), Stack(create_item('stick'), 4)),
            ((0, 0), Stack(create_item('stone'),10)),
        ]
        self._inventory = Grid(rows=3, columns=10)
        for position, stack in starting_inventory:
            self._inventory[position] = stack

    def message_box_restart(self):
        """Restart the game if you choose yes and do nothing if you choose no."""
        restart = messagebox.askyesno("New Game", "Would you like to start a new game?")
        if restart == True:
            self.restart_the_game()


    def message_box_restart_for_death(self):
        """If you die, restart the game if you choose yes and exit the game if you choose no."""
        restart = messagebox.askyesno("New Game", "You die!!!! Would you like to start a new game?")
        if restart == True:
            self.restart_the_game()
        else:
            self._master.destroy()



    def redraw(self):
        self._view.delete(tk.ALL)

        # physical things
        self._view.draw_physical(self._world.get_all_things())

        # target
        target_x, target_y = self._target_position
        target = self._world.get_block(target_x, target_y)
        cursor_position = self._world.grid_to_xy_centre(*self._world.xy_to_grid(target_x, target_y))

        # Task 1.2 Mouse Controls: Show/hide target here
        # ...
        self._view.show_target(self._player.get_position(), cursor_position)
        if not self._target_in_range:
            self._view.hide_target()


        # Task 1.3 StatusView: Update StatusView values here
        # ...
        self._status_view.set_health(self._player.get_health())
        self._status_view.set_food(self._player.get_food())
        # hot bar
        self._hot_bar_view.render(self._hot_bar.items(), self._hot_bar.get_selected())

    def step(self):
        data = GameData(self._world, self._player)
        self._world.step(data)

        self.redraw()

        # Task 1.6 File Menu & Dialogs: Handle the player's death if necessary
        # ...
        if self._player.get_health() == 0:
            self.message_box_restart_for_death()


        self._master.after(15, self.step)

    def _move(self, dx, dy):
        self.check_target()
        velocity = self._player.get_velocity()
        self._player.set_velocity((velocity.x + dx * 80, velocity.y + dy * 80))

    def _jump(self):
        self.check_target()
        velocity = self._player.get_velocity()
        # Task 1.2: Update the player's velocity here
        # ...
        self._player.set_velocity((velocity.x * 0.8, velocity.y -200))



    def mine_block(self, block, x, y):
        luck = random.random()

        active_item, effective_item = self.get_holding()

        was_item_suitable, was_attack_successful = block.mine(effective_item, active_item, luck)

        effective_item.attack(was_attack_successful)

        if block.is_mined():
            # Task 1.2 Mouse Controls: Reduce the player's food/health appropriately
            # ...
            if self._player.get_food() > 0:
                self._player.change_food(-1.0)
            else:
                self._player.change_health(-1.0)
            # Task 1.2 Mouse Controls: Remove the block from the world & get its drops
            # ...
            self._world.remove_block(block)
            drops = block.get_drops(luck, was_item_suitable)

            if not drops:
                return

            x0, y0 = block.get_position()

            for i, (drop_category, drop_types) in enumerate(drops):
                print(f'Dropped {drop_category}, {drop_types}')

                if drop_category == "item":
                    physical = DroppedItem(create_item(*drop_types))

                    # this is so bleh
                    x = x0 - BLOCK_SIZE // 2 + 5 + (i % 3) * 11 + random.randint(0, 2)
                    y = y0 - BLOCK_SIZE // 2 + 5 + ((i // 3) % 3) * 11 + random.randint(0, 2)

                    self._world.add_item(physical, x, y)
                elif drop_category == "block":
                    self._world.add_block(create_block(*drop_types), x, y)
                else:
                    raise KeyError(f"Unknown drop category {drop_category}")

    def get_holding(self):
        active_stack = self._hot_bar.get_selected_value()
        active_item = active_stack.get_item() if active_stack else self._hands

        effective_item = active_item if active_item.can_attack() else self._hands

        return active_item, effective_item

    def check_target(self):
        # select target block, if possible
        active_item, effective_item = self.get_holding()

        pixel_range = active_item.get_attack_range() * self._world.get_cell_expanse()

        self._target_in_range = positions_in_range(self._player.get_position(),
                                                   self._target_position,
                                                   pixel_range)

    def _mouse_move(self, event):
        self._target_position = event.x, event.y
        self.check_target()

    def _mouse_leave(self, event):
        self._target_in_range = False

    def _left_click(self, event):
        # Invariant: (event.x, event.y) == self._target_position
        #  => Due to mouse move setting target position to cursor
        x, y = self._target_position

        if self._target_in_range:
            block = self._world.get_block(x, y)
            if block:
                self.mine_block(block, x, y)

    def _trigger_crafting(self, craft_type):
        print(f"Crafting with {craft_type}")
        # Initialise the crafting window
        if craft_type == "basic":
            crafter = GridCrafter(CRAFTING_RECIPES_2x2)

            self.crafter_window = CraftingWindow(self._master, "Basic Crafter", self._hot_bar, self._inventory,crafter)
            # close the crafting window by pressing "e"
            self.crafter_window.bind("e",
                              lambda e: self.crafter_window.destroy())



        # Initialise the crafting table
        elif craft_type == "crafting_table":
            crafter = GridCrafter(CRAFTING_RECIPES_3x3,rows=3,columns=3)
            self.crafter_window = CraftingWindow(self._master,"Advanced Crafter", self._hot_bar, self._inventory, crafter)
            # close the crafting window by pressing "e"
            self.crafter_window.bind("e",
                                     lambda e: self.crafter_window.destroy())


    def run_effect(self, effect):
        if len(effect) == 2:
            if effect[0] == "crafting":
                craft_type = effect[1]

                if craft_type == "basic":
                    print("Can't craft much on a 2x2 grid :/")

                elif craft_type == "crafting_table":
                    print("Let's get our kraft® on! King of the brands")

                self._trigger_crafting(craft_type)
                return
            elif effect[0] in ("food", "health"):
                if self._player.get_food() < self._player.get_max_food():
                    stat, strength = effect
                    print(f"Gaining {strength} {stat}!")
                    getattr(self._player, f"change_{stat}")(strength)
                elif self._player.get_food() == self._player.get_max_food() and self._player.get_health() < self._player.get_max_food():
                    stat, strength = effect
                    stat = 'health'
                    print(f"Gaining {strength} {stat}!")
                    getattr(self._player, f"change_{stat}")(strength)

                return

        raise KeyError(f"No effect defined for {effect}")

    def _right_click(self, event):
        print("Right click")

        x, y = self._target_position
        target = self._world.get_thing(x, y)

        if target:
            # use this thing
            print(f'using {target}')
            effect = target.use()
            print(f'used {target} and got {effect}')

            if effect:
                self.run_effect(effect)

        else:
            # place active item
            selected = self._hot_bar.get_selected()

            if not selected:
                return

            stack = self._hot_bar[selected]
            drops = stack.get_item().place()

            stack.subtract(1)
            if stack.get_quantity() == 0:
                # remove from hotbar
                self._hot_bar[selected] = None

            if not drops:
                return

            # handling multiple drops would be somewhat finicky, so prevent it
            if len(drops) > 1:
                raise NotImplementedError("Cannot handle dropping more than 1 thing")

            drop_category, drop_types = drops[0]

            x, y = event.x, event.y

            if drop_category == "block":
                existing_block = self._world.get_block(x, y)

                if not existing_block:
                    self._world.add_block(create_block(drop_types[0]), x, y)
                else:
                    raise NotImplementedError(
                        "Automatically placing a block nearby if the target cell is full is not yet implemented")

            elif drop_category == "effect":
                self.run_effect(drop_types)

            else:
                raise KeyError(f"Unknown drop category {drop_category}")

    def _activate_item(self, index):
        print(f"Activating {index}")

        self._hot_bar.toggle_selection((0, index))

    def _handle_player_collide_item(self, player: Player, dropped_item: DroppedItem, data,
                                    arbiter: pymunk.Arbiter):
        """Callback to handle collision between the player and a (dropped) item. If the player has sufficient space in
        their to pick up the item, the item will be removed from the game world.

        Parameters:
            player (Player): The player that was involved in the collision
            dropped_item (DroppedItem): The (dropped) item that the player collided with
            data (dict): data that was added with this collision handler (see data parameter in
                         World.add_collision_handler)
            arbiter (pymunk.Arbiter): Data about a collision
                                      (see http://www.pymunk.org/en/latest/pymunk.html#pymunk.Arbiter)
                                      NOTE: you probably won't need this
        Return:
             bool: False (always ignore this type of collision)
                   (more generally, collision callbacks return True iff the collision should be considered valid; i.e.
                   returning False makes the world ignore the collision)
        """

        item = dropped_item.get_item()

        if self._hot_bar.add_item(item):
            print(f"Added 1 {item!r} to the hotbar")
        elif self._inventory.add_item(item):
            print(f"Added 1 {item!r} to the inventory")
        else:
            print(f"Found 1 {item!r}, but both hotbar & inventory are full")
            return True

        self._world.remove_item(dropped_item)
        return False





# Task 1.1 App class: Add a main function to instantiate the GUI here
# ...
def main():
    root = tk.Tk()
    # change the title of the game window
    root.title("Ninedraft")
    app = Ninedraft(root)
    root.mainloop()

if __name__ == '__main__':
    main()

