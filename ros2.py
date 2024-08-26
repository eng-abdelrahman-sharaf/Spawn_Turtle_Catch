import rclpy
from singleton_class import SingletonClass

class ROS2(SingletonClass):
    def _singleton_init(self , *args) -> None:
        if(self._instance != None): return
        if len(args) == 0: args = None
        rclpy.init(args=args)
        
    def shutdown(self):
        rclpy.shutdown()
        
    def publish(self , PublisherClass):
        publisher = PublisherClass()
        rclpy.spin(publisher)
        # publisher.destroy_node()


    def subscribe(self , SubscriberClass):
        subscriber = SubscriberClass()
        rclpy.spin(subscriber)
        # subscriber.destroy_node()

    def request(self,ClientClass , *request_args):
        client = ClientClass()
        future = client.send_request(*request_args)
        rclpy.spin_until_future_complete(client, future)
        response = future.result()
        # client.destroy_node()
        return response