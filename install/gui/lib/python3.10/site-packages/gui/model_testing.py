import tkinter
import customtkinter



class TopicSubscriber:
    def __init__(self, node, topic, message_type, callback):
        self.topic = topic
        self.subscription = node.create_subscription(
            message_type,
            topic,
            lambda msg: callback(msg, topic),
            10)
    

class ModelTestingFrame(tkinter.Frame):
    def __init__(self, parent,ros_node):
        super().__init__(parent, bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.ros_node=ros_node
        self.create_model_testing_view()

    def create_model_testing_view(self):
        self.tabview = customtkinter.CTkTabview(self, width=1000, height=1000, fg_color="white", 
                                                segmented_button_fg_color="#2CC985",
                                                segmented_button_unselected_color="#2CC985",
                                                segmented_button_selected_color="#0C955A",
                                                segmented_button_unselected_hover_color="#0C955A")
        self.tabview.grid(row=0, column=0, sticky="nsew")
        
        # Adding tabs
        self.tabview.add("Model testing")
        self.tabview.add("Model settings")
        self.tabview.add("Model list")
        self.tabview.tab("Model testing").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Model settings").grid_columnconfigure(1, weight=1)
        self.tabview.tab("Model list").grid_columnconfigure(1, weight=1)

        # Scrollable frame configuration
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Model testing"), label_text="", width=900, height=700, fg_color="white")
        self.scrollable_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_rowconfigure(1, weight=1)
        for col in range(5):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)

        # Adding widgets
        self.topics_option = customtkinter.CTkOptionMenu(master=self.scrollable_frame, dynamic_resizing=True,
                                                        values=["Value 1", "Value 2", "/R_xarm6_traj_controller/transition_event"], width=400)
        self.topics_option.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.models_option = customtkinter.CTkOptionMenu(master=self.scrollable_frame, dynamic_resizing=True,
                                                        values=["models", "Value 2", "groundingDino"], width=400)
        self.models_option.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
     
        self.test_model = customtkinter.CTkButton(master=self.scrollable_frame, text="Test model", width=50, fg_color="#2CC985")
        self.test_model.grid(row=0, column=3, padx=20, pady=20, sticky="nsew")
    
        self.take_frame = customtkinter.CTkButton(master=self.scrollable_frame, text="Picture", width=50, fg_color="#2CC985")
        self.take_frame.grid(row=0, column=4, padx=20, pady=20, sticky="nsew")
       
        webcam_label = customtkinter.CTkLabel(self.scrollable_frame, text="", width=300, height=300, fg_color="white")
        webcam_label.grid(row=1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")

    
              

            
