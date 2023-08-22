import handlers
import json
import os
import time
import re
import watchdog.observers as observers

from datetime import date, datetime, timedelta
from pathlib import Path
from project import Project
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib import colors
from trackers import BrowserTracker


class CodeTime:
    def __init__(self, process=None):
        self.projects = {}
        self.projects_dir = ''
        self.verbose = False
        self.ide_process = process

    # ----------------------------------------------
    # ------------------ Observer ------------------
    # ----------------------------------------------
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

    # ----------------------------------------------
    # -------------- Argument Handler --------------
    # ----------------------------------------------
    def help():
        print(
            "\nCode Time records time spent in the IDE and internet browsers automatically.  It tracks the time spent and the project (directory by default) you are working in, the files modified and the URL's visited for research on your project." +
            "\n\nUsage:  code_time.py [-a | --argument]\n" +
            "\n\t-c --complete\tToggles projects status for active tracking.\n\t\t\tSeveral projects can be specified using a space delimited list in quotes.\n\t\t\ti.e.: \"codetime website tic-tac-toe-game\"" +
            "\n\n\t-d --date\tThe date used to create a summary report." +
            "\n\n\t-g --gui\tStart the graphic user interface for Code Time." +
            "\n\n\t-h --help\tThis help message." +
            "\n\n\t-p --project\tThe name of the project to create a summary report.\nUsed with other arguments to define a single or 'list' of project(s) for that operation." +
            "\n\n\t-r --remove\tUsed in conjuction with '-p' to remove all data associated with the project(s) specified.\n\t\t\tSeveral projects can be specified using a space delimited list in quotes.\n\t\t\ti.e.: \"codetime react_extension calculator\"" +
            "\n\n\t-s --status\tUsed in conjuction with '-p' to display the status associated with the project specified." +
            "\n\n\t-v --verbose\tToggles the inclusion of files modified and URL's visited for the project or date provided.\n\t\t\tThis is included by default with project reports, not with date reports.\n\t\t\tCombination report of both project and date also includes this by default.\n"
        )

    def toggle_complete(self):
        if self.complete:
            self.complete = False
        else:
            self.complete = True

    def toggle_verbose(self):
        if self.verbose:
            self.verbose = False
        else:
            self.verbose = True

    # ----------------------------------------------
    # ------------- Project Management -------------
    # ----------------------------------------------
    def create_project(self, name):
        print('Detected VSCode startup for project:', name)
        designation = input(
            'Enter project name or press enter to use the default (project directory):'
        )
        if designation:
            name = designation

        return Project(name)

    def get_project(self, name):
        if name not in self.projects:
            return None

        print(
            'Resuming tracking for project:',
            self.projects['name']
        )
        return self.projects[name]

    def delete_project(self, project_name):
        project = self.get_project(project_name)
        # Delete project on disk? shutil.rmtree?
        self.projects.delete(project)

    def save_projects(self):
        projects = [project.to_dict() for project in self.projects.values()]
        path = os.path.join(
            os.path.expanduser('~'),
            '.codetime',
            'projects.json'
        )
        with open(path, 'w') as f:
            json.dump(projects, f, default=str)

    def load_projects(self):
        path = os.path.join(
            os.path.expanduser('~'),
            '.codetime',
            'projects.json'
        )
        with open(path, 'r') as file:
            self.projects = json.load(file)

    def project_status(self, project_name, verbose=False):
        project = self.get_project(project_name)
        print(project['name'] + "\n")
        pattern = 'name|dir|created|complete'

        if verbose:
            pattern += '|date|time_spent|last_modified_date'

        for key in project:
            if re.fullmatch(pattern, key):
                print(key + ": " + self.projects[project][key] + "\n")

    def get_datetime(self, datetime):
        # Parse date/time
        datetime_obj = None
        time_step = None
        try:
            datetime_obj = datetime.strptime(datetime, '%Y-%m-%d')
            time_step = timedelta(days=1)

        except ValueError:
            try:
                datetime_obj = datetime.strptime(datetime, '%H:%M')
                time_step = timedelta(minutes=60)

            except ValueError:
                print('Invalid date/time format, please use YYYY-MM-DD or HH:MM')
                return

        return datetime_obj, time_step

    # ----------------------------------------------
    # ------------------ Reports -------------------
    # ----------------------------------------------
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
        datetime_obj, time_step = self.get_datetime(date_time)

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

    def date_project_report(self, date, project_name):
        datetime_obj, time_step = self.get_datetime(date)

        project = self.get_project(project_name)
        # Set up canvas
        c = canvas.Canvas(
            project.name + date + '.pdf',
            pagesize=portrait(letter)
        )
        c.setTitle(project.name + ' ' + date + ' CodeTime Report')
