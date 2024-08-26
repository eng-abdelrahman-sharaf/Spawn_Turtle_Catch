from ros2 import ROS2
from factory import Factory
from turtlesim.srv import TeleportAbsolute , Spawn ,Kill
from std_srvs.srv import Empty
from math import radians

class Turtle:
    
    teleportClasses = {}
    killClass = Factory.create_client("kill" , "killClient" , Kill , ["name"])
    spawnClass = Factory.create_client("spawn" , "spawnClient" , Spawn , ["x" , "y" , "theta" , "name"])
    clearClass = Factory.create_client("clear" , "clearClient" , Empty , [])

    def __init__(self ,x , y, theta , name = None) -> None:
        self.ros2 = ROS2()
        if(name):
            self.name = name
            self.respawn(x,y,theta)
        else:
            self.name = self._spwan(x,y,theta)
    

    def get_position(self):
        return [self.x , self.y , self.theta]

    def _spwan(self, x , y , theta,name=""):
        x=float(x)
        y=float(y)
        theta=float(theta)
        response = self.ros2.request(self.__class__.spawnClass , x, y, radians(theta) , name)
        self.x = x
        self.y = y
        self.theta = theta
        return response.name

    def teleport(self , x , y , theta):
        x=float(x)
        y=float(y)
        theta=float(theta)
        try:
            self.__class__.teleportClasses[self.name]
        except KeyError:
            self.__class__.teleportClasses[self.name] = Factory.create_client(self.name+"/teleport_absolute" , "teleportClient" , TeleportAbsolute , ["x" , "y" , "theta"])
        self.ros2.request(self.__class__.teleportClasses[self.name] , x, y, radians(theta))
        self.ros2.request(self.__class__.clearClass)
        self.x = x
        self.y = y
        self.theta = theta

    def respawn(self , x , y , theta):
        self.kill()
        self.name = self._spwan(x,y,theta, self.name)

    def kill(self):
        self.ros2.request(self.__class__.killClass , self.name)
    
