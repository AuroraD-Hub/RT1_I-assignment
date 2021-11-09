# Research track 1: python robotic simulator
This is a simple, portable robot simulator developed by Student Robotics. Some of the arenas and the exercises have been modified for the Research Track I course by professor Carmine Recchiuto, Unige. 

## Installing and running
The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML. These can be found in Prof. Recchiuto's Docker Image carms84/noetic_ros2 used for this assignment. 

Once the dependencies are installed and the script written, simply run the commands python2 run.py assignment.py to run it in the simulator.

## Assignment
In this assignment it is required to achieve this robot behaviour:

- constrantly drive the robot around the circuit in the counter-clockwise   direction
- avoid touching the golden boxes
- when the robot is close to a silver box, it should grab it, and move it behind itself

## Robot API features
The API for controlling a simulated robot is designed to be as similar as possible to the SR API.

The following features are represented in Prof. Recchiuto's Git repository and rewritten here. 

### Motors
The simulated robot has two motors configured for skid steering, connected to a two-output Motor Board. The left motor is connected to output 0 and the right motor to output 1.

The Motor Board API is identical to that of the SR API, except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:
(code) 

### The Grabber
The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the R.grab method:
(code) 

The R.grab function returns True if a token was successfully picked up, or False otherwise. If the robot is already holding a token, it will throw an AlreadyHoldingSomethingException.

To drop the token, call the R.release method.

Cable-tie flails are not implemented.

### Vision
To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The R.see method returns a list of all the markers the robot can see, as Marker objects. The robot can only see markers which it is facing towards.

Each Marker object has the following attributes:

- info: a MarkerInfo object describing the marker itself. Has the following attributes:
   - code: the numeric code of the marker.
   - marker_type: the type of object the marker is attached to (either MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER or MARKER_ARENA).
   - offset: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
   - size: the size that the marker would be in the real game, for compatibility with the SR API.
- centre: the location of the marker in polar coordinates, as a PolarCoord object. Has the following attributes:
   - length: the distance from the centre of the robot to the object (in metres).
   - rot_y: rotation about the Y axis in degrees.
- dist: an alias for centre.length
- res: the value of the res parameter of R.see, for compatibility with the SR API.
- rot_y: an alias for centre.rot_y
- timestamp: the time at which the marker was seen (when R.see was called).
