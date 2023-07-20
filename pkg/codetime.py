import handlers
import json
import os
import time
import watchdog.observers as observers
import webbrowser

from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse as parse


class CodeTimeTracker:
    def __init__(self):
        self.projects = {}
        self.current_project = ""
        self.current_file = ""
        self.start_time = 0

    def start_project(self, project_name: str):
        self.current_project = project_name
        self.projects[self.current_project] = {
            "files": {},
            "time": 0
        }
        self.start_time = time.time()
        print(f"Started tracking project {self.current_project}")

    def end_project(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.projects[self.current_project]["time"] += elapsed_time

        with open(os.path.expanduser("~/codetime/projects.json"), "w") as file:
            json.dump(self.projects, file, indent=4)

        print(f"Stopped tracking project {self.current_project}")

    def update_file(self, file_path: str):
        if self.current_project:

            if file_path not in self.projects[self.current_project]["files"]:
                self.projects[self.current_project]["files"][file_path] = 0

            self.projects[self.current_project]["files"][file_path] += 1
            self.current_file = file_path

    def print_projects(self):
        for project_name, project_data in self.projects.items():
            print(f"{project_name}: {project_data['time']}")

            for file_path, file_count in project_data["files"].items():
                print(f"    {file_path}: {file_count}")


class BrowserTracker:
    def __init__(self):
        self.browsers = {
            "Firefox": {},
            "Chrome": {}
        }
        self.current_browser = ""
        self.current_tab = ""
        self.start_time = 0

    def start_browser(self, browser_name: str):
        self.current_browser = browser_name
        self.browsers[self.current_browser] = {}
        self.start_time = time.time()
        print(f"Started tracking {self.current_browser}")

    def end_browser(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        if self.current_browser:

            if self.current_tab not in self.browsers[self.current_browser]:
                self.browsers[self.current_browser][self.current_tab] = 0

            self.browsers[self.current_browser][self.current_tab] += elapsed_time

            with open(os.path.expanduser("~/codetime/browsers.json"), "w") as file:
                json.dump(self.browsers, file, indent=4)

            print(f"Stopped tracking {self.current_browser}")

    def update_tab(self, url: str):
        if self.current_browser:
            parsed_url = parse(url)
            self.current_tab = parsed_url.netloc
            self.start_time = time.time()

    def print_browsers(self):
        for browser_name, browser_data in self.browsers.items:
            print(f"{browser_name}: {browser_data}")


#     Use a Python package such as psutil to monitor running processes and detect when VSCode or a web browser is started.
    # When VSCode is started, record the current working directory as the project name, and prompt the user to confirm or edit the project name if desired.
    # Use watchdog to monitor file system events in the project directory and track modified files.
    # Record the time spent in VSCode using the time package, and store this information in a class object.
    # When VSCode is closed, write the class object to a JSON file in the ~/codetime directory.
    # Repeat steps 1-5 for the web browser.
    # Accept command-line arguments to run the program as a service and to generate PDF reports by project or date/time.


class Project:
    def __init__(self, name):
        self.name = name
        self.modified_files = set()
        self.time_spent = 0
        self.date = date.today()
        self.last_modified_date = ""
        self.created = ""

    def add_modified_file(self, path):
        self.modified_files.add(path)

    def add_time_spent(self, seconds):
        self.time_spent += seconds

    def update_last_modified(self, date):
        self.last_modified_date = date

    def update_created(self, date):
        if not self.created:
            self.created = date

    def to_dict(self):
        return {
            'name': self.name,
            'modified_files': list(self.modified_files),
            'time_spent': self.time_spent,
            'date': self.date,
            'last_modified_date': self.last_modified_date,
            'created': self.created
        }


class CodeTime:
    def __init__(self):
        self.projects = {}
        self.projects_dir = Path(os.getcwd()).parent

    def start(self):
        observer = observers.Observer()

        # Watch for VSCode startup
        vscode_handler = handlers.VSCodeHandler(self)
        observer.schedule(
            vscode_handler,
            os.path.expanduser('~'),
            recursive=True
        )

        # Watch for web browser activity
        browser_handler = BrowserTracker(self)
        observer.schedule(
            browser_handler,
            None
        )

        observer.start()

    def stop(self, observer=observers.Observer()):
        observer.stop()
        observer.join()

    def get_project(self, name):
        if name not in self.projects:
            self.projects[name] = Project(name)
        return self.projects[name]

    def save_projects(self):
        projects = [p.to_dict() for p in self.projects.values()]
        path = os.path.join(
            os.path.expanduser('~'),
            'codetime',
            'projects.json'
        )

        with open(path, 'w') as f:
            json.dump(projects, f)
