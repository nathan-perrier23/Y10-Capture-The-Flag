from queue import PriorityQueue
from errno import ENOTEMPTY
from socket import close
from turtle import distance, position, width
from GameFrame import BlueBot, Globals
from enum import Enum
import random

from GameFrame import Level, Globals, RedFlag, BlueFlag, TextObject
from Objects import DangerZone
from Objects import Red1, Red2, Red3, Red4, Red5
from Objects import Blue1, Blue2, Blue3, Blue4, Blue5
import math
import numpy as np
import pygame
WHITE =  (255,255,255)


class STATE(Enum):
    WAIT = 1
    ATTACK = 2
    JAIL_BREAK = 3
    



    





class Blue1(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(60, 100)
        self.wait_count = 0
        self.enemy_coords = (0,0)
        

    
    def tick(self):
        halfway = Globals.SCREEN_WIDTH / 2                  #halfway point of the arena
        dict, dict_positions = {}, {}                       #creates empty dictionaries
        dict_positions, active_bots,sorted_dist,sorted_bots,sorted_positions = self.sort(halfway,dict,dict_positions, Globals.red_flag, True)   #sorts the positions, distances and indentifiers in order of closest or furtherest
        if active_bots and (self.x < halfway):              #if there are active bot's and if my bot is less than halfway
            dict_positions, active_bots,sorted_dist,sorted_bots,sorted_positions = self.sort(halfway,dict,dict_positions, Globals.red_flag, True)   #sorts the positions, distances and indentifiers in order of closest or furthest
            close_coords = (sorted_positions[0][0], sorted_positions[0][1])     #set's the current location of the bot to a variable
            distance_traveled = self.point_to_point_distance(close_coords[0],close_coords[1], self.enemy_coords[0], self.enemy_coords[1])   #the distance the closest emeny traveled in a Tick
            speed = self.get_speed(distance_traveled)       #calculate the speed of the enemy
            my_x, my_y = self.x, self.y                     #set my bots x,y positions in a variable
            x4 = my_x + ((abs(my_x - close_coords[0]))/2)   #caculate x4 (setting it as halfway between the two bots)
            active = True 
        else:
            active = False
            sorted_bots,sorted_dist,sorted_positions, active_bots = self.sort(halfway,dict,dict_positions, self, active)    #sorts the positions, distances and indentifiers in order of closest or furtherest
        
        if self.wait_count < self.initial_wait:     #delays how long until the bot starts
            self.wait_count += 1
        else:
            if active == True:                      #if there are active bot's and if my bot is less than halfway
                if (self.x < (halfway - 80)):       #if the bot is less than halfway - 80 px
                    dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1], active)   #calculate the equations needed to get the intercept
                    if (dist_to_self == dist_to_enemy) or ((abs(dist_to_enemy - dist_to_self)) <= 45):  #if the distances are equal and it is an isoceles triangle then drive towards the intercept at the same speed of the bot
                        self.drive_to_enemy(speed,x4,y4)
                    else:
                        if y4 >= Globals.SCREEN_HEIGHT:         #if y4 is lager than the screen height set it to the max screen height and make distances equal
                            dist_to_self = dist_to_enemy
                            y4 = Globals.SCREEN_HEIGHT
                            self.drive_to_enemy(speed,x4,y4)
                        elif y4 <= 0:                           #if y4 is smaller than the screen height set it to the lowest screen height and make distances equal
                            dist_to_self = dist_to_enemy
                            y4 = 0
                            self.drive_to_enemy(speed,x4,y4)
                            
                        else:
                            if (dist_to_self > dist_to_enemy) and (abs(dist_to_enemy - dist_to_self) > 45):         #if it's not an isoceles 
                                x4 = my_x + ((abs(x4 - close_coords[0]))-(dist_to_self-dist_to_enemy))              # recalculate x4, moving it left
                                dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1], active) #recalculate equations now that x4 has been changed

                            elif (dist_to_enemy > dist_to_self) and (abs(dist_to_enemy - dist_to_self) > 45):       #if it's not an isoceles 
                                x4 = my_x + ((abs(x4 - close_coords[0]))+(dist_to_enemy-dist_to_self))              # recalculate x4, moving it right 
                                dist_to_self, dist_to_enemy,x4,y4 = self.calculate(x4,my_x,my_y,self.enemy_coords[0], self.enemy_coords[1], close_coords[0], close_coords[1], active) #recalculate equations now that x4 has been changed
                    
                            self.drive_to_enemy(speed,x4,y4)        #drive forward, towards the intercept, matching enemies speed
                
                else:       #if my bot is further than halfway - 80px turn back towards red flag
                    self.go_to_flag()
            else: 
                if sorted_dist[0] > 180:        #if the distance to the closest bot is more than 180
                    if self.has_flag:           #if the bot has the flag back to it's own half
                        self.turn_towards(0, self.y) 
                        self.drive_forward(Globals.FAST)
                    else:
                        self.drive_to_flag()    #drive to the blue flag

                else:
                    
                    if self.point_to_point_distance(Globals.blue_flag.x, Globals.blue_flag.y, self.x,self.y) > 180 and sorted_dist[0] < 180:  #if the distance between the bot and the blue flag is more than 180 and the closest bot is less than 180 away
                        self.turn_towards(-sorted_positions[0][0], -sorted_positions[0][1], Globals.FAST)   #go the opposite direction
                        self.drive_forward(Globals.FAST)
                    else:
                        self.drive_to_flag()                    #drive towards blue flag
                        if self.has_flag:                       #if bot has the flag 
                            self.turn_towards(0, self.y)        #go back to their half
                            self.drive_forward(Globals.FAST)
                            if sorted_dist[0] < 200:            #if bot is less than 200 away from the closest enemy
                                self.turn_towards(-sorted_positions[0][0], -sorted_positions[0][1], Globals.FAST)   #avoid enemy
                                self.drive_forward(Globals.FAST)
        if active == True:
            self.enemy_coords = (close_coords[0], close_coords[1])      #update enemy last coordinates with the current coordinates
                
    def drive_to_flag(self):
        self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)  #turn twoards blue flag
        self.drive_forward(Globals.FAST)       #drive fast

    def sort(self, halfway,dict,dict_positions, object, active):
        
        for enemy in Globals.red_bots:                  #for each enemy in red bots
            enemy_distance = self.point_to_point_distance(object.x,object.y, enemy.x, enemy.y)  #get the distance between the object and the enemy
            dict[enemy] = enemy_distance                # put the enemy's indentifier and the distance into dict
            dict_positions[enemy] = [enemy.x,enemy.y]   # put the enemy's indentifier and it's position into dict_positions
        
        dict = {key: val for key, val in sorted(dict.items(), key = lambda ele: ele[1])}                        #sort dict values from lease to most
        dict_positions = {key: val for key, val in sorted(dict_positions.items(), key = lambda ele: ele[1])}    #sort dict_position values from least to most
        
        sorted_bots = list(dict.keys())  #put the values and keys into lists
        sorted_dist = list(dict.values())
        sorted_positions = list(dict_positions.values())
        
            
        
        if active == False:         #if there are active bot's and if my bot is less than halfway
            active_bots = {}        #return an epemty dictionary
            return sorted_bots,sorted_dist,sorted_positions, active_bots
        else:
            i = 0
            active_bots = {}                    #create an empt dictionary
            while i < len(dict.keys()):         #for every element in the dictionary
                if sorted_positions[i][0] < halfway:    #if the current bots (bot[i]) x value is less than halfway
                    active_bots[sorted_dist[i]] = [sorted_positions[i][0],sorted_positions[i][1]]   #add the distance of that bot and it's position to the active_bots dictionary
                i = i + 1 
            
            sorted_bots = list(dict.keys()) #put the values and keys into lists
            sorted_dist = list(dict.values())
            sorted_positions = list(dict_positions.values())
            
            return dict_positions, active_bots,sorted_dist,sorted_bots,sorted_positions
        
        
    def go_to_flag(self):
        self.turn_towards(Globals.red_flag.x,Globals.red_flag.y, Globals.FAST) #turn towards the red flag
        self.drive_forward(Globals.FAST)    #drive fast
        
        
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
        if speed == 1:  #matches the speed
            self.drive_forward(Globals.SLOW) 
        elif speed == 2:
            self.drive_forward(Globals.MEDIUM)
        else:
            self.drive_forward(Globals.FAST)

    
        
        
    
    def gradient(self,x1,y1,x2,y2, active):
        if active == True:
            try:
                gradient = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else 0
                # gradient = (y2 - y1) / (x2 - x1)  #calculates the gradient of two points
            except ZeroDivisionError:
                gradient = math.inf
        else:
            gradient = math.inf
        return gradient
    
    def calculate(self,x4, my_x,my_y, last_sorted_positions_x, last_sorted_positions_y,sorted_positions_x,sorted_positions_y, active):
        m = self.gradient(last_sorted_positions_x,last_sorted_positions_y,sorted_positions_x,sorted_positions_y, active) #get's the gradient
        c = sorted_positions_y - m*sorted_positions_x #rearranges y=mx+c to get c
        y4 = abs(m*x4 + c) #get the y4 value by substituting x4 into y=mx+c
        dist_to_self = self.point_to_point_distance(my_x,my_y,x4,y4) #get's the distance between self and intercept
        dist_to_enemy = self.point_to_point_distance(sorted_positions_x,sorted_positions_y,x4,y4) #get's the distance between enemy and intercept
        return dist_to_self,dist_to_enemy,x4,y4
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # halfway = Globals.SCREEN_WIDTH/2
        # dict = {}
        # dict_positions = {}
        # active_bots,sorted_dist,sorted_bots,sorted_positions = self.sort(halfway,dict,dict_positions)
        
        # dict_path = {}
        
        # grid = self.makeGrid()
        # weights = self.weighted_nodes(grid)
        # end = self.get_start_and_end(grid, Globals.blue_flag)
        # start = self.get_start_and_end(grid, self)
        # blocked = self.enemy_in_path(grid,active_bots)
        # dict_path = self.get_path(grid,end,start,weights,active_bots, blocked, dict_path)
        
        # self.drive_forward(Globals.SLOW)
            
            
    # def get_path(self,grid,end,start,weights,active_bots, blocked,dict_path):
    #     weight_pos = list(weights.keys())
    #     weight_dist = list(weights.values())
    #     dict_temp = {}
    #     if start == end:
    #         # self.drive_backward()
    #         print(len(grid))
    #         print("START: ", start, "END: ", end)
    #         print("---------------------- YAY!!! ---------------------")
    #         return dict_path
    #     else:
    #         if end in blocked and ((abs(start[0] - end[0]) <= 120) and (abs(start[1] - end[1]) <= 120)):
    #             print(len(grid))
    #             print("START: ", start, "END: ", end)
    #             print("---------------------- YAY!!! ---------------------") 
    #             return dict_path
    #         else:
    #             find = True
    #             while find == True:
    #                 i,j=0,0
    #                 while i <= len(weights):
    #                     if start == end or (end in blocked and ((abs(start[0] - end[0]) <= 120) and (abs(start[1] - end[1]) <= 120))):
    #                         find = False
    #                         break
    #                     else:
    #                         if (start[0] == (weight_pos[i][0])) and (start[1] == (weight_pos[i][1])): #works
    #                             x=0
    #                             while x <= len(weights):
    #                                 if (((weight_pos[i][0] + 40) == weight_pos[x][0]) and ((weight_pos[i][1] + 40) == weight_pos[x][1]) or ((weight_pos[i][0] + 40) == weight_pos[x][0]) and ((weight_pos[i][1]) == weight_pos[x][1]) or ((weight_pos[i][0] + 40) == weight_pos[x][0]) and ((weight_pos[i][1] - 40) == weight_pos[x][1]) or ((weight_pos[i][0]) == weight_pos[x][0]) and ((weight_pos[i][1] - 40) == weight_pos[x][1]) or ((weight_pos[i][0] - 40) == weight_pos[x][0]) and ((weight_pos[i][1] - 40) == weight_pos[x][1]) or ((weight_pos[i][0] - 40) == weight_pos[x][0]) and ((weight_pos[i][1]) == weight_pos[x][1]) or ((weight_pos[i][0] - 40) == weight_pos[x][0]) and ((weight_pos[i][1] + 40) == weight_pos[x][1]) or ((weight_pos[i][0]) == weight_pos[x][0]) and ((weight_pos[i][1] + 40) == weight_pos[x][1])):
    #                                     temp = list([weight_pos[x][0],weight_pos[x][1]])
    #                                     j = j + 1
    #                                     print(j)
    #                                     if temp not in blocked: #test
    #                                         print("not blocked")
    #                                         dict_temp[weight_dist[x]] = (temp) #test
    #                                     if j == 8: #test
    #                                         dict = {key: val for key, val in sorted(dict_temp.items(), key = lambda ele: ele[0])}
    #                                         print(dict)
    #                                         weighted_pos = list(dict.values())
    #                                         weighted_dist = list(dict.keys())
    #                                         start = [weighted_pos[0][0], weighted_pos[0][1]]
    #                                         dict_path[weighted_dist[0]] = [weighted_pos[0][0], weighted_pos[0][1]]
    #                                         print(dict_path)
    #                                         print("START: ", start, "END: ", end)
    #                                         self.get_path(grid,end,start,weights,active_bots, blocked,dict_path)
    #                                         find = False
    #                                         break
    #                                 x=x+1             
    #                         i=i+1
            
            
       
                
    # def enemy_in_path(self,grid,active_bots):
    #     blocked = []
    #     enemy_bots = active_bots.keys()
    #     for enemys in enemy_bots:
    #         enemy_node = self.get_start_and_end(grid,enemys)
    #         blocked.append(enemy_node)
    #         enemy_node_x = enemy_node[0]
    #         enemy_node_y = enemy_node[1]
            
    #         i = 0

    #         while i < 3:  #get's two layers from enemy
    #             new_x_node = enemy_node_x - (40 + (40*(i)))
    #             new_y_node = enemy_node_y - (40 + (40*(i)))
    #             new_x_node_2 = enemy_node_x + (40 + (40*(i)))
    #             new_y_node_2 = enemy_node_y + (40 + (40*(i)))
    #             blocked.append([new_x_node,new_y_node])
    #             blocked.append([new_x_node,enemy_node_y])
    #             blocked.append([enemy_node_x,new_y_node])
    #             blocked.append([new_x_node_2,new_y_node_2])
    #             blocked.append([new_x_node_2,enemy_node_y])
    #             blocked.append([enemy_node_x,new_y_node_2])
    #             blocked.append([new_x_node_2,new_y_node])
    #             blocked.append([new_x_node,new_y_node_2])
    #             i=i+1
                
    #     return blocked
                
            
                
            
            
    # def get_start_and_end(self,grid, object): #could make modular
    #     i = 0
    #     y = 0
    #     object_grid_pos = []
    #     while i < len(grid):
    #         grid_x_midpoint = grid[i][0] + 20
    #         grid_y_midpoint = grid[i][1] + 20
    #         if (abs(object.x - grid_x_midpoint) <= 20) and (abs(object.y - grid_y_midpoint) <= 20): #test
    #             object_grid_pos = list([grid_x_midpoint,grid_y_midpoint])
                            
    #         i=i+1
    #     # if len(object_grid_pos) == 2: #should work
    #     #     if object_grid_pos[0][0] != object_grid_pos[1][0]:
    #     #         final_object_grid_pos_x = object_grid_pos[0][0] + ((abs(object_grid_pos[1][0]-object_grid_pos[0][0]))/2)
    #     #     else:
    #     #         final_object_grid_pos_x = object_grid_pos[0][0]
    #     #     if object_grid_pos[0][1] != object_grid_pos[1][1]:
    #     #         final_object_grid_pos_y = object_grid_pos[0][1] + ((abs(object_grid_pos[1][1]-object_grid_pos[0][1]))/2)
    #     #     else:
    #     #         final_object_grid_pos_y = object_grid_pos[0][1]
    #     #     object_grid_pos = []
    #     #     object_grid_pos.append([final_object_grid_pos_x,final_object_grid_pos_y])
            
        
    #     # if len(object_grid_pos) > 1: #not the most accurate
    #     #     final_object_grid_pos_x = object_grid_pos[0][0]
    #     #     final_object_grid_pos_y = object_grid_pos[0][1]
    #     #     object_grid_pos = []
    #     #     temp = list(final_object_grid_pos_x,final_object_grid_pos_y)
    #     #     object_grid_pos.append(temp)
    #         # print("object_x: ", object.x, "object_y: ", object.y, "new object grid pos x: ", object_grid_pos[0][0], "new object grid pos y: ", object_grid_pos[0][1])

    #     return object_grid_pos        
        
    
    # def weighted_nodes(self, grid):
    #     i = 0
    #     weights = {}
    #     while i < len(grid):
    #         grid_x_midpoint = grid[i][0] + 20
    #         grid_y_midpoint = grid[i][1] + 20
    #         dist_to_flag = self.point_to_point_distance(grid_x_midpoint,grid_y_midpoint,Globals.blue_flag.x,Globals.blue_flag.y)
    #         weights[grid_x_midpoint,grid_y_midpoint] = dist_to_flag #sorted?
    #         i = i + 1
    #     return weights
                    

    # def makeGrid(self):
    #     grid = []
    #     blockSize = 40
    #     for y in range(0, Globals.SCREEN_HEIGHT, blockSize):
    #         for x in range(0, Globals.SCREEN_WIDTH, blockSize):
    #             node = pygame.Rect(x, y, blockSize, blockSize)
    #             node = list(node)
    #             grid.append(node)
    #     return grid


    # def sort(self, halfway,dict,dict_positions):
    #     for enemy in Globals.red_bots:
    #         enemy_distance = self.point_to_point_distance(self.x,self.y, enemy.x,enemy.y)
    #         dict[enemy] = enemy_distance 
    #         dict_positions[enemy] = [enemy.x,enemy.y]

    #     print("----      NEW TICK       ----", end="\n")
    #     print("given dist: \n", str(dict.values()),end="\n")
    #     print("old dict postions: ", dict_positions.values(), end="\n")
        
    #     dict = {key: val for key, val in sorted(dict.items(), key = lambda ele: ele[1])}
    #     dict_positions = {key: val for key, val in sorted(dict_positions.items(), key = lambda ele: ele[1])}

    #     sorted_bots = list(dict.keys())  #not needed once print statements are gone
    #     sorted_dist = list(dict.values())
    #     sorted_positions = list(dict_positions.values())
        
    #     print("sorted dist: \n", sorted_dist,end="\n")
    #     print("sorted postions: \n", sorted_positions, end="\n")
    #     print("closest postion_x: \n", sorted_positions[0][0], end="\n")
        
    #     i = 0
    #     active_bots = {}

    #     while i < len(dict.keys()):  
    #         if sorted_positions[i][0] > halfway:  
    #             print(sorted_bots[i], " --   ACTIVE   -- ", "position_x: ", sorted_positions[i][0], " position_y: ", sorted_positions[i][1], end="\n")
    #             active_bots[sorted_bots[i]] = [sorted_positions[i][0],sorted_positions[i][1]] 
    #         else:
    #             print(sorted_bots[i], " --  DISABLED  -- ", "position_x: ", sorted_positions[i][0], " position_y: ", sorted_positions[i][1], end="\n")
    #         i = i + 1
        
    #     sorted_positions = list(active_bots.values())  
        
    #     print("closest active postion_x: \n", sorted_positions[0][0], end="\n")
    #     print("active bots: \n", active_bots, end="\n")
        
    #     return active_bots,sorted_dist,sorted_bots,sorted_positions
           
           
 
       
       
            
    
                
 
        
        
        
        

    # def make_grid(self,rows, width):
    #     grid = []
    #     gap = width // rows
    #     for i in range(rows):
    #         grid.append([])
    #         for j in range(rows):
    #             spot = list(i, j, gap, rows)
    #             grid[i].append(spot)

    #     return grid          
                
    # def reconstruct_path(self,came_from, current, draw):
    #     while current in came_from:
    #         current = came_from[current]
    #         current.make_path()
    #         draw()
            
    # def h(self,p1, p2):
    #     x1, y1 = p1
    #     x2, y2 = p2
    #     return abs(x1-x2) + abs(y1-y2)
        
    # def algorithm(self,draw, grid, start, end):
    #     count = 0
    #     open_set = PriorityQueue()   # returns the smallest value in the list
    #     open_set.put((0, count, start))
    #     came_from = {}
    #     g_score = {spot: float("inf") for row in grid for spot in row}
    #     g_score[start] = 0
    #     f_score = {spot: float("inf") for row in grid for spot in row}
    #     f_score[start] = self.h(start.get_pos(), end.get_pos())

    #     open_set_hash = {start}
    #     while not open_set.empty():
    #         for event in pygame.event.get():
    #             if event.type ==pygame.QUIT:
    #                 pygame.quit()
    #         current = open_set.get()[2]      # returns the best value
    #         open_set_hash.remove(current)
    #         if current == end:
    #             self.reconstruct_path(came_from, end, draw)
    #             end.make_end()
    #             start.make_start()
    #             return True

    #         for neighbour in current.neighbours:
    #             temp_g_score = g_score[current]+1

    #             if temp_g_score < g_score[neighbour]:
    #                 came_from[neighbour] = current
    #                 g_score[neighbour] = temp_g_score
    #                 f_score[neighbour] = temp_g_score + self.h(neighbour.get_pos(), end.get_pos())
    #                 if neighbour not in open_set_hash:
    #                     count += 1
    #                     open_set.put((f_score[neighbour], count, neighbour))
    #                     open_set_hash.add(neighbour)
    #                     neighbour.make_open()
    #         draw()
    #         if current != start:
    #             current.make_closed()

    #     return False              


