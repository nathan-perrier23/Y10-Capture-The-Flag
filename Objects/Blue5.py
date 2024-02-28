from GameFrame import BlueBot, Globals
import random


class Blue5(BlueBot):
    def __init__(self, room, x, y):
        BlueBot.__init__(self, room, x, y)
        self.stuck = False


    def tick(self):  
        halfway = Globals.SCREEN_WIDTH / 2          #sets hafway as half of screen width
        red_flag = Globals.red_flag                 #set's the red flag as a variable 
        dist_to_flag = self.dist_to_enemy_flag()    # get's the distance of the closest enemy to flag
        stuck = self.is_self_stuck()                #checks to see if the bot is stuck
        
        # if stuck == True:   #if the bot is stuck then turn left
        #     self.turn_left()

        for bot in Globals.red_bots:    #for every red bot
            if bot.has_flag and bot is not self:    #if bot has flag
                self.turn_towards(bot.x, bot.y, Globals.FAST) #go towards bot
                self.drive_forward(Globals.FAST) 
                    
        if (Globals.blue_bots[2].jailed) and dist_to_flag > 225:    #if blue 3 is in jail and the bots distance to the flag is more than 225
                
            for friend in Globals.blue_bots: #for every blue bot
                if friend.jailed:       #if bot is jailed
                    self.go_to_jail(friend) #go to jail
                                
        else: 
            blue_flag = Globals.blue_flag   #set the blue flag to a variable
            closest, dist = self.closest_to_me()    #get the distance and identifier of the closest bot to the bot
            if dist > 180:      #if distance to the bot is more than 18-
                if self.has_flag:   #if the bot has the flag
                    self.turn_towards(0, self.y)    #turn back towards the blue side
                    self.drive_forward(Globals.FAST)    
                else: #if the bot doesn't have the flag then turn towards the blue flag
                    self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)  
                    self.drive_forward(Globals.FAST)
            else:
                if (self.x < halfway - 100) and (closest.x < halfway):  #if the bot is less than halfway then go towards the cloeset bot
                    self.turn_towards(closest.x, closest.y, Globals.FAST)
                    self.drive_forward(Globals.FAST)
                else:
                    if self.point_to_point_distance(Globals.blue_flag.x, Globals.blue_flag.y, self.x,self.y) > 180:  #if the diance between the blue flag and the bot is more than 180 then avoid the closest bots
                        self.turn_towards(-closest.x, -closest.y, Globals.FAST)
                        self.drive_forward(Globals.FAST)
                    else: 
                        self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST) #turn toawrds the blue flag and drive fast
                        self.drive_forward(Globals.FAST)
                        if self.has_flag: #if the bot has flag then turn towards the blue half
                            self.turn_towards(0, self.y)
                            self.drive_forward(Globals.FAST)
                            closest, dist = self.closest_to_me() #update the closest bots
                            if dist < 200: #if dist of the closest is less then 200 then avoid it
                                self.turn_towards(-closest.x, -closest.y, Globals.FAST)
                                self.drive_forward(Globals.FAST)
                                    
        
               
    def closest_to_me(self):   
        closest1 = Globals.red_bots[0]
        shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        for enemy in Globals.red_bots:
            if self.point_to_point_distance(enemy.x,enemy.y,self.x,self.y) < shortest_distance: 
                closest1 = enemy
                shortest_distance = self.point_to_point_distance(closest1.x,closest1.y,self.x,self.y)
        return closest1, shortest_distance

    def go_to_jail(self,friend):
        if Globals.blue_bots[2].jailed:
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
        else:
            return  #test
        
    def is_self_stuck(self):
        if not self.jailed:
            if self.x <= self.width:
                return True
            elif self.x >= Globals.SCREEN_WIDTH - self.width:
                return True
            if self.y <= self.width:
                return True
            elif self.y >= Globals.SCREEN_HEIGHT - self.height:
                return True
            else:
                return False


    def closest_enemy_to_flag(self):
        # set default bot for comparison
        closest2 = Globals.red_bots[0]
        # set flag
        flag = Globals.red_flag
        # set default distance
        dist = self.point_to_point_distance(closest2.x,closest2.y,flag.x,flag.y)

        for enemy in Globals.red_bots:
            # checks if any are closer
            if self.point_to_point_distance(enemy.x,enemy.y,flag.x,flag.y) < dist:
                # reallocates the closest bot and the distance
                closest2 = enemy
                dist = dist = self.point_to_point_distance(closest2.x,closest2.y,flag.x,flag.y)

        return closest2

    def dist_to_enemy_flag(self):
        flag = Globals.blue_flag
        dist = self.point_to_point_distance(self.x,self.y,flag.x,flag.y)
        
        return dist

    



    
