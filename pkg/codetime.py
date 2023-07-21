import handlers
import json
import os
import time
import watchdog.observers as observers
import webbrowser

from datetime import date, datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib import colors
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

    def help():
        print(
            "\nCode Time records time spent in the IDE and internet browsers automatically.  It tracks the time spent and the project (directory by default) you are working in, the files modified and the URL's visited for research on your project." +
            "\n\nUsage:  code_time.py [-a | --argument]" +
            "\n\t-d --date\tThe date used to create a summary report." +
            "\n\t-h --help\tThis help message." +
            "\n\t-p --project\tThe name of the project to create a summary report."
            "\n\t-v --verbose\tToggles the inclusion of files modified and URL's visited for the project or date provided.\n\t\t\tThis is included by default with project reports, not with date reports.\n\t\t\tCombination report of both project and date also includes this by default.\n"
        )

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

    def project_report(self, project_name):
        project = self.get_project(project_name)
        # Set up canvas
        canvas = canvas.Canvas(
            project.name + '.pdf',
            pagesize=landscape(letter)
        )
        canvas.setTitle(project.name + ' CodeTime Report')

        # Set up grid
        y_grid = [i * inch for i in range(1, 13)]
        x_grid = [i * inch for i in range(1, len(project.modified_files) + 2)]
        canvas.grid(x_grid, y_grid)

        # Draw time spent data
        max_time = project.get_total_time_spent()
        time_step = max_time / 12

        for i in range(12):
            canvas.drawString(
                0.5 * inch, (12 - i) * inch,
                '{:.2f}'.format(time_step * i)
            )
        canvas.drawString(
            0.5 * inch, 0.5 * inch,
            'Time spent (hours)'
        )

        # Draw modified files data
        for i, modified_file in enumerate(project.modified_files):
            canvas.drawString(
                (i + 1.5) * inch,
                0.25 * inch,
                modified_file
            )

        # Draw browser usage data
        browser_usage = project.get_browser_usage()
        for i, usage in enumerate(browser_usage):
            canvas.drawString(
                (i + 1.5) * inch,
                0.75 * inch,
                '{} ({:.2f} min)'.format(
                    usage['title'],
                    usage['time'] / 60
                )
            )

        # Save and close canvas
        canvas.showPage()
        canvas.save()

    def date_report(self, date_time):
        # Parse date/time
        try:
            datetime_obj = datetime.strptime(date_time, '%Y-%m-%d')
            time_step = timedelta(days=1)

        except ValueError:
            try:
                datetime_obj = datetime.strptime(date_time, '%H:%M')
                time_step = timedelta(minutes=60)

            except ValueError:
                print('Invalid date/time format, please use YYYY-MM-DD or HH:MM')
                return

        # Set up canvas
        c = canvas.Canvas(
            date_time + '.pdf',
            pagesize=portrait(letter)
        )
        c.setTitle(date_time + ' CodeTime Report')

        # Set up grid
        y_grid = [i * inch for i in range(1, len(self.projects) + 2)]
        x_grid = [i * inch for i in range(1, 13)]
        c.grid(x_grid, y_grid)

        # Draw project data
        for i, project in enumerate(self.projects):
            time_spent = project.get_time_spent(
                datetime_obj,
                datetime_obj + time_step
            )
            if time_spent > 0:
                c.drawString(
                    0.5 * inch,
                    (len(self.projects) - i) * inch,
                    project.name
                )
                c.rect(
                    1 * inch,
                    (len(self.projects) - i + 0.5) * inch,
                    time_spent / 60 * inch,
                    0.5 * inch,
                    fill=1
                )
                c.drawString(
                    (time_spent / 60 + 1) * inch,
                    (len(self.projects) - i) * inch,
                    '{:.2f} min'.format(time_spent)
                )

        # Save and close canvas
        c.showPage()
        c.save()

    def date_project_report(date, project_name):
        pass
