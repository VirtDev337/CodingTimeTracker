import json
import psutil as util
import platform
import re
import time
import os

from pathlib import Path



class ProcMonitor:
    def __init__(self, delay=5):
        self.active_codetime = False
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

        if pids:
            self['current_{program}'] = app
            self[self['current_{program}']]['pids'] = pids
            if 'ide' in program:
                self.get_ide_parent()
            return True
        return False

    def get_ide_parent(self):
        # Iterate over the applications defined in the initilization of the ProcHandler
        for pid in self.ides[self.current_ide]['pids']:
            try:
                process = util.Process(pid)
                if not process.name in process.parent().name:
                    self.active_ide_parent = process
            except util.NoSuchProcess or util.AccessDenied as err:
                print("There is a problem getting the parent process: " + err)

    def monitor_processes(self):
        while not self.active_ide_parent:
            if not self.detect_application('ide'):
                time.sleep(self.delay)
        return self

    # if __name__ == "__main__":
    #     monitoring_interval = 5  # seconds
    #     try:
    #         monitor_ide_processes(monitoring_interval)
    #     except KeyboardInterrupt:
    #         print("Monitoring stopped.")


class ProcessMonitor:
    def __init__(self):
        pass

    def monitor_apps(self):
        while True:
            if self.detect_vscode():
                self.on_vscode_start()
            if self.detect_browser():
                self.on_browser_start()
            time.sleep(self.monitor_interval)

    def detect_vscode(self):
        ide_pids = [
            p.info['pid'] for p in util.process_iter(
                attrs=['pid', 'name']) if p.info['name'] == 'code']
        if ide_pids:
            self.ide_pids = ide_pids
            return True
        return False

    def detect_browser(self):
        browsers = [
            'Firefox',
            'Google Chrome',
            'Brave'
        ]
        pids = []
        previous_browser = ''
        net_browser = ''

        for browser in self.browsers:
            net_browser = browser
            if not pids:
                pids = [
                    process.info['pid'] for process in util.process_iter(
                        attrs=['pid', 'name']
                    ) if process.info['name'] == browser
                ]
                previous_browser = browser
            else:
                browser = input(
                    'At least two internet browsers are running, {previous_browser} and {browser}, whcih would you like to track?'
                )

        if pids:
            return True
        return False
