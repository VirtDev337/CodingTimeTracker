import os
import time
from datetime import date, datetime
from pkg.browser_lib import Browser


class Project:
    def __init__(self, name):
        self.name = name
        self.modified_files = {}
        self.time_spent = 0
        self.date = date.today()
        self.last_modified_date = ""
        self.created = ""
        self.complete = False
        self.dir = os.path.basename(os.getcwd())
        self.browser = Browser()

    def add_modified_file(self, path):
        self.modified_files.add(path)

    def add_time_spent(self, seconds):
        self.time_spent += seconds

    def update_last_modified(self):
        self.last_modified_date = self.date

    def update_created(self):
        if not self.created:
            self.created = self.date

    def to_dict(self):
        return {
            'name': self.name,
            'created': self.created,
            'complete': self.complete,
            'dir': self.dir,
            'time_spent': self.time_spent,
            'last_modified_date': self.last_modified_date,
            self.date: {
                'modified_files': list(self.modified_files),
                'browser': dict(self.browser.to_dict())
            }
        }
