#!/usr/bin/env python

"""
ROS Action Client Script

This script initializes a ROS node that communicates with an action server to send goal coordinates for a robot.
It also subscribes to the /odom topic to receive odometry data and publishes processed robot position and velocity data.

Main Components:
- **clbk_odom**: Callback function to process odometry data and publish robot position & velocity.
- **clbk_feedback**: Callback function to handle feedback from the action server.
- **action**: Function to accept user input for goal coordinates and send them to the action server.
- **main**: Initializes the ROS node, publisher, and subscriber, and runs the action function.

Author: [Mohamed Elhefnawy]
Date: [01/04/2025]
"""

import time
import rospy
import select
import actionlib
import sys
from std_srvs.srv import *
from nav_msgs.msg import Odometry
from assignment_2_2024.msg import Custom_msg
from assignment_2_2024.msg import PlanningAction, PlanningGoal

def clbk_odom(msg):
    """
    Callback function to process odometry data.
    Extracts the robot's position (x, y) and velocities (linear x, angular z)
    and publishes them on the /robot_pos_vel topic.

    :param msg: Odometry message received from the /odom topic.
    :type msg: Odometry
    """
    
    # Initialize a new custom message instance
    new_custom_msg = Custom_msg()
    
    # Extract position and velocity data
    new_custom_msg.x = msg.pose.pose.position.x            # Robot x position
    new_custom_msg.y = msg.pose.pose.position.y            # Robot y position
    new_custom_msg.vel_x = msg.twist.twist.linear.x        # Linear velocity along x-axis
    new_custom_msg.vel_z = msg.twist.twist.angular.z       # Angular velocity around z-axis
    
    # Publish processed odometry data
    pub.publish(new_custom_msg)

def clbk_feedback(feedback):
    """
    Callback function that processes feedback from the action server.

    Displays feedback messages when the robot reaches or cancels a target.

    :param feedback: Feedback message from the action server.
    :type feedback: Feedback
    """
    
    if feedback.stat == "Target reached!":
        print(feedback)
        print("Target reached successfully!")
        print(f"Robot orientation (angular velocity around Z-axis): {feedback.vel_z} rad/s")
        print("Press 'Enter' to set a new goal\n")
    elif feedback.stat == "Target cancelled!":
        print(feedback)

def action():
    """
    Handles user input to send goal coordinates to the action server.

    The function initializes an action client, waits for the server, and then 
    continuously accepts user input for goal coordinates. The user can cancel 
    an ongoing goal by pressing "c".
    """
    
    # Create an action client
    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)
    
    # Wait for the action server to start
    client.wait_for_server()
    
    while not rospy.is_shutdown():
        time.sleep(0.5)
        print("Set the goal coordinates!")
        
        try:
            # Take user input for goal coordinates
            x = float(input("Enter x coordinate: "))
            y = float(input("Enter y coordinate: "))
            print(f"Goal coordinates set: (x={x}, y={y})")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        
        # Create and send goal to action server
        goal = PlanningGoal()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        client.send_goal(goal, None, None, clbk_feedback)
        
        # Monitor goal execution, allowing user to cancel
        while not client.get_result():
            print("Robot is reaching the goal. Press 'c' to cancel the goal.")
            cancel = select.select([sys.stdin], [], [], 0.1)
            if cancel:
                user_input = sys.stdin.readline().strip()
                if user_input == 'c':
                    client.cancel_goal()
                    break

def main():
    """
    Main function that initializes the ROS node and sets up publishers and subscribers.
    """
    global pub
    
    # Initialize the ROS node
    rospy.init_node('action_client')
    
    # Publisher: Publish robot position and velocity on /robot_pos_vel
    pub = rospy.Publisher('/robot_pos_vel', Custom_msg, queue_size=10)
    
    # Subscriber: Listen to /odom topic and process odometry data
    rospy.Subscriber('/odom', Odometry, clbk_odom)
    
    # Run the action client
    action()

if __name__ == "__main__":
    main()

