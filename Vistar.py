#!/usr/bin/python3
import subprocess
import requests
import json
import rumps
from datetime import datetime

# Define the osquery queries and their simplified names as a dictionary
osquery_queries = {
    "SELECT REPLACE(CONCAT(hostname, '-', uuid), '-', '_') AS uniqueId FROM system_info;": "uniqueId",
    "SELECT name, version FROM os_version;": "os_version",
    "SELECT CASE WHEN encrypted = '1' THEN 'Yes' ELSE 'No' END AS is_encrypted FROM disk_encryption;":"HD",
    "SELECT enabled FROM screenlock;":"SL"
}

# Define the API endpoint where you want to send the data
endpoint_url = "https://api.vistar.cloud/api/v1/computers/osquery_log_data/"

# Specify the interval (in seconds) between data sends (e.g., every 1 hour)
interval_seconds = 60

# Variable to track the sync state
last_sync_time = None
sync_active = False  # Track whether sync is active or not

class VistarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(VistarApp, self).__init__(*args, **kwargs)
        self.icon = "/Applications/Vistar.app/Contents/Resources/vistarlogo.png"
        self.start_icon = "/Applications/Vistar.app/Contents/Resources/toggle_on.png"
        self.stop_icon="/Applications/Vistar.app/Contents/Resources/toggle_off.png"
        self.login="/Applications/Vistar.app/Contents/Resources/login.png"
        self.menu.add(rumps.MenuItem(""))
        self.menu.add(rumps.MenuItem("Vistar Agent",icon=self.login))
        self.menu.add(rumps.MenuItem(""))
        # self.quit_button=None


        if sync_active:

            self.menu.add(rumps.MenuItem('Start Sync', icon=self.start_icon, callback=self.toggle_sync, key='⌘v'))
            self.stop_icon=""
        else:
            self.menu.add(rumps.MenuItem('Start Sync',icon=self.stop_icon, callback=self.toggle_sync, key='s'))
            self.start_icon=""
        # self.menu.add(rumps.MenuItem('Quit', callback=rumps.quit_application))
        self.menu.add(rumps.MenuItem(""))
    @rumps.clicked('Start Sync')
    def toggle_sync(self, sender):
        global sync_active
        global timer
        sync_active = not sync_active
        sender.state = not sender.state
        self.update_menu()

        

        if sync_active:
            self.sync_data(None)  # Pass a placeholder parameter to match the expected signature
        else: 
            if timer is not None:
                timer.stop()

    def sync_data(self, _):
        global last_sync_time
        global sync_active
        global timer
        current_time = datetime.now()
        if last_sync_time is None:
            last_sync_time = current_time
            osquery_data = self.run_osquery()
            self.send_data_to_api(osquery_data)

        elapsed_time = (current_time - last_sync_time).total_seconds()

        if elapsed_time >= interval_seconds and sync_active:
            osquery_data = self.run_osquery()
            self.send_data_to_api(osquery_data)
            last_sync_time = current_time
            if sync_active:
                self.update_menu()

        timer = rumps.Timer(self.sync_data, interval_seconds)
        timer.start()


    def run_osquery(self):
        all_osquery_data = {}

        for query, simplified_name in osquery_queries.items():
            try:
                osquery_output = subprocess.check_output(["/Applications/Vistar.app/Contents/MacOS/osqueryi", "--json", query], universal_newlines=True)
                osquery_data = json.loads(osquery_output)
                all_osquery_data[simplified_name] = osquery_data
            except subprocess.CalledProcessError as e:
                print(f"Error running osquery for query '{query}':", e)
            except Exception as e:
                print(f"Error processing query '{query}':", e)

        return all_osquery_data

    def send_data_to_api(self, data):
        try:
            response = requests.post(endpoint_url, json=data)
            if response.status_code == 201:
                print("Data sent successfully. Status code: 201")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Error sending data:", e)

    def update_menu(self):
        global sync_active
        self.start_icon = "/Applications/Vistar.app/Contents/Resources/toggle_on.png"
        self.stop_icon="/Applications/Vistar.app/Contents/Resources/toggle_off.png"
        if sync_active:
            self.menu['Start Sync'].title = 'Stop Sync'
            self.menu['Start Sync'].icon = self.start_icon
            # self.menu(rumps.notification('Stop Sync','Start data sent'))
        else:
            self.menu['Start Sync'].title = 'Start Sync'
            self.menu['Start Sync'].icon = self.stop_icon
            # rumps.notification('Start Sync', 'Stop vistar')

if __name__ == "__main__":
    VistarApp("Vistar App").quit_button = False  # Remove default Quit button
    VistarApp("Vistar App").run()
    