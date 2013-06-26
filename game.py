import core
import pyglet
from pyglet.window import key
from core import GameElement
from pyglet import clock #to get scheduling for create_love
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER_GIRL = None
PLAYER_BOY = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
# class Rock(GameElement):
#     IMAGE = "Rock"
#     SOLID = True

# class Walls(GameElement):
#     IMAGE = "Wall"
#     SOLID = True

# class Trees(GameElement):
#     IMAGE = "ShortTree"
#     SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

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
        self.has_key = False    #is false until girl finds and picks up key
        self.points = 0
        self.IMAGE = "Princess"


class Obstacles(GameElement):
    SOLID = True

    
class Gem(GameElement):


    def __init__(self):
        GameElement.__init__(self)
        self.IMAGE = "BlueGem"
        self.SOLID = False  

    def interact(self, player):
        if self.IMAGE == "Key":
            player.has_key = True    #if true, girl has picked up key. 
        elif self.IMAGE == "BlueGem":
            player.points +=1
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % player.points)
        elif self.IMAGE == "OrangeGem":
            player.points -=1
            GAME_BOARD.draw_msg("Orange is bad! You lose a point. You now have %d gems" % player.points)


####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    global PLAYER_GIRL
    PLAYER_GIRL = Character()
    GAME_BOARD.register(PLAYER_GIRL)
    GAME_BOARD.set_el(1,6,PLAYER_GIRL)

    global PLAYER_BOY
    PLAYER_BOY = Character()
    PLAYER_BOY.IMAGE = "Boy"
    PLAYER_BOY.SOLID = True
    GAME_BOARD.register(PLAYER_BOY)
    GAME_BOARD.set_el(6,1,PLAYER_BOY)

    #Add any/all obstacles to the board
    obstacle_positions = [
        (2,4), 
        (2,3),
        (2,2),
        (3,2),
        (5,2),
        (6,3),
        (2,6),
        (3,6),
        (4,6),
        (5,6),
        (4,4),
        (5,4),
        (6,4),
        (5,3),
        (5,2),
        (4,2)
    ]

    obstacles = []
    possible_obstacles = ["TallTree", "ShortTree", "Rock"]

    x = 0
    for pos in obstacle_positions:
        obstacle = Obstacles()
        obstacles.append(obstacle)

        #Will put random obstacle image from list possible_obstacles and insert at location from obstacle_positions
        obstacles[x].IMAGE = possible_obstacles[random.randint(0, len(possible_obstacles)-1)]
        x += 1 #counter to go through each item in obstacles[]
        GAME_BOARD.register(obstacle)
        GAME_BOARD.set_el(pos[0], pos[1], obstacle)
    
    key = Obstacles()
    key.IMAGE = "Key"
    key.SOLID = False
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(1,4, key)

    door = Obstacles()
    door.IMAGE = "DoorClosed"
    door.SOLID = True
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(4,1,door)


    #Add gems to the board
    # gem_positions = [
    #     (6,6)
  
    # ]

    # gems = []
    # for gem_pos in gem_positions:
    #     gem = Gem()

    #     gems.append(gem)
    #     gems[0].IMAGE = "OrangeGem"
    #     GAME_BOARD.register(gem)
    #     GAME_BOARD.set_el(gem_pos[0], gem_pos[1], gem)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"

    elif KEYBOARD[key.DOWN]:
        direction = "down"

    elif KEYBOARD[key.LEFT]:
        direction = "left"

    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()

    if direction:
        next_location = PLAYER_GIRL.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]


        if next_y == 0 or next_x == 0 or next_y == 7 or next_x == 7:
            GAME_BOARD.set_el(PLAYER_GIRL.x, PLAYER_GIRL.y, PLAYER_GIRL)
            GAME_BOARD.draw_msg("Sorry! Out of bounds homie!!")
        else:    
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            #If there's an element in the next location:
            if existing_el:
                existing_el.interact(PLAYER_GIRL)
                #If girl's next move is the key
                if existing_el.IMAGE == "Key":
                    PLAYER_GIRL.has_key = True
                    GAME_BOARD.draw_msg("Now you have THE KEY... Hurry! Go find your love!")
                    #Move girl to key's location 
                    GAME_BOARD.del_el(PLAYER_GIRL.x, PLAYER_GIRL.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER_GIRL)
                    #If girl found key, then we stop checking conditions.

                #If the girl is in front of the locked door and has the key
                if existing_el.IMAGE == "DoorClosed" and PLAYER_GIRL.has_key == True:
                    GAME_BOARD.del_el(next_x, next_y)   #deleting closed door
                    existing_el.IMAGE = "DoorOpen"
                    GAME_BOARD.register(existing_el)
                    GAME_BOARD.set_el(next_x, next_y, existing_el) #putting open door

                    #*****Come back and figure out how to open door first before moving through the door
                    GAME_BOARD.del_el(PLAYER_GIRL.x, PLAYER_GIRL.y)
                    GAME_BOARD.set_el(next_x + 1, next_y, PLAYER_GIRL)
            
            #If next move is empty sqare or it's transparent, then move girl to that position
            elif existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER_GIRL.x, PLAYER_GIRL.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER_GIRL)
            
            else:
                GAME_BOARD.draw_msg("That's an obstacle...You can't move through it!!!")

            if existing_el == PLAYER_BOY:
                GAME_BOARD.draw_msg("YOU HAVE FOUND YOUR ONE TRUE LOVE!!!")
                
                for x in range (4):
                    clock.schedule_interval(create_love, .5)    #make heart every half second
                

                # heart = Obstacles()
                # heart.IMAGE = "Heart"
                # GAME_BOARD.register(heart)
                # GAME_BOARD.set_el(7,0, heart)
                # create_love()


def create_love():


    hearts = [(5,0)]#, (6,0), (7,0), (7,1)]

    for pos in hearts:

        # GAME_BOARD.del_el(pos[0],pos[1])

        heart = Obstacles()
        GAME_BOARD.register(heart)
        heart.IMAGE = "Heart"

        GAME_BOARD.set_el(pos[0], pos[1], heart)



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

