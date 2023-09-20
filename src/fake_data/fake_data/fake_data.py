import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image
from std_msgs.msg import Float64MultiArray
import random
import cv2
from cv_bridge import CvBridge

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher_node')
        self.pub_all = self.create_publisher(JointState, '/joint_states', 10)
        
        # Publishers for individual joints and attributes
        self.pubs_positions = [self.create_publisher(Float64MultiArray, f'/joint_{i+1}_position', 10) for i in range(6)]
        self.pubs_velocities = [self.create_publisher(Float64MultiArray, f'/joint_{i+1}_velocity', 10) for i in range(6)]
        self.pubs_efforts = [self.create_publisher(Float64MultiArray, f'/joint_{i+1}_effort', 10) for i in range(6)]
        
        # Publishers for joint groups
        # self.pub_all_positions_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_positions', 10)
        # self.pub_all_velocities_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_velocities', 10)
        # self.pub_all_efforts_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_efforts', 10)
        # self.pub_all_positions_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_positions', 10)
        # self.pub_all_velocities_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_velocities', 10)
        # self.pub_all_efforts_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_efforts', 10)
        
        self.timer = self.create_timer(0.05, self.publish_random_joint_states)  # Publish at 10Hz
         # Image publisher and bridge to convert between OpenCV images and ROS image messages
        self.image_pub1 = self.create_publisher(Image, '/camera/image_raw1', 10)
        self.image_pub2 = self.create_publisher(Image, '/camera/image_raw2', 10)
        self.image_pub3 = self.create_publisher(Image, '/camera/image_raw3', 10)
        self.image_pub4 = self.create_publisher(Image, '/camera/image_raw4', 10)
        self.image_pub5 = self.create_publisher(Image, '/camera/image_raw5', 10)
        self.image_pub6 = self.create_publisher(Image, '/camera/image_raw6', 10)

        self.bridge = CvBridge()

        # If you're capturing from a video file, replace 0 with the video file's path.
        self.cap = cv2.VideoCapture(0)

        self.image_timer = self.create_timer(0.02, self.publish_camera_image)  # Assuming 10 FPS for the camera feed
    
    def publish_camera_image(self):
        ret, frame = self.cap.read()
        if ret:
            image_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")  # Convert the image to ROS Image message format
            self.image_pub1.publish(image_msg)
            self.image_pub2.publish(image_msg)
            self.image_pub3.publish(image_msg)
            self.image_pub4.publish(image_msg)
            self.image_pub5.publish(image_msg)
            self.image_pub6.publish(image_msg)
            
    def publish_random_joint_states(self):
        pass
        # joint_msg = JointState()
        
        # joint_msg.header.stamp = self.get_clock().now().to_msg()
        # joint_msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        
        # # Generate random joint values
        # joint_msg.position = [random.uniform(-3.14, 3.14) for _ in range(6)]
        # joint_msg.velocity = [random.uniform(-1, 1) for _ in range(6)]
        # joint_msg.effort = [random.uniform(-10, 10) for _ in range(6)]
        
        # self.pub_all.publish(joint_msg)

        # # Publish individual joints and their attributes
        # for i in range(6):
        #     position_msg = Float64MultiArray(data=[joint_msg.position[i]])
        #     velocity_msg = Float64MultiArray(data=[joint_msg.velocity[i]])
        #     effort_msg = Float64MultiArray(data=[joint_msg.effort[i]])

        #     self.pubs_positions[i].publish(position_msg)
        #     self.pubs_velocities[i].publish(velocity_msg)
        #     self.pubs_efforts[i].publish(effort_msg)

        # Publish joint groups
        # self.pub_all_positions_cutter.publish(Float64MultiArray(data=joint_msg.position))
        # self.pub_all_velocities_cutter.publish(Float64MultiArray(data=joint_msg.velocity))
        # self.pub_all_efforts_cutter.publish(Float64MultiArray(data=joint_msg.effort))
        # self.pub_all_positions_gripper.publish(Float64MultiArray(data=joint_msg.position))
        # self.pub_all_velocities_gripper.publish(Float64MultiArray(data=joint_msg.velocity))
        # self.pub_all_efforts_gripper.publish(Float64MultiArray(data=joint_msg.effort))
        
def main(args=None):
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    rclpy.spin(joint_state_publisher)
    joint_state_publisher.cap.release()  # Release the video capture
    joint_state_publisher.destroy_node()
    rclpy.shutdown()
