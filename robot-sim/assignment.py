from __future__ import print_function

import time
from sr.robot import*

"""
Assignment:

Write a python script for achieving this robot behaviour:
	1)constrantly drive the robot around the circuit in the counter clockwise direction
	2)avoid touching the golden boxes
	3)when the robot is close to a silver box, it should grab it, and move it behind itself

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
 depending of the type of marker (golden or silver). 
The method grab() of the class Robot allows it to pick up a token which is in front of the robot within 0.4 metres from the robot centre
 and returns True if a token is successfully picked up or False otherwise. If the robot is already holding a token, it will throw an
 AlreadyHoldingSomethingException.
The method release() of the class Robot allows it to drop the token previously picked up by the robot.
"""

# Variables:

R = Robot()
"""instance of the class Robot"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

g_th = 1
""" float: Threshold for the control of the distance between the robot and the golden token"""

# Functions:

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    Args: 
          speed (int): the speed of the wheels
	      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    Args: 
          speed (int): the speed of the wheels
	      seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
	"""
	Function to find the closest silver token
	Returns:
		dist (float): distance of the closest silver token (-1 if no silver token is detected)
		rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	"""
	dist=2
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: 
			if -60<=token.rot_y<=60: # look for token which are in front of the robot only
				dist=token.dist
				rot_y=token.rot_y
				
	if dist==2: # if no token is found
		return -1, -1
	else: # if token is found
		return dist, rot_y

def find_golden_token(alpha,beta):
	"""
	Function to find the closest golden token
	Args:
		alpha, beta (float): range of the robot angular vision
	Returns:
		dist (float): distance of the closest golden token (-1 if no golden token is detected)
		rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
	"""
	dist=3
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			if alpha<=token.rot_y<=beta:
				dist=token.dist
				rot_y=token.rot_y
				
	if dist==3: # if no token is found
		return -1, -1
	else: # if token is found
		return dist, rot_y
		
def grab_silver_token():
	"""
	Function to grab a silver token:
		after picking it up, the robot turns and drops it behind itself
		after turning again, the robot goes on driving on straight line
	"""	
	print("Got it!")
	turn(25,2)
	R.release()
	print("Released it!")
	turn(-25,2)
	drive(10,2)
	
def silver_token_alignment(rot_y):
	"""
	Function to control robot alignment with silver token:
		if the angle is in the range established by a_th, go straight
		turn left or right according to rot_y otherwise
	Arg:
		rot_y (float): angle between the robot and the silver token
	"""	
	if -a_th<=rot_y<=a_th: # the robot is well aligned with the token
		print("Ok, I'm well aligned with it.")
		drive(10,1)
				
	elif rot_y>a_th: # the robot needs to move on to the right
		print("Need to turn a little bit to the right.")
		turn(rot_y-a_th,0.5)
		drive(10,1)
			
	elif rot_y<-a_th: # the robot needs to move on to the left
		print("Need to turn a little bit to the left.")
		turn(rot_y+a_th,0.5)
		drive(10,1)

def explore():
	"""
	Function to explore the arena to find silver golden:
		at first look for golden tokens around the robot
		then control its behaviour in order to guide it knowing where are the golden tokens
	"""		
	print("Exploring the arena...")
	
	""" find the left,right and front closest gold tokens """
	dist_g,rot_y_g = find_golden_token(-45,45)
	dist_g_l,rot_y_g_l = find_golden_token(-90,-45)
	dist_g_r,rot_y_g_r = find_golden_token(45,90)
	
	""" control robot behaviour """
	if dist_g>g_th: #  go straight if there is no token right in front of the robot
		print("I can go this way")
		drive(10,1)
	
	else: # there is a token right in front of the robot
		if dist_g_l>dist_g_r: # turn left if there is no token blocking the robot
			print("I need to turn left")
			turn(-10,1)
		elif dist_g_r>dist_g_l: # turn right if there is no token blocking the robot
			print("I need to turn right")
			turn(10,1)
			
	
# Main code:

while 1:	
			
	""" find the closest tokens """
	dist,rot_y = find_silver_token()
	dist_g,rot_y_g = find_golden_token(-75,75)
	
	""" control on robot behaviour """
	if dist==-1: # no silver token is found
		print("I can't find any token!")
		explore()
		
	else: # silver token is found
		print("Fund it!")
		
		if dist_g<g_th/2: # the robot is really close to hit a golden token
			print("Ouch, golden token ahead!")
			turn((rot_y-rot_y_g)*0.1,2)
			drive(5,1)
			
		elif dist<d_th: # the robot can grab the token
			if R.grab():
				grab_silver_token()
			
		else: # the robot has to adjust its alignment with the silver token
			silver_token_alignment(rot_y)
