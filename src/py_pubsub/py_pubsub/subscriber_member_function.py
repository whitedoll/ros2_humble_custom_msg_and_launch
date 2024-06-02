import rclpy
from rclpy.node import Node

import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from robot_msgs.msg import Custom as CustomMsg
from cv_bridge import CvBridge

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 10)
        # self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        # self.img_subscription = self.create_subscription(Image, 'img_file', self.img_callback, 10)
        # self.img_subscription 

        self.array_subscription = self.create_subscription(CustomMsg, 'test_msg', self.array_listener_callback, 10)
        self.array_subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def array_listener_callback(self, array_msg):
        # self.get_logger().info('my name: "%s"' % array_msg.name)
        self.get_logger().info('age: "{}"'.format(array_msg.age))
        current_frame = self.bridge.imgmsg_to_cv2(array_msg.depth_image)
        cv2.imshow("Test", current_frame)   
        cv2.waitKey(1)

    def img_callback(self, data):
        self.get_logger().info('Receiving video frame')
        current_frame = self.bridge.imgmsg_to_cv2(data)
        cv2.imshow("Test", current_frame)   
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()