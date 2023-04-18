# ED5215 Path Planning Project - RCM on the kuka iiwa 7

## Team:

**Shrung D N - ME19B168**

**Sidharth Tadeparti - ME19B051**

**Tejas Rao - ME19B179**

Various Path Planning Algorithms are implemented to enforce the RCM (Remote Centre of Motion) of a surgical robot. All the simulations are done using the KUKA iiwa 7 robot package on Gazebo. FK and Collision planning is natively implemented.




**Running the Code**
- To open the simulator: roslaunch iiwa_tool_moveit moveit_planning_and_execution.launch
- To start the controller: rosrun iiwa_control sunrise2.py 
- To plan and execute path: rosrun iiwa_moveit main2.py
- The above files need to opened in the order given.

- All algorithms are available in different files in .../catkin_ws/src/iiwa_stack/iiwa_moveit/scripts. They need to imported and appropriately used in main2.py







**Instructions:(for contributors on local machine and repo)***

- The algorithm folder, can be used, but code in deployment in RCM_Project/....../catkin_ws/src/iiwa_stack/iiwa_moveit/scripts.
- To be similarly mirrored in HOME/catkin_ws
