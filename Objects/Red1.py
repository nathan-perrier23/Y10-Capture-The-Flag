from pickle import GLOBAL
from GameFrame import RedBot, Globals
import random
import time
import math

class Red1(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(60, 100)
        self.wait_count = 0
        self.enemy_coords = (0,0)

    def tick(self): 
        closest = self.closest_enemy_to_flag()
        distance = self.closest_to_me()
        blue_flag = Globals.blue_flag
        halfway = Globals.SCREEN_WIDTH / 2
        if self.point_to_point_distance(Globals.SCREEN_WIDTH,32,self.x,self.y) > halfway:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:
            for friend in Globals.red_bots:
                if friend.jailed:
                    self.turn_towards(friend.x, friend.y, Globals.FAST)
                    self.drive_forward(Globals.SLOW)
                
            for bot in Globals.blue_bots:
                if bot.has_flag and bot is not self:
                    self.turn_towards(bot.x, bot.y, Globals.FAST)
                    self.drive_forward(Globals.FAST) 
                    
            if distance < halfway - 200:
                self.turn_towards(closest.x, closest.y, Globals.FAST)
                self.drive_forward(Globals.FAST)  
            else:
                if self.point_to_point_distance(blue_flag.x,blue_flag.y,self.x,self.y) > 50:
                    self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                else:
                    self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.MEDIUM)
                    self.drive_forward(Globals.SLOW)
                    closest = self.closest_enemy_to_flag()
                    distance = self.closest_to_me()


        
    def closest_to_me(self):   
        closest1 = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        for enemy in Globals.blue_bots:
            if self.point_to_point_distance(enemy.x,enemy.y,self.x,self.y) < shortest_distance: 
                closest1 = enemy
                shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        return shortest_distance

    def closest_enemy_to_flag(self):
        # set default bot for comparison
        closest2 = Globals.blue_bots[0]
        # set flag
        flag = Globals.blue_flag
        # set default distance
        dist = self.point_to_point_distance(closest2.x,closest2.y,flag.x,flag.y)

        for enemy in Globals.blue_bots:
            # checks if any are closer
            if self.point_to_point_distance(enemy.x,enemy.y,flag.x,flag.y) < dist:
                # reallocates the closest bot and the distance
                closest2 = enemy
                dist = dist = self.point_to_point_distance(closest2.x,closest2.y,flag.x,flag.y)

        return closest2