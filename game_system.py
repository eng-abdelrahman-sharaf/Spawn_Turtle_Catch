from math import  atan ,degrees
from random import random,randint
from turtlecontroller import Turtle
from factory import Factory
from std_srvs.srv import Empty
from ros2 import ROS2

class GameSystem:
    ResetClass = Factory.create_client("reset" , "resetClient" , Empty , [])
    
    def __init__(self) -> None:
        ROS2().request(self.__class__.ResetClass)
        class Turtles:pass
        self.turtles = Turtles
        Turtles.moving_turtle = Turtle(5,5,0,"turtle1")
        position = self._generate_random_position()
        Turtles.chased_turtle = Turtle(position.x , position.y , position.theta)
        pass    

    def mainloop(self):
        count = 0
        while(True):
            self._move_to_turtle(self.turtles.moving_turtle , self.turtles.chased_turtle)
            count+=1
            position = self._generate_random_position()
            self.turtles.chased_turtle.respawn(position.x , position.y , position.theta)
            print(f"\tyou killed {count} turtles up to now\r" , end="")

    def _generate_random_position(self):
        class Position:
            x = randint( 0 , 10 )+random()
            y = randint( 0 , 10 )+random()
            theta = randint( 0 , 359 )+random()
        moving_turtle = self.turtles.moving_turtle
        if(self._distance(moving_turtle.x , moving_turtle.y , Position.x , Position.y) < 5):
            return self._generate_random_position()
        return Position

    def _get_degree(self,x1,y1,x2,y2):
        if x1 == x2:
            deg = 90
        else:
            deg = degrees(atan((y2-y1)/(x2-x1)))
        if deg < 0:
            deg += 180
        if y2 < y1:
            deg += 180
        return deg

    def _get_offset(self,moving_turtle , target_turtle, time_to_reach_s , steps_num):
        x1 = moving_turtle.x
        y1 = moving_turtle.y
        x2 = target_turtle.x
        y2 = target_turtle.y
        return [(x2-x1)/time_to_reach_s/steps_num , (y2-y1)/time_to_reach_s/steps_num]

    def _collision_happened(self,turtle1 , turtle2):
        if abs(turtle1.x - turtle2.x) < .05 and abs(turtle1.y - turtle2.y) < 0.05:
            return True
        return False
    
    def _distance(self,x1, y1,x2 , y2):
        return ((x2 - x1)**2 + (y2 - y1)**2)**.5
    
    def _move_to_turtle(self,moving_turtle , target_turtle , time_to_reach_s = 1 , steps_num=50):
        offset = self._get_offset(moving_turtle, target_turtle , time_to_reach_s , steps_num)
        for i in range(steps_num * time_to_reach_s):
            new_x = moving_turtle.x + offset[0]
            new_y = moving_turtle.y + offset[1]
            moving_turtle.teleport( new_x,new_y , self._get_degree(new_x , new_y , target_turtle.x , target_turtle.y))