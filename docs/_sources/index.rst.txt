.. assignment_2_2024 documentation master file, created by
   sphinx-quickstart on Fri Mar 28 11:37:59 2025.




Researchtrack Assignment Documentation (ROS)
============================================
Overview

This package extends the original ROS package developed by Prof. Carmine Recchiuto for simulating and controlling a mobile robot in Gazebo. The key contributions include:

Action Client Node: A client node that interacts with the /reaching_goal action server to set a target goal (x, y), move the robot to the target, and provide feedback.

Service to Track Last Target: A service node that tracks the last target goal sent to the robot and responds with the last known target coordinates.

Custom Message for Position and Velocity: A subscriber listens to the robot’s odometry data and publishes a custom message containing the robot’s position and velocity.

Launch File: A launch file that integrates multiple nodes for seamless execution.

Module 1 - Action Client
========================

.. automodule:: scripts.action_client
   :members:
   :show-inheritance:
   :undoc-members:
   
.. autofunction:: scripts.action_client.action
   
   
Module 2 - Last target service
==============================

.. automodule:: scripts.last_target_service
   :members:
   :show-inheritance:
   :undoc-members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
