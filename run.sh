#!/bin/bash

# Stop on error
set -e

echo "sourcing ros2"
source /opt/ros/humble/setup.sh # change to your ros2 version

echo "🔧 Building the workspace..."
colcon build --packages-select my_robot_package --symlink-install # build the project

echo "✅ Build complete. Sourcing the environment..."
source install/setup.bash # source the environment

echo "🚀 Running real_button_node..."
ros2 run my_robot_package test  # run the node
