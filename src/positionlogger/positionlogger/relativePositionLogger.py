import math
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Path
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class FrameListener(Node):
    def __init__(self):
        super().__init__('relativePositionLogger')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.path_publisher = self.create_publisher(Path, 'robot_path', 1)
        self.path = Path()
        self.path.header.frame_id = 'map'
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        from_frame_rel = 'base_link'
        to_frame_rel = 'map'
        try:
            t = self.tf_buffer.lookup_transform(
                to_frame_rel,
                from_frame_rel,
                rclpy.time.Time())
            pose = PoseStamped()
            pose.header.frame_id = from_frame_rel
            pose.pose.position.x = t.transform.translation.x
            pose.pose.position.y = t.transform.translation.y
            pose.pose.orientation.w = 1.0
            self.path.poses.append(pose)
            self.path_publisher.publish(self.path)
            self.get_logger().info("linear x{} linear y {}".format(t.transform.translation.x,t.transform.translation.y))
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
            return

def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == '__main__':
    main()


