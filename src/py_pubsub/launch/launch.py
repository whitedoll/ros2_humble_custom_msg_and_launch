from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="py_pubsub",
            executable="talker",
            output="screen"
        ),
        Node(
            package="py_pubsub",
            executable="listener",
            output="screen"
        ),
    ])