import tkinter
import customtkinter
from logger.logger import LoggerModule  
import os
import datetime
from tkinter import filedialog
from tkinter import scrolledtext


class LoggerWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LoggerModule.set_logger_window(self)

        self.geometry("1000x600")
        self.title("Logger")

        # Entry widget
        self.entry = customtkinter.CTkEntry(self, width=40)  # Adjust width as needed
        self.entry.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        # Log button
        log_button = customtkinter.CTkButton(self, text="Log", command=self.log_action)
        log_button.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Save button
        save_button = customtkinter.CTkButton(self, text="Save", command=self.save_action)
        save_button.grid(row=0, column=2, padx=10, pady=10, sticky="nswe")

        # ScrolledText widget to show logs with vertical scrollbar
        self.log_text = scrolledtext.ScrolledText(self, width=50, height=20)  # Adjust width and height as needed
        self.log_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configure the grid to expand with the window
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{current_date}.txt"
        log_filepath = os.path.join(LoggerModule.log_directory, log_filename)

        if os.path.exists(log_filepath):
            with open(log_filepath, "r") as file:
                self.log_text.insert(tkinter.END, file.read())
    
    def insert_log(self, message):
        self.log_text.insert(tkinter.END, message)
        
    def log_action(self):
        log = self.entry.get()
        LoggerModule.log(log)  # Use LoggerModule to log the message
        self.entry.delete(0, tkinter.END)

    def save_action(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.log_text.get(1.0, tkinter.END))
           