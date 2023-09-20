import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image
from std_msgs.msg import Float64MultiArray
import random
import cv2
from cv_bridge import CvBridge
import customtkinter


class TopicSubscriber:
    def __init__(self, node, topic, message_type, callback):
        self.topic = topic
        self.subscription = node.create_subscription(
            message_type,
            topic,
            lambda msg: callback(msg, topic),
            10)
    
class DashboardFrame(tkinter.Frame):
    def __init__(self, parent,ros_node):
        super().__init__(parent, bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.data_lock = threading.Lock()
        self.ros_node=ros_node
        # Initialize ROS2 node
        
        # Initialize data structures
       
        #time.sleep(2)
        self.available_topics = self.get_available_topics()
        self.topic_data = {topic: [] for topic in self.available_topics}
        self.joint_state_data = [[] for _ in range(12)]
        self.subscribers = {}
        self.subscribe_to_topics()
        self.topics_menu_vars = [tkinter.StringVar() for _ in range(12)]

        #self.update_graph()

        self.canvases = []
        self.axes = []

        self.update_interval = 20  # Update every 20 milliseconds
        self.after(self.update_interval, self.update_graph)
        self.create_dashboard()
        
    def subscribe_to_topics(self):
        available_topics = self.get_available_topics()
        for topic in available_topics:
            # If the topic doesn't exist in subscribers, then we add it.
            if topic not in self.subscribers:
                # Pass the DashboardFrame's node for subscription
                self.subscribers[topic] = TopicSubscriber(self.ros_node, topic, Float64MultiArray, self.update_data)
                self.topic_data[topic] = []
                #print(f"Subscribed to topic: {topic}")

    def topics_menu_callback(self, choice):
        # Determine which dropdown (and hence which graph) this callback corresponds to
        for dashboard_name, menu_vars in self.dashboard_menu_vars.items():
            for i, menu_var in enumerate(menu_vars):
                if menu_var.get() == choice:
                    self.axes[i].clear()
                    self.axes[i].plot(self.topic_data[choice])
                    self.axes[i].set(title=f'Data from {choice}', ylabel='Value', xlabel='Joint Index')
                    self.axes[i].grid()
                    self.dashboard_canvases[dashboard_name][i].draw()
                    return
    def get_available_topics(self):
        # Get topic names and types
        topic_names_and_types = self.ros_node.get_topic_names_and_types()
        
        # print("All Topics:", topic_names_and_types)  # Debugging
        
        # Only allow Float64MultiArray message type
        desired_topics = [topic for topic in topic_names_and_types if 'std_msgs/msg/Float64MultiArray' in topic[1]]
        
        # print("Filtered Topics:", desired_topics)  # Debugging
        
        # Extract just the topic names
        topic_names = [topic[0] for topic in desired_topics]
        
        return topic_names
    
    def create_dashboard(self):
        self.tabview = customtkinter.CTkTabview(self, width=1000, height=1000, fg_color="white", 
                                                segmented_button_fg_color="#2CC985",
                                                segmented_button_unselected_color="#2CC985",
                                                segmented_button_selected_color="#0C955A",
                                                segmented_button_unselected_hover_color="#0C955A")
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Main Dashboard")
       
        self.tabview.tab("Main Dashboard").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
       
        self.scrollable_frames = {}
        self.dashboard_canvases = {}
        self.dashboard_topic_options = {}
        self.dashboard_save_buttons = {}
        self.dashboard_menu_vars = {}

         # Create frames for each dashboard
        self.create_scrollable_frame("Main Dashboard")

        
    def create_scrollable_frame(self,dashboard_name):
        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab(dashboard_name), label_text="",
                                                                width=900, height=700, fg_color="white")
        self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.scrollable_frame.grid_rowconfigure((0, 1, 2,3,4,5,6,7,8,9,10,11), weight=1)
        
        # Store the scrollable frame in the dictionary
        self.scrollable_frames[dashboard_name] = self.scrollable_frame

        # Initialization for storage
        self.dashboard_canvases[dashboard_name] = []
        self.dashboard_topic_options[dashboard_name] = []
        self.dashboard_save_buttons[dashboard_name] = []
        self.dashboard_menu_vars[dashboard_name] = [tkinter.StringVar() for _ in range(12)]
        default_topics_list=['/Cutter/all_joint_positions','/Cutter/all_joint_velocities','/Cutter/all_joint_efforts','/Gripper/all_joint_positions','/Gripper/all_joint_velocities','/Gripper/all_joint_efforts']
        for i in range(6):
            canvas = self.create_graph_widget(i)
            self.dashboard_canvases[dashboard_name].append(canvas)
            
            # Set the default topic to the position of the current joint
            default_topic =default_topics_list[i]  if i < len(self.available_topics) else "No topics"
            self.dashboard_menu_vars[dashboard_name][i].set(default_topic)
            
            self.topics_option = customtkinter.CTkOptionMenu(
                master=self.scrollable_frame, 
                dynamic_resizing=True,
                values=self.available_topics,
                width=200,
                command=self.topics_menu_callback,
                variable=self.dashboard_menu_vars[dashboard_name][i]  # Use the dashboard-specific StringVar
            ) 
        
            # Adjusting the grid placement
            self.topics_option.grid(row=2*(i//3)*2, column=i%3, padx=(20, 5), pady=(20, 0), sticky="w")
            self.save_data = customtkinter.CTkButton(master=self.scrollable_frame, text="Save Data", width=50, fg_color="#2CC985")
            self.save_data.grid(row=2*(i//3)*2, column=i%3, padx=(5, 20), pady=(20, 0), sticky="e")
            # Store the widgets in the respective dictionaries
            self.dashboard_topic_options[dashboard_name].append(self.topics_option)
            self.dashboard_save_buttons[dashboard_name].append(self.save_data)

    def create_graph_widget(self, i,title="Data"):
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set(title=title, ylabel='Value', xlabel='Joint Index')
        ax.grid()
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2*(i//3)*2 + 1, column=i%3, padx=20, pady=(20, 10))
        canvas.draw()

        self.axes.append(ax)
        
        return canvas
        
    def update_data(self, msg, topic):
        with self.data_lock:
            self.topic_data[topic].append(msg.data)
            if len(self.topic_data[topic]) > 100:
                self.topic_data[topic].pop(0)

    def update_graph(self):
        with self.data_lock:
            for dashboard_name, menu_vars in self.dashboard_menu_vars.items():
                for i, topic_var in enumerate(menu_vars):
                    topic = topic_var.get()
                    if topic and topic in self.topic_data and self.topic_data[topic]:
                        self.axes[i].clear()
                        self.axes[i].plot(self.topic_data[topic])
                        self.axes[i].set(title=f'Data from {topic}', ylabel='Value', xlabel='Joint Index')
                        self.axes[i].grid()
                        self.dashboard_canvases[dashboard_name][i].draw()
        self.after(self.update_interval, self.update_graph)
               
    def destroy(self):
        # Cleanup: destroy subscribers and the node.
        for subscriber in self.subscribers.values():
            self.ros_node.destroy_subscription(subscriber)
        rclpy.shutdown()