from GameFrame import RedBot, Globals
from enum import Enum
import time

class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3


class Red5(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)

        self.stuck = False

    def tick(self):
        help_flag = 0
        closest, dist = self.closest_to_me()
        halfway = Globals.SCREEN_WIDTH / 2
        blue_flag = Globals.blue_flag
        for enemy in Globals.red_bots:
            if enemy.has_flag:
                help_flag = help_flag + 1     
        if (Globals.blue_bots[1].jailed) or (help_flag >= 1):
            closest = self.closest_enemy_to_flag()
            closest2, distance = self.closest_to_me()
            blue_flag = Globals.blue_flag
            halfway = Globals.SCREEN_WIDTH / 2
            if self.point_to_point_distance(Globals.SCREEN_WIDTH,32,self.x,self.y) > halfway:
                self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
                self.drive_forward(Globals.FAST)
            else:
                    
                for bot in Globals.blue_bots:
                    if bot.has_flag and bot is not self:
                        self.turn_towards(bot.x, bot.y, Globals.FAST)
                        self.drive_forward(Globals.FAST) 
                        
                if distance > halfway + 40:
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
        else:

            if dist > 180:
                if self.has_flag:
                    self.turn_towards(Globals.SCREEN_WIDTH, self.y)
                    self.drive_forward(Globals.FAST)
                else:
                    self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                closest, dist = self.closest_to_me()
            else:
                if self.x > halfway + 70:
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
                        self.drive_forward(Globals.FAST)
                        if self.has_flag:
                            self.turn_towards(0, self.y)
                            self.drive_forward(Globals.FAST)
                            if dist < 200:
                                self.turn_towards(-closest.x, -closest.y, Globals.FAST)
                                self.drive_forward(Globals.FAST)
                        closest, dist = self.closest_to_me()
                                    
        
               
    def closest_to_me(self):   
        closest1 = Globals.blue_bots[0]
        shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        for enemy in Globals.blue_bots:
            if self.point_to_point_distance(enemy.x,enemy.y,self.x,self.y) < shortest_distance: 
                closest1 = enemy
                shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        return closest1, shortest_distance

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

