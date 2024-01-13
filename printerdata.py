import requests
from config import conf
import tkinter as tk

class PrinterData:

    def get_status(self):
        endpoint = "/api/job"
        url = conf.octoprint_url + endpoint
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': conf.api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to OctoPrint: {e}")
            return None
        
    def command(self, cmd_json):
        endpoint = "/api/job"
        url = conf.octoprint_url + endpoint
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': conf.api_key
        }

        try:
            response = requests.post(url, json=cmd_json, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to OctoPrint: {e}")
            return None
        
    def start(self):
        self.command('{"command": "start"}')

    def cancel(self):
        self.command('{"command": "cancel"}')

    def pause(self):
        self.command('{"command": "pause", "action": "toggle"}')
        
    def update(self):
        status_data = self.get_status()
        if status_data:
            if (status_data["progress"]["completion"] is not None):
                self.progress_completion = "{:.2f}".format(status_data["progress"]["completion"])
            else:
                self.progress_completion = 0
            self.progress_print_time = status_data["progress"]["printTime"]
            self.progress_time_left = status_data["progress"]["printTimeLeft"]
            self.filename = status_data["job"]["file"]["name"]
            self.state = status_data["state"]
            
            # print("Updating printer data values.")
            # print(f"Completion: {self.progress_completion}")
            # print(f"Time left: {self.progress_time_left}")

printer_data = PrinterData()