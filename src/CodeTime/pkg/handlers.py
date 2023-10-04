import argparse
import os
import time
import psutil as util
import watchdog.events as events
import watchdog.observers as observers

from src.CodeTime.mon import monitor
from pathlib import Path


class IdeHandler(events.FileSystemEventHandler):
    def __init__(self, codetime):
        self.codetime = codetime

    def on_created(self, event):
        cwd = self.ide_process.cwd() if self.ide_process else os.getcwd()

        project_name = os.path.basename(cwd)

        # Load existing project data from JSON file
        self.codetime.load_projects()

        # Check if project already exists
        project = self.codetime.get_project(project_name)

        if not project:
            project = self.codetime.create_project(project_name)

        self.codetime.current_project = project.name

        # Start tracking time spent in project
        project.add_time_spent(-project.start_time)
        project['start_time'] = time.time()
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
        if os.path.basename(event.src_path) == self.project.name or os.path.basename(event.src_path) == self.project.dir:
            project = self.codetime.get_project(project_name)
            project.add_time_spent(time.time() - project.start_time)
            project.update_last_modified(project.date)
            self.codetime.save_projects()
        # TODO: Is this the best way?
        self.codetime.stop()
        monitor()


class FileModifiedHandler(events.FileSystemEventHandler):
    def __init__(self, project):
        self.project = project

    def on_modified(self, event):
        rel_path = None

        if not event.is_directory and event.src_path.startswith(self.project.name):
            rel_path = os.path.relpath(
                event.src_path,
                self.project.name
            )
        elif not event.is_directory and event.src_path.startswith(self.project.dir):
            rel_path = os.path.relpath(
                event.src_path,
                self.project.dir
            )

        if rel_path:
            if rel_path not in self.project.modified_files:
                self.project.modified_files.append(rel_path)

    def on_closed(self, event):
        rel_path = None

        if not event.is_directory and event.src_path.startswith(self.project.name):
            rel_path = os.path.relpath(event.src_path, self.project.name)
        elif not event.is_directory and event.src_path.startswith(self.project.dir):
            rel_path = os.path.relpath(event.src_path, self.project.dir)

        if rel_path:
            if rel_path not in self.project.modified_files:
                self.project.modified_files.append(rel_path)

        return self.project
