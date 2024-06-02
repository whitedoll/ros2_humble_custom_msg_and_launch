import rclpy
from rclpy.node import Node
import cv2
import os, json
from ament_index_python.packages import get_package_share_directory

from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from robot_msgs.msg import Custom
import numpy as np
# from std_msgs.msg import Float32MultiArray

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.msg_publisher = self.create_publisher(Custom, 'test_msg', 10)
        self.img_publisher_ = self.create_publisher(Image, 'img_file' , 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        # self.timer = self.create_timer(0.1, self.timer_callback)

        self.bridge = CvBridge()
        img_file = os.path.join(get_package_share_directory("py_pubsub"), 'img_file', 'sans.jpg')
        under_img_file = os.path.join(get_package_share_directory("py_pubsub"), 'img_file', 'under.jpg')
        self.img_file = cv2.imread(img_file)
        self.img_file = cv2.resize(self.img_file, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

        self.under_img_file = cv2.imread(under_img_file)
        # self.under_img_file = cv2.resize(self.under_img_file, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

        # print(self.img_file)

    def timer_callback(self):
        msg = String()

        msg.data = 'Hello World: %d' % self.i

        self.robot_data = {
            "name": "robot",
            "age": 5 + self.i,
            "depth_image": self.under_img_file  # 2D or 3D array
        }
        
        dict_msg = Custom()
        dict_msg.name = self.robot_data["name"]
        dict_msg.age = self.robot_data["age"]
        # depth_image_msg = self.bridge.cv2_to_imgmsg(self.robot_data["depth_image"], encoding="32FC1")
        depth_image_msg = self.bridge.cv2_to_imgmsg(self.robot_data["depth_image"])
        dict_msg.depth_image = depth_image_msg
        # dict_msg.depth_image = self.bridge.cv2_to_imgmsg(self.img_file)
        self.msg_publisher.publish(dict_msg)

        self.publisher_.publish(msg)        
        # self.msg_publisher.publish()
        self.img_publisher_.publish(self.bridge.cv2_to_imgmsg(self.img_file))

        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()