import customtkinter



class GripperWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x1000")
        self.title("Gripper Controller")
        self.grid_columnconfigure(0, weight=1)  # Left padding column
        self.grid_columnconfigure(2, weight=1)  # Right padding column
        self.grid_columnconfigure(1, weight=1)  # Allow column to expand as window resizes

        self.label = customtkinter.CTkLabel(self, text="Xarm6 Gripper Controller")
        self.label.grid(row=0, column=1, padx=20, pady=10)
        self.label.grid_columnconfigure(1, weight=1)
        self.connect_to_gripper=customtkinter.CTkButton(self, text="Connect to Gripper", command=self.plus_z_event,width=100)
        self.connect_to_gripper.grid(row=1, column=1, padx=20, pady=10)
        self.J1_label=customtkinter.CTkLabel(self, text="J1:")
        self.J1_label.grid(row=2, column=1, padx=20, pady=10,sticky="w")
        self.J1=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J1.set(0)
        
        self.J2_label=customtkinter.CTkLabel(self, text="J2:")
        self.J2_label.grid(row=3, column=1, padx=20, pady=10,sticky="w")
        self.J2=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J2.set(0)
        
        self.J3_label=customtkinter.CTkLabel(self, text="J3:")
        self.J3_label.grid(row=4, column=1, padx=20, pady=10,sticky="w")
        self.J3=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J3.set(0)
        
        self.J4_label=customtkinter.CTkLabel(self, text="J4:")
        self.J4_label.grid(row=5, column=1, padx=20, pady=10,sticky="w")
        self.J4=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J4.set(0)
        
        self.J5_label=customtkinter.CTkLabel(self, text="J5:")
        self.J5_label.grid(row=6, column=1, padx=20, pady=10,sticky="w")
        self.J5=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J5.set(0)
        
        self.J6_label=customtkinter.CTkLabel(self, text="J6:")
        self.J6_label.grid(row=7, column=1, padx=20, pady=10,sticky="w")
        self.J6=customtkinter.CTkSlider(self, from_=-360,to=360,number_of_steps=720, width=500)
        self.J6.set(0)
        
        self.J1.grid(row=2, column=1, padx=20, pady=10,sticky="e")
        self.J2.grid(row=3, column=1, padx=20, pady=10,sticky="e")
        self.J3.grid(row=4, column=1, padx=20, pady=10,sticky="e")
        self.J4.grid(row=5, column=1, padx=20, pady=10,sticky="e")
        self.J5.grid(row=6, column=1, padx=20, pady=10,sticky="e")
        self.J6.grid(row=7, column=1, padx=20, pady=10,sticky="e")
        self.J1.grid_columnconfigure(0, weight=1)
        self.J2.grid_columnconfigure(0, weight=1)
        self.J3.grid_columnconfigure(0, weight=1)
        self.J4.grid_columnconfigure(0, weight=1)
        self.J5.grid_columnconfigure(0, weight=1)
        self.J6.grid_columnconfigure(0, weight=1)
        
        self.Z_YAW_frame=customtkinter.CTkFrame(self, width=400)
        self.Z_YAW_frame.grid(row=8, column=1, padx=20, pady=10,sticky="w")
        self.Z_YAW_frame.columnconfigure((0, 1, 2, 3), weight=1)
        # Z_YAW_frame
        self.Z_YAW_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.Z_YAW_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.Z_YAW_frame.grid_columnconfigure(4, weight=1)
        
        self.Plus_Z=customtkinter.CTkButton(self.Z_YAW_frame, text="+Z", command=self.plus_z_event,width=100)
        self.Plus_Z.grid(row=0, column=0, padx=20, pady=10,sticky="w")
        self.Minus_Z=customtkinter.CTkButton(self.Z_YAW_frame, text="-Z", command=self.plus_z_event,width=100)
        self.Minus_Z.grid(row=0, column=1, padx=20, pady=10,sticky="w")
        self.Minus_YAW=customtkinter.CTkButton(self.Z_YAW_frame, text="-YAW", command=self.plus_z_event,width=100)
        self.Minus_YAW.grid(row=0, column=2, padx=20, pady=10,sticky="e")
        self.Plus_YAW=customtkinter.CTkButton(self.Z_YAW_frame, text="+YAW", command=self.plus_z_event,width=100)
        self.Plus_YAW.grid(row=0, column=3, padx=20, pady=10,sticky="e")
        
        self.Y_P_frame=customtkinter.CTkFrame(self, width=400)
        self.Y_P_frame.grid(row=9, column=1, padx=20, pady=10,sticky="ew")
        self.Y_P_frame.columnconfigure((0, 1, 2), weight=1)
        self.Y_P_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.Y_P_frame.grid_columnconfigure(2, weight=1)
        
        self.Plus_Y=customtkinter.CTkButton(self.Y_P_frame, text="+Y", command=self.plus_z_event,width=100)
        self.Plus_Y.grid(row=0, column=0, padx=20, pady=10)  
        self.Plus_P=customtkinter.CTkButton(self.Y_P_frame, text="+P", command=self.plus_z_event,width=100)
        self.Plus_P.grid(row=0, column=1, padx=20, pady=10)
        self.Y_P_frame.columnconfigure((0,1), weight=1)
          
        self.X_R_frame=customtkinter.CTkFrame(self, width=400)
        self.X_R_frame.grid(row=10, column=1, padx=20, pady=10,sticky="w")
        self.X_R_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.X_R_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.X_R_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.X_R_frame.grid_columnconfigure(4, weight=1)
        
        self.Minus_X=customtkinter.CTkButton(self.X_R_frame, text="-X", command=self.plus_z_event,width=100)
        self.Minus_X.grid(row=0, column=0, padx=20, pady=10)
        self.Plus_X=customtkinter.CTkButton(self.X_R_frame, text="+X", command=self.plus_z_event,width=100)
        self.Plus_X.grid(row=0, column=1, padx=20, pady=10)
        self.Minus_R=customtkinter.CTkButton(self.X_R_frame, text="-R", command=self.plus_z_event,width=100)
        self.Minus_R.grid(row=0, column=2, padx=20, pady=10)
        self.Plus_R=customtkinter.CTkButton(self.X_R_frame, text="+R", command=self.plus_z_event,width=100)
        self.Plus_R.grid(row=0, column=3, padx=20, pady=10) 
        self.X_R_frame.columnconfigure((0,1,2,3), weight=1)
         
        self.Minus_Y_P_frame=customtkinter.CTkFrame(self, width=400)
        self.Minus_Y_P_frame.grid(row=11, column=1, padx=20, pady=10,sticky="ew")     
        self.Minus_Y_P_frame.columnconfigure((0, 1, 2), weight=1)
        self.Minus_Y_P_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.Minus_Y_P_frame.grid_columnconfigure(2, weight=1)
        
        self.Minus_Y=customtkinter.CTkButton(self.Minus_Y_P_frame, text="-Y", command=self.plus_z_event,width=100)
        self.Minus_Y.grid(row=0, column=0, padx=20, pady=10)
        self.Minus_P=customtkinter.CTkButton(self.Minus_Y_P_frame, text="-P", command=self.plus_z_event,width=100)
        self.Minus_P.grid(row=0, column=1, padx=20, pady=10)
        
        self.xyz_rpy_entry_frame=customtkinter.CTkFrame(self, width=400)
        self.xyz_rpy_entry_frame.grid(row=12, column=1, padx=20, pady=10,sticky="w")
        self.xyz_rpy_entry_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.xyz_rpy_entry_frame.rowconfigure((0, 1), weight=1)
       
        self.x_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="X:")
        self.x_label.grid(row=0, column=0, padx=20, pady=10)
        self.x_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.x_entry.grid(row=0, column=1, padx=20, pady=10)
        self.y_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="Y:")
        self.y_label.grid(row=0, column=2, padx=20, pady=10)
        self.y_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.y_entry.grid(row=0, column=3, padx=20, pady=10)
        self.z_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="Z:")
        self.z_label.grid(row=0, column=4, padx=20, pady=10)
        self.z_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.z_entry.grid(row=0, column=5, padx=20, pady=10)
        self.r_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="R:")
        self.r_label.grid(row=1, column=0, padx=20, pady=10)
        self.r_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.r_entry.grid(row=1, column=1, padx=20, pady=10)
        self.p_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="P:")
        self.p_label.grid(row=1, column=2, padx=20, pady=10)
        self.p_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.p_entry.grid(row=1, column=3, padx=20, pady=10)
        self.yaw_label=customtkinter.CTkLabel(self.xyz_rpy_entry_frame, text="Yaw:")
        self.yaw_label.grid(row=1, column=4, padx=20, pady=10)
        self.yaw_entry=customtkinter.CTkEntry(self.xyz_rpy_entry_frame,width=100)
        self.yaw_entry.grid(row=1, column=5, padx=20, pady=10)
        self.xyz_rpy_entry_frame.rowconfigure((0,1), weight=1)
        self.xyz_rpy_entry_frame.columnconfigure((0,1,2,3,4,5), weight=1)
        self.xyz_rpy_entry_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.xyz_rpy_entry_frame.grid_columnconfigure(2, weight=1)
        
        self.controls_frame=customtkinter.CTkFrame(self, width=400)
        self.controls_frame.grid(row=13, column=1, padx=20, pady=10,sticky="ew")
        self.controls_frame.columnconfigure((0, 1), weight=1)
        self.Z_YAW_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.Z_YAW_frame.grid_columnconfigure(2, weight=1)  # Right padding

        self.controls_frame.rowconfigure((0, 1, 2), weight=1)

        self.plan_button=customtkinter.CTkButton( self.controls_frame, text="Plan", command=self.plus_z_event,width=100)
        self.plan_button.grid(row=0, column=0, padx=20, pady=10)
        self.execute_button=customtkinter.CTkButton( self.controls_frame, text="Execute", command=self.plus_z_event,width=100)
        self.execute_button.grid(row=0, column=1, padx=20, pady=10)
        self.stop_button=customtkinter.CTkButton( self.controls_frame, text="Stop", command=self.plus_z_event,width=100)
        self.stop_button.grid(row=1, column=0, padx=20, pady=10)
        self.home_button=customtkinter.CTkButton( self.controls_frame, text="Home", command=self.plus_z_event,width=100)
        self.home_button.grid(row=1, column=1, padx=20, pady=10)
        self.open_gripper_buttom=customtkinter.CTkButton( self.controls_frame, text="Open Gripper", command=self.plus_z_event,width=100)
        self.open_gripper_buttom.grid(row=2, column=0, padx=20, pady=10)
        self.close_gripper_buttom=customtkinter.CTkButton( self.controls_frame, text="Close Gripper", command=self.plus_z_event,width=100)
        self.close_gripper_buttom.grid(row=2, column=1, padx=20, pady=10)
        self.controls_frame.rowconfigure((0,1,2), weight=1)
        self.controls_frame.columnconfigure((0,1), weight=1)
        self.controls_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.controls_frame.grid_columnconfigure(2, weight=1)  # Right padding

        self.rowconfigure((8,9,10,11,12,13,14), weight=1)
        for i in range(14):  # You have 14 rows (0 to 13)
            self.grid_rowconfigure(i, weight=1)
    def plus_z_event(self):
        pass
    def minus_z_event(self):
        pass
    def minus_yaw_event(self):
        pass
    def plus_yaw_event(self):
        pass
    def plus_y_event(self):
        pass
    def plus_p_event(self):
        pass
    def minus_x_event(self):
        pass
    def plus_x_event(self):
        pass
    def minus_r_event(self):
        pass
    def plus_r_event(self):
        pass
    def minus_y_event(self):
        pass
    def minus_p_event(self):
        pass
    def plan_event(self):
        pass
    def execute_event(self):
        pass
    def stop_event(self):
        pass
    def home_event(self):
        pass
    def open_gripper_event(self):
        pass
    def close_gripper_event(self):
        pass