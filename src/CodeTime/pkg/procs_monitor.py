import json
import psutil as util
import platform
import re
import time
import os
import subprocess

from pathlib import Path



class ProcMonitor:
    def __init__(self, delay=5, interf='gui'):
        self.active_codetime = False
        self.default_interface = interf
        self.active_ide_parent = ''
        self.delay = delay
        self.ides = [
            'code',
            'codium',
            'rstudio'
        ]
        self.browsers = [
            'Firefox',
            'Google Chrome',
            'Brave'
        ]
        self.current_ide = ''
        self.current_browser = ''

    def on_created(self, ides=[], browsers=[]):
        ide_count = 0
        browser_count = 0

        conf_file = Path(
            os.path.expanduser('~'),
            '.codetime',
            'proc_config.json'
        )
        if conf_file.is_file():
            ide_count, browser_count = self.load_conf(conf_file)

        if ides:
            self.ides.append(ides)

        if browsers:
            self.browsers.append(browsers)

        if len(self.ides) > ide_count or len(self.browsers) > browser_count or not conf_file.is_file():
            self.save_conf()

    def load_conf(self, conf_file):
            conf_obj = json.load(conf_file)
            self.delay = conf_obj.delay
            self.ides.append(conf_obj.ides)
            self.browsers.append(conf_obj.browsers)
            return len(self.ides), len(self.browsers)

    def save_conf(self):
        cfg_file = Path(
            os.path.expanduser('~'),
            '.codetime',
            'proc_config.json'
        )
        cfg_obj = {}
        cfg_obj['delay'] = self.delay

        for ide in self.ides:
            coded = "code|codium|rstudio"
            if not re.match(coded, ide):
                cfg_obj['ides'].append(ide)

        for browser in self.browsers:
            coded = "firefox|chrome|brave"
            if not re.match(coded, browser):
                cfg_obj['browsers'].append(browser)

        with open(cfg_file, 'w') as file:
            json.dump(cfg_obj, file, default=str)

    def get_ide_parent(self):
        # Iterate over the applications defined in the initilization of the ProcHandler
        for pid in self.ides[self.current_ide]['pids']:
            try:
                process = util.Processdocs(pid)
                if not process.name in process.parent().name:
                    self.active_ide_parent = { process.name: pid}
            except util.NoSuchProcess or util.AccessDenied as err:
                print("There is a problem getting the parent process: " + err)

    def is_gui(self):
        pass

    def detect_codetime(self):
        for process in util.process_iter(attrs=['pid', 'name']):
            if 'codetime' in process.info['name']:
                return True
        return False

    def detect_application(self, program):
        pids = []
        previous_app = ''
        app = ''
        msg = '{program.upper}s' if 'ide' in program else '{program.title}s'

        for application in self['{program}s']:
            app = application

            if not pids:
                pids = [
                    process.info['pid'] for process in util.process_iter(attrs=['pid', 'name']) if process.info['name'] == application
                ]
                previous_app = application
            elif pids and application == previous_app:
                application = input(
                    'At least two {msg} are running, {previous_app} and {application}, whcih would you like to track?'
                )
                pids = [
                    process.info['pid'] for process in util.process_iter(attrs=['pid', 'name']) if process.info['name'] == application
                ]
                app = application
                break
        self.active_codetime = self.detect_codetime()
        if pids:
            self['current_{program}'] = app
            self[app]['pids'] = pids
            if 'ide' in program:
                self.get_ide_parent()
            return True
        return False

    def monitor_processes(self):
        while not self.active_idocsde_parent:
            active = False
            for ide in self.ides:
                if self.detect_application(ide):
                    active = True

            if not active:
                time.sleep(self.delay)

    def on_ide_start(self):
        if not self.active_codetime:
            # TODO: Create cache_monitor method
            self.cache_monitor()
            subprocess.call(
                'python3',
                'codetime_{self.default_interface}.py',
                )
        # TODO: Pass current IDE and any Browser information to codetime_gui/cli.py.  Convert the objects to dictionary (text) or save the info to a cache file and load it from codetime_ application.

    def on_ide_close(self):
        pass # TODO: save browser info in codetime object.

    def to_dict(self):
        return {
            'ide': {
                'name': self.current_ide,
                'pids': self[self.current_ide]['pids']
            },
            'browser': {
                'name': self.current_browser,
                'pids': self[self.current_browser]['pids']
            }
        }

    # if __name__ == "__main__":
    #     monitoring_interval = 5  # seconds
    #     try:
    #         monitor_ide_processes(monitoring_interval)
    #     except KeyboardInterrupt:
    #         print("Monitoring stopped.")
