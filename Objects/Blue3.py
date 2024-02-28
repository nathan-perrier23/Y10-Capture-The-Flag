from ast import Global
from statistics import median
from turtle import speed
from GameFrame import BlueBot, Globals
import random

from Objects.Blue2 import Blue2


class Blue3(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(30, 90)
        self.wait_count = 0
        self.stuck = False

    def tick(self):
        stuck = self.is_self_stuck()        #checks to see if the bot is stuck
        closest, distance_to_flag = self.closest_to(Globals.red_bots, Globals.red_flag)     #get's the closest bot to the flag
        closest_to_self, distance = self.closest_to(Globals.red_bots, self)     #get's the closest bot to self
        red_flag = Globals.red_flag         #set's the red flag as a variable
        halfway = Globals.SCREEN_WIDTH / 2  #sets hafway as half of screen width
        if self.point_to_point_distance(0,Globals.SCREEN_HEIGHT/2,self.x,self.y) > halfway - 90:   #if the bot is further than halfway
            self.go_to_red_flag()   #turn back towards the red flag
        else:
            for friend in Globals.blue_bots: #for ever blue bot
                if friend.jailed:            #if the a blue bot is jailed
                    self.go_to_jail(friend)  #go to jail

            # if stuck == True:
            #     self.turn_left()    #if stuck turn left
                
            for bot in Globals.red_bots:                            #for every red bots
                if bot.has_flag and bot is not self:                #if bot has flag
                    self.turn_towards(bot.x, bot.y, Globals.FAST)   #turn towards the bot
                    self.drive_forward(Globals.FAST)                #drive forward
                    
            if distance < halfway - 90:                             #if the closest enemy bot is less than halfway then go to bot
                self.turn_towards(closest.x, closest.y, Globals.FAST)
                self.drive_forward(Globals.FAST)  
            else:
                if self.point_to_point_distance(red_flag.x,red_flag.y,self.x,self.y) > 50:      #if distance to flag is more than 50 then go to flag
                    self.go_to_red_flag()
                else:
                    self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.MEDIUM)   #else slowly circle flag
                    self.drive_forward(Globals.SLOW)

    def go_to_jail(self,friend):
        stuck = self.is_self_stuck()        #check to see if bot is stuck
        if stuck == True:                   # if bot is stuck
            self.turn_towards(friend.x,friend.y, Globals.FAST)  #turn towards friend
        elif self.x <= 20 and (self.angle >= 80 and self.angle <= 100): #if the bot is stuck on wall with the lowest x axis 
            self.turn_towards(friend.x, 0, Globals.FAST)    #turn towards friend.x and o
        elif self.y <= 20 and ((self.angle <= 10 and self.angle >= 350) or self.angle < 0): #if the bot is stuck on wall with the lowest y axis 
            self.turn_towards(0, friend.y, Globals.FAST)    #turn towards 0, friend y
        else:
            self.turn_towards(friend.x,friend.y, Globals.FAST) #if the bot is not stuck then slowly navigate to the friend in jail
            self.drive_forward(Globals.SLOW)
            
    def go_to_red_flag(self):
        self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.FAST) #turn to red flag
        self.drive_forward(Globals.FAST) #drive fast
           
    def closest_to(self, object, target):   
        closest = object[0] #set closest to the first object
        shortest_distance = self.point_to_point_distance(closest.x,closest.y,target.x,target.y) #get the distance between the object and the target
        for objects in object: #for every object
            if self.point_to_point_distance(objects.x,objects.y,target.x,target.y) < shortest_distance: #if the distacne between the new object and the target is less
                closest = objects #set closest to the current object
                shortest_distance = self.point_to_point_distance(closest.x,closest.y,target.x,target.y) #set the distance to the distance between the new object and the target
        return closest, shortest_distance

    def is_self_stuck(self):
        if not self.jailed:                                     #if the bot is not jailed
            if self.x <= self.width:                            #if the bot's x value is less than it's width then it is stuck
                return True
            elif self.x >= Globals.SCREEN_WIDTH - self.width:   #if the bot's x value is more than screen width - the bots width then it is stuck
                return True
            if self.y <= self.width:                            #if the bot's y value is less than it's height then it is stuck
                return True
            elif self.y >= Globals.SCREEN_HEIGHT - self.height: #if the bot's y value is more than screen height - the bots height then it is stuck
                return True
            else:
                return False                                    #else the bot is not jailed

   
    # def closest_friend_to_jail(self):
    #     # set default bot for comparison
    #     closest = Globals.blue_bots[0]
    #     # set flag
    #     jail_x = 0
    #     jail_y = 0
    #     # set default distance
        
    #     dist = self.point_to_point_distance(self.x, self.y, jail_x, jail_y)

    #     for friends in Globals.blue_bots:
    #         if (friends == Globals.blue_bots[1]) or (friends == Globals.blue_bots[2]):
    #             # checks if any are closer
    #             if self.point_to_point_distance(friends.x, friends.y, jail_x, jail_y) < dist:
    #                 # reallocates the closest bot and the distance
    #                 closest = friends
    #                 dist = dist = self.point_to_point_distance(closest.x, closest.y, jail_x, jail_y)

    #     return dist
                
            
            
    
