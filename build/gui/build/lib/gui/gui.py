import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import PIL
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import scrolledtext
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import threading
from std_msgs.msg import Float64MultiArray
import  time
from sensor_msgs.msg import Image
import functools
import datetime
import os
from logger.logger import LoggerModule

from .cameras import CamerasFrame
from .dashboards import DashboardFrame
from .model_testing import ModelTestingFrame
from .Gripper import GripperWindow
from .cutter import CutterWindow
from .logg import LoggerWindow
from .settings import SettingsWindow



def ros_spin(node):
    rclpy.spin(node)
    
class MainApp(customtkinter.CTk):
    def __init__(self,):
        super().__init__()
        self.ros_node = rclpy.create_node('GUI_node')

        # self.cap = cv2.VideoCapture(0)  # 0 for default camera
        self.cutter_window=None
        self.gripper_window=None
        self.logger_window=None
        self.pulsating_task = None
        self.settings_window=None
        # configure window
        self.title("Daily Robotics")
        self.geometry(f"{1850}x{950}")
        self.minsize(1850, 1050)
        # configure grid layout (4x4)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        customtkinter.set_default_color_theme("green")
        customtkinter.set_appearance_mode("Light")
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=500, corner_radius=0,fg_color="#2CC985")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")


        image = PIL.Image.open("src/gui/gui/logo.png")
        # Convert PIL image to CTkImage
        self.logo_image = customtkinter.CTkImage(image,size=(204, 41.5))
        self.logo_img_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image,text="")
        self.logo_img_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        # Buttons
     
        self.placeholder2 = customtkinter.CTkLabel(self.sidebar_frame, text="")
        self.placeholder2.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.sidebar_button_dashboard = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.sidebar_button_event("Dashboard"))
        self.sidebar_button_dashboard.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_button_cameras = customtkinter.CTkButton(self.sidebar_frame, text="Cameras", command=lambda: self.sidebar_button_event("Cameras"))
        self.sidebar_button_cameras.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_button_gripper = customtkinter.CTkButton(self.sidebar_frame, text="Gripper", command=self.open_gripper_controller,width=100)
        self.sidebar_button_gripper.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.sidebar_button_cutter = customtkinter.CTkButton(self.sidebar_frame, text="Cutter", command=self.open_cutter_controller,width=100)
        self.sidebar_button_cutter.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.sidebar_button_model_testing = customtkinter.CTkButton(self.sidebar_frame, text="Model Testing", command=lambda: self.sidebar_button_event("Model Testing"))
        self.sidebar_button_model_testing.grid(row=6, column=0, padx=20, pady=(20, 10), sticky="ew")
       
        self.record_frame=customtkinter.CTkFrame(self.sidebar_frame, width=500, fg_color="#DBDBDB",border_color="red")
        self.record_frame.grid(row=7,column=0,rowspan=2, padx=(20,20), pady=(20, 20),sticky="ew")
        # Record and Stop buttons
        self.record_button = customtkinter.CTkButton(self.record_frame, text="Record", command=self.record_event,width=100,text_color="red")
        self.record_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.stop_button = customtkinter.CTkButton(self.record_frame, text="Stop", command=self.stop_event,width=100)
        self.stop_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        
        # Save path
        self.save_path_entry = customtkinter.CTkEntry(self.record_frame,width=100)
        self.save_path_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.save_path_button = customtkinter.CTkButton(self.record_frame, text="Save To", command=self.select_save_path,width=100)
        self.save_path_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")
        
        # Configure the grid to center the widgets
        self.record_frame.grid_rowconfigure(0, weight=1)   # Top padding row
        self.record_frame.grid_rowconfigure(2, weight=1)   # Bottom padding row
        self.record_frame.grid_columnconfigure(0, weight=1)  # Left padding column
        self.record_frame.grid_columnconfigure(3, weight=1)  # Right padding column
        
        self.placeholder3 = customtkinter.CTkLabel(self.sidebar_frame, text="")
        self.placeholder3.grid(row=9, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.logger = customtkinter.CTkButton(self.sidebar_frame, text="Logger", command=self.logger)
        self.logger.grid(row=10, column=0, padx=20, pady=10, sticky="w")
        # Settings button
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="Settings", command=self.open_settings)
        self.settings_button.grid(row=10, column=0, padx=20, pady=10, sticky="e")
        for i in range(11):
            self.sidebar_frame.grid_rowconfigure(i, weight=1)
      
        
        # create main window frame with widgets
        self.main_window=customtkinter.CTkFrame(self, width=1000,height=1000, fg_color="white")
        self.main_window.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(1, weight=1)
       
        self.dashboard_frame = DashboardFrame(self.main_window,self.ros_node)
        self.cameras_frame = CamerasFrame(self.main_window,self.ros_node)
        self.model_testing_frame = ModelTestingFrame(self.main_window,self.ros_node)
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        #self.cameras_frame.grid(row=0, column=1, sticky="nsew")
        #self.model_testing_frame.grid(row=0, column=1, sticky="nsew")
        self.current_frame = self.dashboard_frame
        self.current_frame.grid(row=0, column=1, sticky="nsew")
       

        # create bottom menu frame with widgets
        self.bottom_menu=customtkinter.CTkFrame(self.main_window, width=700, height=100, fg_color="#2CC985")
        self.bottom_menu.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
       
        style = tkinter.ttk.Style()
        style.theme_use('clam')  # -> uncomment this line if the styling does not work
        style.configure('my.DateEntry',
                        fieldbackground='light green',
                        background='white',
                        foreground='green',
                        arrowcolor='green',textclolor="black")
        self.add_datetime_entry(self.bottom_menu)

        duration_label = customtkinter.CTkLabel(self.bottom_menu, text="Duration:")
        duration_label.grid(row=0, column=3, padx=(10, 10))
        duration_picker = customtkinter.CTkOptionMenu(master=self.bottom_menu, dynamic_resizing=True,
                                                            values=["10 sec", "30 sec", "1 min","3 min", "5 min", "10 min","30 min","1 hour","2 hours","3 hours","4 hours","5 hours","6 hours","7 hours","8 hours","9 hours","10 hours","11 hours","12 hours","13 hours","14 hours","15 hours","16 hours","17 hours","18 hours","19 hours","20 hours","21 hours","22 hours","23 hours","24 hours"])
        duration_picker.grid(row=0, column=4, padx=(0, 10))
        rewind_button = customtkinter.CTkButton(self.bottom_menu, text="<<", command=self.rewind_event)
        rewind_button.grid(row=0, column=5, padx=(10, 10))

        play_stop_button = customtkinter.CTkButton(self.bottom_menu, text="Play/Stop", command=self.play_stop_event)
        play_stop_button.grid(row=0, column=6, padx=(10, 10))

        fast_forward_button = customtkinter.CTkButton(self.bottom_menu, text=">>", command=self.fast_forward_event)
        fast_forward_button.grid(row=0, column=7, padx=(10, 10))
        import_button = customtkinter.CTkEntry(self.bottom_menu)
        import_button.grid(row=0, column=8, padx=(10, 10),sticky="e")
        load_data_button = customtkinter.CTkButton(self.bottom_menu, text="Load Data", command=self.load_data_event)
        load_data_button.grid(row=0, column=9, padx=(10, 10),sticky="e")
        self.bottom_menu.grid_columnconfigure((0, 1, 2,3,4,5,6,7,8,9), weight=1)
        
    def __del__(self):
        # Release the capture when the application is closed
        if self.cap:
            self.cap.release()
        self.dashboard_frame.destroy()
        self.cameras_frame.close_ros()
    def show_frame(self, frame):
        self.current_frame.grid_forget()
        frame.grid(row=0, column=1, sticky="nsew")
        self.current_frame = frame

    def sidebar_button_event(self, button_text):
        if button_text == "Dashboard":
            self.show_frame(self.dashboard_frame)
        elif button_text == "Cameras":
            self.show_frame(self.cameras_frame)
        elif button_text == "Model Testing":
            self.show_frame(self.model_testing_frame)
        else:
            print(f"No frame associated with the button: {button_text}")

    def add_datetime_entry(self,parent):
        # Date selector
        date_entry = DateEntry(parent,width=30, background='green')
        date_entry.grid(row=0, column=0, padx=(10, 10), pady=(20, 20),sticky="w")

        # Hour selector
        hours = [f"{i:02}" for i in range(24)]
        hour_spinbox = ttk.Spinbox(parent, values=hours, wrap=True, width=5)
        hour_spinbox.grid(row=0, column=1, padx=(10, 10),sticky="e")
        
        # Minute selector
        minutes = [f"{i:02}" for i in range(60)]
        minute_spinbox = ttk.Spinbox(parent, values=minutes, wrap=True, width=5)
        minute_spinbox.grid(row=0, column=2, padx=(10, 10),sticky="e")
        
        return date_entry, hour_spinbox, minute_spinbox         

    def settings(self):
        self.tabview = customtkinter.CTkTabview(self.main_window, width=1000, height=800,fg_color="white",segmented_button_fg_color="#2CC985",segmented_button_unselected_color="#2CC985",segmented_button_selected_color="#0C955A",segmented_button_unselected_hover_color="#0C955A")
        self.tabview.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.tabview.add("Settings")
        self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    def open_gripper_controller(self):
        if self.gripper_window is None or not self.gripper_window.winfo_exists():
            self.gripper_window = GripperWindow(self)  # create window if its None or destroyed
        else:
            self.gripper_window.focus()  # if window exists focus it

    def open_cutter_controller(self):
        if self.cutter_window is None or not self.cutter_window.winfo_exists():
            self.cutter_window = CutterWindow(self)  # create window if its None or destroyed
        else:
            self.cutter_window.focus()  # if window exists focus it

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)  # create window if its None or destroyed
        else:
            self.settings_window.focus()  # if window exists focus it
        
    def logger(self):
        if self.logger_window is None or not self.logger_window.winfo_exists():
            self.logger_window = LoggerWindow(self)  # create window if its None or destroyed
        else:
            self.logger_window.focus()  # if window exists focus it
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def record_event(self):
        self.pulsate()
    def pulsate(self):
            # Alternate between the original color and red
            if self.record_button.cget("text_color") == "red":
                self.record_button.configure(text_color="black")  # or your original color
            else:
                self.record_button.configure(text_color="red")  # or your original color

            # Schedule the method to be called again after 500 milliseconds (0.5 second)
            self.stop_event()
            self.pulsating_task = self.after(500, self.pulsate)
    def stop_event(self):
        if self.pulsating_task:
            self.after_cancel(self.pulsating_task)
            self.pulsating_task = None

    def select_save_path(self):
        # Let user select a directory and update the entry
        folder_selected = filedialog.askdirectory()
        self.save_path_entry.delete(0, tkinter.END)
        self.save_path_entry.insert(0, folder_selected)
    

    
    def rewind_event(self):
        pass
    def play_stop_event(self):
        pass
    def fast_forward_event(self):
        pass
    
    def load_data_event(self):
        pass
    def import_path(self):
        file_path = filedialog.askopenfilename()
        # Do something with the file path
        print(file_path)  # For now, we'll just print it

def main():
    rclpy.init()
        
    # Initialize your GUI app
    app = MainApp()
    
    # Spin ROS in a separate thread
    ros_thread = threading.Thread(target=ros_spin, args=(app.ros_node,))
    ros_thread.start()

    app.mainloop()

    # Shutdown ROS cleanly after GUI closes
    rclpy.shutdown()

if __name__ == "__main__":
    main()