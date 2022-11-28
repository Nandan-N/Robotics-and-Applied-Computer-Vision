import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def _init_(self):
        
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):      # euclid distance between current position and goal 
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):

        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):    # due to this functon turtle moves towards its goal 
        goal_pose = Pose()

        goal_pose.x = float(input("Set your x goal: "))   # taking inputs 
        goal_pose.y = float(input("Set your y goal: "))

        print(" enter a number slightly greater than 0 for tolerance (e.g. 0.01)")
        distance_tolerance = float(input("Set your tolerance: "))

        print("your turtle has started moving what are doing looking at this terminal ")

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

    
            
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            self.velocity_publisher.publish(vel_msg)

            self.rate.sleep()


        vel_msg.linear.x = 0       # stoping our turtle after execution of input 
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        rospy.spin()

if _name_ == '_main_':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
