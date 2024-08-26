from rclpy.node import Node
from singleton_class import SingletonClass

class Factory:
    @staticmethod
    def create_client(service_name:str , node_name:str , service_type , request_args_names):
        returned_class = type("".join([*[i.capitalize() for i in service_name.split("_")] , "Client"]) , (SingletonClass,Node) , {})

        def _singleton_init(self):
            Node.__init__(self,node_name)
            self.cli = self.create_client(service_type, service_name)
            while not self.cli.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('service not available, waiting again...')
            self.req = service_type.Request()

        def send_request(self , *args):
            for i in range(len(args)):
                setattr(self.req , request_args_names[i] , args[i])
            return self.cli.call_async(self.req)
        
        returned_class._singleton_init = _singleton_init
        returned_class.send_request = send_request
        return returned_class
    
    @staticmethod
    def create_publisher(node_name:str , topic_name:str , message_ros_type , init_func = lambda self : None ,generate_message_data_func = lambda self : None):
        
        returned_class = type("".join([*[i.capitalize() for i in topic_name.split("_")] , "Publisher"]) , (SingletonClass,Node) , {})

        def _singleton_init(self):
            Node.__init__(self,node_name)
            self.publisher_ = self.create_publisher(message_ros_type, topic_name , 10)
            timer_period = 0.5  # seconds
            self.timer = self.create_timer(timer_period, self.timer_callback)
            init_func(self)
        def timer_callback(self):
            msg = message_ros_type()
            msg.data = generate_message_data_func(self)
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)
        
        returned_class._singleton_init = _singleton_init
        returned_class.timer_callback = timer_callback
        return returned_class

    @staticmethod
    def create_subscriber(node_name:str , topic_name:str , message_ros_type , callback_func = lambda self , msg : None):
        returned_class = type("".join([*[i.capitalize() for i in topic_name.split("_")] , "Subscriber"]) , (SingletonClass,Node) , {})

        def _singleton_init(self):
            Node.__init__(self , node_name)
            self.subscription = self.create_subscription(
                message_ros_type,
                topic_name,
                self.listener_callback,
                10)
            self.subscription  # prevent unused variable warning

        def listener_callback(self, msg):
            self.get_logger().info('I heard: "%s"' % msg.data)
            return msg.data
        
        returned_class._singleton_init = _singleton_init
        returned_class.listener_callback = listener_callback
        return returned_class

