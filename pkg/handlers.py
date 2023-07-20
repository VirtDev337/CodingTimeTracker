import argparse
import pkg.codetime as codetime
import os
import time
import psutil as util
import watchdog.events as events
import watchdog.observers as observers

from pathlib import Path


class VSCodeHandler(events.FileSystemEventHandler):
    def __init__(self, codetime):
        self.codetime = codetime.CodeTimeTracker()

    def on_created(self, event):
        project_name = os.path.basename(os.getcwd())

        # Load existing project data from JSON file
        self.codetime.load_projects()

        # Check if project already exists
        project = self.codetime.get_project(project_name)

        if project:
            print('Resuming tracking for project:', project_name)

        else:
            print('Detected VSCode startup for project:', project_name)
            project_name = input(
                'Enter project name or press enter to use default:')

            if not project_name:
                project_name = os.path.basename(os.getcwd())
            project = self.codetime.get_project(project_name)

        # Start tracking time spent in project
        project.add_time_spent(-project.start_time)
        project.start_time = time.time()
        project.update_created(project.date)

        # Watch for file modifications
        handler = FileModifiedHandler(project)
        observer = observers.Observer()
        observer.schedule(
            handler,
            project_name,
            recursive=True
        )
        observer.start()

    def on_closed(self, event, project_name=os.getcwd()):
        if os.path.basename(event.src_path) == 'Code - Insiders':
            project = self.codetime.get_project(project_name)
            project.add_time_spent(time.time() - project.start_time)
            project.update_last_modified(project.date)
            self.codetime.save_projects()


class FileModifiedHandler(events.FileSystemEventHandler):
    def __init__(self, project):
        self.project = project

    def on_modified(self, event):
        if not event.is_directory and event.src_path.startswith(self.project.name):
            rel_path = os.path.relpath(event.src_path, self.project.name)

            if rel_path not in self.project.modified_files:
                self.project.modified_files.append(rel_path)

    def on_closed(self, event):
        if not event.is_directory and event.src_path.startswith(self.project.name):
            rel_path = os.path.relpath(event.src_path, self.project.name)

            if rel_path in self.project.modified_files:
                self.project.modified_files.remove(rel_path)
