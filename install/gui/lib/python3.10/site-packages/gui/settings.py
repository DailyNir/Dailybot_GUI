import customtkinter
import tkinter

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x1000")
        self.title("Settings")