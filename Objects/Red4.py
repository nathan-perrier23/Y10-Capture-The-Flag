from GameFrame import RedBot, Globals
from enum import Enum
import random
import time
import math 

class STATE(Enum):
    WAIT = 1
    ATTACK = 2


class Red4(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(60, 100)
        self.wait_count = 0
        self.enemy_coords = (0,0)

    def tick(self):
        red_flag = Globals.red_flag
        closest, dist = self.closest_to_me()
        halfway = Globals.SCREEN_WIDTH / 2
        if self.wait_count < self.initial_wait:
            self.wait_count += 1
        else:
                
            if dist > 180:
                if self.has_flag:
                    self.turn_towards(Globals.blue_flag.x,Globals.blue_flag.y,Globals.FAST)
                    self.drive_forward(Globals.FAST)
                else:
                    self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
                    self.drive_forward(Globals.MEDIUM)
                closest, dist = self.closest_to_me()
            else:
                if self.x > halfway + 80:
                    self.turn_towards(closest.x, closest.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                    closest, dist = self.closest_to_me()
                else:
                    if self.point_to_point_distance(Globals.red_flag.x, Globals.red_flag.y, self.x,self.y) > 180:  #messs around with it
                        self.turn_towards(-closest.x, -closest.y, Globals.FAST)
                        self.drive_forward(Globals.FAST)
                        closest, dist = self.closest_to_me()
                    else:
                        self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
                        self.drive_forward(Globals.MEDIUM)
                        if self.has_flag:
                            self.turn_towards(0, self.y)
                            self.drive_forward(Globals.FAST)
                            if dist < 200:
                                self.turn_towards(-closest.x, -closest.y, Globals.FAST)
                                self.drive_forward(Globals.FAST)
                        closest, dist = self.closest_to_me()
                
    

    def closest_to_me(self):   
        closest = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest.x,closest.y,self.x,self.y)
        for enemy in Globals.blue_bots:
            if self.point_to_point_distance(enemy.x,enemy.y,self.x,self.y) < shortest_distance: 
                closest = enemy
                shortest_distance = self.point_to_point_distance(enemy.x,enemy.y,self.x,self.y)
        return closest , shortest_distance