from GameFrame import RedBot, Globals
import random
import time

class Red3(RedBot):
    def __init__(self, room, x, y):
        RedBot.__init__(self, room, x, y)
        self.initial_wait = random.randint(30, 90)
        self.wait_count = 0
        self.stuck = False

    def tick(self):
                    
        closest_jail , dist_jail = self.closest_friend_to_jail()
        closest = self.closest_enemy_to_flag()   #good (defender and jailer)
        distance = self.closest_to_me()
        blue_flag = Globals.blue_flag
        halfway = Globals.SCREEN_WIDTH / 2
        
        if self.point_to_point_distance(Globals.SCREEN_WIDTH,32,self.x,self.y) > halfway:
            self.turn_towards(Globals.blue_flag.x, Globals.blue_flag.y, Globals.FAST)
            self.drive_forward(Globals.FAST)
        else:  
            if Globals.red_bots[0].jailed:
                for friend in Globals.red_bots:
                    if friend.jailed:
                        self.turn_towards(friend.x, friend.y, Globals.FAST)
                        self.drive_forward(Globals.SLOW)
                    
                           
            if distance < halfway - 200:
                self.turn_towards(closest.x, closest.y, Globals.FAST)
                self.drive_forward(Globals.FAST)  
            else:   
                if self.point_to_point_distance(blue_flag.x,blue_flag.y,self.x,self.y) > 80:
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


    
        
    def closest_friend_to_jail(self):
        # set default bot for comparison
        closest = Globals.red_bots[0]
        # set flag
        jail_x = Globals.SCREEN_WIDTH
        jail_y = Globals.SCREEN_HEIGHT
        # set default distance
        
        dist = self.point_to_point_distance(self.x, self.y, jail_x, jail_y)

        for friends in Globals.red_bots:
            # checks if any are closer
            if self.point_to_point_distance(friends.x, friends.y, jail_x, jail_y) < dist:
                # reallocates the closest bot and the distance
                closest = friends
                dist = dist = self.point_to_point_distance(closest.x, closest.y, jail_x, jail_y)

        return closest, dist