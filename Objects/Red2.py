from ctypes import pointer
import re
from GameFrame import RedBot, Globals
import random
from Rooms import Arena
import time
import math

class Red2(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.stuck = False
        self.enemy_coords = (0,0)
        
        

    def tick(self):  
        if Globals.red_bots[0].jailed and Globals.red_bots[2].jailed:
            for friend in Globals.red_bots:
                self.turn_towards(friend.x,friend.y,self.x,self.y)
                self.drive_forward(Globals.SLOW)
        for enemy in Globals.blue_bots:
            if enemy.has_flag:
                self.turn_towards(enemy.x, Globals.blue_flag.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
        if self.point_to_point_distance(Globals.blue_flag.x, Globals.blue_flag.y, self.x, self.y) > 8:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.MEDIUM)
            
            
            
            
        # Red defending against blue
        # closest, dist = self.closest_enemy_to_flag()
        # halfway = Globals.SCREEN_WIDTH / 2
        # for enemy in Globals.blue_bots:
        #     if enemy.x > halfway and enemy == closest:
        #         self.turn_towards(enemy.x, enemy.y, Globals.FAST)
        #         self.drive_forward(Globals.FAST)
        # if self.point_to_point_distance(Globals.blue_flag.x, Globals.blue_flag.y,self.x,self.y) > 50:
        #     self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
        #     self.drive_forward(Globals.FAST)
        # else:
        #     self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.MEDIUM)
        #     self.drive_forward(Globals.SLOW)
        #     closest, dist = self.closest_enemy_to_flag()


    def closest_enemy_to_flag(self):
        # set default bot for comparison
        closest = Globals.blue_bots[0]
        # set flag
        flag = Globals.blue_flag
        # set default distance
        dist = self.point_to_point_distance(closest.x,closest.y,flag.x,flag.y)

        for enemy in Globals.blue_bots:
            # checks if any are closer
            if self.point_to_point_distance(enemy.x,enemy.y,flag.x,flag.y) < dist:
                # reallocates the closest bot and the distance
                closest = enemy
                dist = dist = self.point_to_point_distance(closest.x,closest.y,flag.x,flag.y)
        return closest, dist