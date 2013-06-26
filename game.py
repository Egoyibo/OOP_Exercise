import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Horns"

    def  next_pos(self, direction):
        if direction == "up":
            return (self.x, (self.y-1))
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x - 1, self.y)
        elif direction == "right":
            return (self.x + 1 , self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.points = 0
        self.IMAGE = "Boy"

class Gem(GameElement):


    def __init__(self):
        GameElement.__init__(self)
        self.IMAGE = "BlueGem"
        self.SOLID = False 

    def interact(self, player):
        if self.IMAGE == "BlueGem":
            player.inventory.append(self)
            player.points +=1
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % player.points)
        elif self.IMAGE == "OrangeGem":
            print player.inventory
            player.points -=1
            #player.inventory.pop()
            GAME_BOARD.draw_msg("Orange is bad! You lose a point. You now have %d gems" % player.points)

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
        (2,1), 
        (1,2),
        (3,2),
        (2,3)
    ]

    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2,PLAYER)

    GAME_BOARD.draw_msg("This game is wicked awesome.")
    gem_positions = [
        (4,4),
        (3,1),
        (1,1)
    ]

    gems = []
    for gem_pos in gem_positions:
        gem = Gem()

        gems.append(gem)
        gems[0].IMAGE = "OrangeGem"
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(gem_pos[0], gem_pos[1], gem)



def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        GAME_BOARD.draw_msg("You pressed up")
        direction = "up"

    elif KEYBOARD[key.DOWN]:
        GAME_BOARD.draw_msg("You pressed down")
        direction = "down"

    elif KEYBOARD[key.LEFT]:
        GAME_BOARD.draw_msg("You pressed left")
        direction = "left"

    elif KEYBOARD[key.RIGHT]:
        GAME_BOARD.draw_msg("You pressed right")
        direction = "right"

    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)
        else:
            GAME_BOARD.draw_msg("You can't move through a rock!!!")




        # rock1 = Rock()
    # GAME_BOARD.register(rock1)
    # GAME_BOARD.set_el(1,1, rock1)

    # rock2 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(2,2, rock2)

    # rock3 = Rock()
    # GAME_BOARD.register(rock3)
    # GAME_BOARD.set_el(4,4, rock3)
    # print "The first rock is at ", (rock1.x, rock1.y)
    # print "The second rock is at ", (rock2.x, rock2.y)
    # print "The third rock is at ", (rock3.x, rock3.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE

