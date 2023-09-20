import os
import datetime

class LoggerModule:
    _logger_window_instance = None
    log_directory = "logs"

    @classmethod
    def set_logger_window(cls, logger_window):
        cls._logger_window_instance = logger_window

    @classmethod
    def log(cls, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_with_timestamp = f"[{timestamp}] {message}\n"

        # Ensure log directory exists
        if not os.path.exists(cls.log_directory):
            os.makedirs(cls.log_directory)

        # Determine file name based on current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{current_date}.txt"
        log_filepath = os.path.join(cls.log_directory, log_filename)

        # Save log with timestamp to the determined file
        with open(log_filepath, "a") as file:
            file.write(log_with_timestamp)

        # If logger window instance is set, update the window
        if cls._logger_window_instance:
            cls._logger_window_instance.insert_log(log_with_timestamp)
