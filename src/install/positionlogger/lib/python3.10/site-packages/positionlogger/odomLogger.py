import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomLogger(Node):
    def __init__(self):
        super().__init__('odom_logger')
        self.get_logger().info("Started odometry logger...")
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.file = open('odom.txt', 'w')

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.file.write(f'{x} {y}\n')

    def __del__(self):
        self.file.close()

def main(args=None):
    rclpy.init(args=args)
    odom_logger = OdomLogger()
    rclpy.spin(odom_logger)
    odom_logger.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
