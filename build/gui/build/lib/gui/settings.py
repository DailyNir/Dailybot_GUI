import tkinter as tk
import customtkinter
import yaml
import os

CONFIG_PATH = "config/common.yaml"


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x530")
        self.title("Settings")

        # Load settings from the yaml file
        self.settings = self.load_settings()

        # Settings Variables
        self.cutter_ip = tk.StringVar(value=self.settings.get("Cutter IP", ""))
        self.gripper_ip = tk.StringVar(value=self.settings.get("Gripper IP", ""))
        self.camera_default_topic = tk.StringVar(value=self.settings.get("Camera Default Topic Names", ""))
        self.dashboard_default_topic = tk.StringVar(value=self.settings.get("Dashboard Default Topic Names", ""))
        self.default_recordings_folder = tk.StringVar(value=self.settings.get("Default Recordings Folder", ""))
        self.default_logs_folder_path = tk.StringVar(value=self.settings.get("Default Logs Folder Path", ""))
        self.postgresql_database_name = tk.StringVar(value=self.settings.get("PostgreSQL Database Name", ""))
        self.user_name = tk.StringVar(value=self.settings.get("User Name", ""))
        self.password = tk.StringVar(value=self.settings.get("Password", ""))
        self.host_ip = tk.StringVar(value=self.settings.get("Host IP", ""))
        self.port = tk.StringVar(value=self.settings.get("Port", ""))

        self.settings_vars = {
            "Cutter IP": self.cutter_ip,
            "Gripper IP": self.gripper_ip,
            "Camera Default Topic Names": self.camera_default_topic,
            "Dashboard Default Topic Names": self.dashboard_default_topic,
            "Default Recordings Folder": self.default_recordings_folder,
            "Default Logs Folder Path": self.default_logs_folder_path,
            "PostgreSQL Database Name": self.postgresql_database_name,
            "User Name": self.user_name,
            "Password": self.password,
            "Host IP": self.host_ip,
            "Port": self.port
        }

        for idx, (label_text, variable) in enumerate(self.settings_vars.items()):
            label = customtkinter.CTkLabel(self, text=label_text)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

            entry = customtkinter.CTkEntry(self, textvariable=variable)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

        save_button = customtkinter.CTkButton(self, text="Save", command=self.save_settings)
        save_button.grid(row=idx+1, column=0, columnspan=2, pady=20)

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                return yaml.safe_load(file)
        return {}  # return an empty dictionary if file doesn't exist

    def save_settings(self):
        for key, variable in self.settings_vars.items():
            self.settings[key] = variable.get()

        with open(CONFIG_PATH, 'w') as file:
            yaml.dump(self.settings, file)
