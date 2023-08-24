from ast import Global
from calendar import c
import dis
from pickle import FALSE, TRUE
from GameFrame import BlueBot, Globals
from enum import Enum
import datetime
import math


class STATE(Enum):
    WAIT = 1
    ATTACK = 2


class Blue2(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.stuck = False
        self.enemy_coords = (0,0)
    
    def tick(self):
        halfway = Globals.SCREEN_WIDTH/2  #halfway 
        dict, dict_positions = {}, {}
        dict_positions, active_bots,sorted_dist,sorted_bots,sorted_positions = self.sort(halfway,dict,dict_positions, Globals.red_flag)  #sorts the enemies distance and position from shortest to furtherest
        if active_bots: #if there are active bot's
            close_coords = (sorted_positions[0][0], sorted_positions[0][1]) 
            distance_traveled = self.point_to_point_distance(close_coords[0],close_coords[1], self.enemy_coords[0], self.enemy_coords[1]) #the distance the closest emeny traveled in a Tick
            speed = self.get_speed(distance_traveled) #calculate the speed of the enemy
            my_x, my_y = self.x, self.y #set my bots x,y positions in a variable
            x4 = my_x + ((abs(my_x - close_coords[0]))/2) #caculate x4 (setting it as halfway between the two bots)
            active = True   
        else:
            active = False   

        if active == True: 
            if (self.x < (halfway - 80)): 
                dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1]) #calculate the equations needed to get the intercept
                if (dist_to_self == dist_to_enemy) or ((abs(dist_to_enemy - dist_to_self)) <= 45): #if the distances are equal and it is an isoceles triangle then drive towards the intercept at the same speed of the bot
                    self.drive_to_enemy(speed,x4,y4)
                else:
                    if y4 >= Globals.SCREEN_HEIGHT: #if y4 is lager than the screen height set it to the max screen height and make distances equal
                        dist_to_self = dist_to_enemy
                        y4 = Globals.SCREEN_HEIGHT
                        self.drive_to_enemy(speed,x4,y4)
                    elif y4 <= 0:                   #if y4 is smaller than the screen height set it to the lowest screen height and make distances equal
                        dist_to_self = dist_to_enemy
                        y4 = 0
                        self.drive_to_enemy(speed,x4,y4)
                        
                    else:
                        if (dist_to_self > dist_to_enemy) and (abs(dist_to_enemy - dist_to_self) > 45): #if it's not an isoceles 
                            x4 = my_x + ((abs(x4 - close_coords[0]))-(dist_to_self-dist_to_enemy)) # recalculate x4, moving it left
                            dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1]) #recalculate equations now that x4 has been changed

                        elif (dist_to_enemy > dist_to_self) and (abs(dist_to_enemy - dist_to_self) > 45):
                            x4 = my_x + ((abs(x4 - close_coords[0]))+(dist_to_enemy-dist_to_self)) # recalculate x4, moving it right 
                            dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1]) #recalculate equations now that x4 has been changed
                
                        self.drive_to_enemy(speed,x4,y4) #drive forward, towards the intercept, matching enemies speed
            
            else:   #if my bot is further than halfway - 80px turn back towards red flag
                self.go_to_flag()
                
        else:
            if self.point_to_point_distance(Globals.red_flag.x,Globals.red_flag.y,self.x,self.y) > 50:  #if there are no active bots, turn back towards red flag, and circle it
                self.go_to_flag()
            else:
                self.turn_towards(Globals.red_flag.x, Globals.red_flag.y, Globals.MEDIUM)
                self.drive_forward(Globals.SLOW)

        if active == True:
            self.enemy_coords = (close_coords[0], close_coords[1])  #set the last coordinates of the enemy to the curRent coordinates


    def go_to_flag(self):
        self.turn_towards(Globals.red_flag.x,Globals.red_flag.y, Globals.FAST)
        self.drive_forward(Globals.FAST)
        
        
    def get_speed(self, distance):
        speed = distance  #the distance between two points corrolates with the speed of the bot
        if speed <= 3: #if speed is less than or equal to 3 then the bot is going slow
            return 1 
        elif speed > 3 and speed <= 7: #if speed is more than 3 but less than or equal to 7 then the bot is going medium speed
            return 2
        elif speed > 7: #if speed is more than 7 then the bot is going fast
            return 3
    
    def drive_to_enemy(self,speed,x4,y4):
        self.turn_towards(x4,y4, Globals.FAST)   #turn towards the intercept point
        if speed == 1:  #matches the speed of the bot
            self.drive_forward(Globals.SLOW) 
        elif speed == 2:
            self.drive_forward(Globals.MEDIUM)
        else:
            self.drive_forward(Globals.FAST)

    def sort(self, halfway,dict,dict_positions, object1):
        for enemy in Globals.red_bots:
            enemy_distance = self.point_to_point_distance(object1.x,object1.y, enemy.x,enemy.y)
            dict[enemy] = enemy_distance 
            dict_positions[enemy] = [enemy.x,enemy.y]
        
        dict = {key: val for key, val in sorted(dict.items(), key = lambda ele: ele[1])}
        dict_positions = {key: val for key, val in sorted(dict_positions.items(), key = lambda ele: ele[1])}

        sorted_bots = list(dict.keys())  #not needed once print statements are gone
        sorted_dist = list(dict.values())
        sorted_positions = list(dict_positions.values())
        
        i = 0
        
        active_bots = {}
        while i < len(dict.keys()):  
            if sorted_positions[i][0] < halfway + 105: #less than half way  
                active_bots[sorted_dist[i]] = [sorted_positions[i][0],sorted_positions[i][1]]   
            i = i + 1  
            
        sorted_dist = list(active_bots.keys()) 
        sorted_positions = list(active_bots.values()) 
        
        return dict_positions, active_bots,sorted_dist,sorted_bots,sorted_positions
    
    def gradient(self,x1,y1,x2,y2):
        try:
            gradient = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0   #calculates the gradient of two points if it doesn't == 0, else it set's the gradient as 0
        except ZeroDivisionError:   #if an error occurs due to division by zero then return infinite
            gradient = math.inf
        return gradient
    
    def calculate(self,x4, my_x,my_y, last_sorted_positions_x, last_sorted_positions_y,sorted_positions_x,sorted_positions_y):
        m = self.gradient(last_sorted_positions_x,last_sorted_positions_y,sorted_positions_x,sorted_positions_y) #get's the gradient
        c = sorted_positions_y - m*sorted_positions_x #rearranges y=mx+c to get c
        y4 = abs(m*x4 + c) #get the y4 value by substituting x4 into y=mx+c
        dist_to_self = self.point_to_point_distance(my_x,my_y,x4,y4) #get's the distance between self and intercept
        dist_to_enemy = self.point_to_point_distance(sorted_positions_x,sorted_positions_y,x4,y4) #get's the distance between enemy and intercept
        return dist_to_self,dist_to_enemy,x4,y4
        
            
            