import tkinter
import customtkinter
import functools
import threading
from cv_bridge import CvBridge, CvBridgeError
from PIL import Image, ImageTk
import PIL
import cv2
import rclpy
import numpy as np
from sensor_msgs.msg import Image


class TopicSubscriber:
    def __init__(self, node, topic, message_type, callback):
        self.topic = topic
        self.subscription = node.create_subscription(
            message_type,
            topic,
            lambda msg: callback(msg, topic),
            10)


class CamerasFrame(tkinter.Frame):
    def __init__(self, parent, ros_node):
        super().__init__(parent, bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.updated_image_topics = []

        # Initialize ROS2 node
        self.bridge = CvBridge()
        self.latest_images = {}
        self.ros_node = ros_node
        self.available_image_topics = self.get_available_image_topics()
        self.image_dict = {}

        for topic in self.available_image_topics:
            self.image_dict[topic] = None

        self.subscribers = {}
        self.subscribe_to_image_topics()
        self.create_cameras_view()

        # Poll for new images in a separate thread
        threading.Thread(target=self.poll_new_image, daemon=True).start()

    def get_available_image_topics(self):
        topic_names_and_types = self.ros_node.get_topic_names_and_types()
        desired_topics = [topic for topic in topic_names_and_types if 'sensor_msgs/msg/Image' in topic[1]]
        return [topic[0] for topic in desired_topics]

    def subscribe_to_image_topics(self):
        for topic in self.available_image_topics:
            if topic not in self.subscribers:
                self.subscribers[topic] = self.ros_node.create_subscription(
                    Image, 
                    topic, 
                    lambda msg, topic=topic: self.update_image(msg, topic),
                    10
                )

                
    def topics_menu_callback(self, value):
        print(f"Selected topic: {value}")  # Debugging print
        # Fetch the latest image for this topic
        if value in self.latest_images:
            cv_image = self.latest_images[value]
            label = self.image_dict[value]
            self.show_image_on_label(cv_image, label)
            
    def create_cameras_view(self):
        self.tabview = customtkinter.CTkTabview(self, width=1000, height=1000, fg_color="white",
                                                segmented_button_fg_color="#2CC985",
                                                segmented_button_unselected_color="#2CC985",
                                                segmented_button_selected_color="#0C955A",
                                                segmented_button_unselected_hover_color="#0C955A")
        self.tabview.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.tabview.add("Main Camera view")
        self.tabview.tab("Main Camera view").grid_columnconfigure(0, weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Main Camera view"), label_text="", width=900, height=700, fg_color="white")
        self.scrollable_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.scrollable_frame.grid_rowconfigure(list(range(12)), weight=1)

        for i in range(6):
            topic = self.available_image_topics[i] if i < len(self.available_image_topics) else None

            # Add option menu back
            topics_option = customtkinter.CTkOptionMenu(
                master=self.scrollable_frame, dynamic_resizing=True,
                values=self.available_image_topics, width=200,
                command=self.topics_menu_callback )
            topics_option.grid(row=2*(i//3)*2, column=i%3, padx=(20, 10), pady=(20, 10), sticky="w")

            # Add button back
            take_frame = customtkinter.CTkButton(master=self.scrollable_frame, text="Picture", width=50, fg_color="#2CC985")
            take_frame.grid(row=2*(i//3)*2, column=i%3, padx=(20, 10), pady=(20, 10), sticky="e")

            self.image_dict[topic] = tkinter.Label(self.scrollable_frame, width=53, height=20, bg="white")  # The width and height are given in text units, adjust if needed.
            self.image_dict[topic].grid(row=2*(i//3)*2 + 1, column=i%3, padx=20, pady=(20, 10))


    def update_image(self, img_msg, topic):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            self.latest_images[topic] = cv_image
            if topic not in self.updated_image_topics:
                self.updated_image_topics.append(topic)

    def poll_new_image(self):
        while True:
            if self.updated_image_topics:
                topic = self.updated_image_topics.pop(0)
                cv_image = self.latest_images.get(topic)
                if cv_image is not None and topic in self.image_dict:
                    self.show_image_on_label(cv_image, label=self.image_dict[topic])

    def show_image_on_label(self, cv_image, label):
        if cv_image is None or label is None:
            return

        if len(cv_image.shape) == 3 and cv_image.shape[2] == 3:  # Ensure the image has 3 channels
            if cv_image.dtype == np.float32:  # Check if the image is of type float32
                cv_image = (cv_image * 255).astype(np.uint8)  # Convert to uint8
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        elif len(cv_image.shape) == 2:  # Grayscale image
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)
        else:
            print(f"Unsupported image format with shape {cv_image.shape}")
            return

        img = PIL.Image.fromarray(cv_image)
        img = img.resize((400, 300))

        imgtk = ImageTk.PhotoImage(image=img)
        if label:
            label.imgtk = imgtk  # Keep a reference to prevent garbage collection
            label.configure(image=imgtk)

