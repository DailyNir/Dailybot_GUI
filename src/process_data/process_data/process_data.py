import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher_node')
        
        # Subscribers
        self.create_subscription(JointState, '/L_xarm/joint_states', self.gripper_joint_state_callback, 10)
        self.create_subscription(JointState, '/R_xarm/joint_states', self.cutter_joint_state_callback, 10)
        
        self.pub_all = self.create_publisher(JointState, '/joint_states', 10)
        
        # Publishers for individual joints and attributes
        self.cutter_pubs_positions = [self.create_publisher(Float64MultiArray, f'/R_xarm/joint_{i+1}_position', 10) for i in range(6)]
        self.cutter_pubs_velocities = [self.create_publisher(Float64MultiArray, f'/R_xarm/joint_{i+1}_velocity', 10) for i in range(6)]
        self.cutter_pubs_efforts = [self.create_publisher(Float64MultiArray, f'/R_xarm/joint_{i+1}_effort', 10) for i in range(6)]
        
        self.gripper_pubs_positions = [self.create_publisher(Float64MultiArray, f'/L_xarm/joint_{i+1}_position', 10) for i in range(6)]
        self.gripper_pubs_velocities = [self.create_publisher(Float64MultiArray, f'/L_xarm/joint_{i+1}_velocity', 10) for i in range(6)]
        self.gripper_pubs_efforts = [self.create_publisher(Float64MultiArray, f'/L_xarm/joint_{i+1}_effort', 10) for i in range(6)]
        
        # Publishers for joint groups
        self.pub_all_positions_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_positions', 10)
        self.pub_all_velocities_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_velocities', 10)
        self.pub_all_efforts_cutter = self.create_publisher(Float64MultiArray, '/Cutter/all_joint_efforts', 10)
        self.pub_all_positions_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_positions', 10)
        self.pub_all_velocities_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_velocities', 10)
        self.pub_all_efforts_gripper = self.create_publisher(Float64MultiArray, '/Gripper/all_joint_efforts', 10)
        
    def gripper_joint_state_callback(self, joint_msg):
        # Publish individual joints for Gripper
        for i in range(6):
            self.gripper_pubs_positions[i].publish(Float64MultiArray(data=[joint_msg.position[i]]))
            self.gripper_pubs_velocities[i].publish(Float64MultiArray(data=[joint_msg.velocity[i]]))
            self.gripper_pubs_efforts[i].publish(Float64MultiArray(data=[joint_msg.effort[i]]))
        
        # Publish joint groups for Gripper
        self.pub_all_positions_gripper.publish(Float64MultiArray(data=joint_msg.position))
        self.pub_all_velocities_gripper.publish(Float64MultiArray(data=joint_msg.velocity))
        self.pub_all_efforts_gripper.publish(Float64MultiArray(data=joint_msg.effort))

    def cutter_joint_state_callback(self, joint_msg):
        # Publish individual joints for Cutter
        for i in range(6):
            self.cutter_pubs_positions[i].publish(Float64MultiArray(data=[joint_msg.position[i]]))
            self.cutter_pubs_velocities[i].publish(Float64MultiArray(data=[joint_msg.velocity[i]]))
            self.cutter_pubs_efforts[i].publish(Float64MultiArray(data=[joint_msg.effort[i]]))
        
        # Publish joint groups for Cutter
        self.pub_all_positions_cutter.publish(Float64MultiArray(data=joint_msg.position))
        self.pub_all_velocities_cutter.publish(Float64MultiArray(data=joint_msg.velocity))
        self.pub_all_efforts_cutter.publish(Float64MultiArray(data=joint_msg.effort))

def main(args=None):
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    rclpy.spin(joint_state_publisher)
    joint_state_publisher.destroy_node()
    rclpy.shutdown()