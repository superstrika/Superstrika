from launch import LaunchDescription
from launch_ros.actions import Node

def generateLaunchDescription():

    uartNode = Node(
        package='my_robot_package',
        executable='my_robot_package.superstrika.UartNode:main',
        name='Uart',
        output='screen'
    )

    motorNode = Node(
        package='my_robot_package',
        executable='my_robot_package.superstrika.motorNode:main',
        name='Motor',
        output='screen'
    )