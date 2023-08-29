import json
import psutil as util
import platform
import time

from pathlib import Path

class ProcMonitor:
    def __init__(self, delay=5, ides=[], browsers=[]):
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

        ide_cnt = 0
        browser_cnt = 0

        conf_file = Path('~/.codetime/proc_config.json')
        if conf_file.is_file():
            ide_cnt, browser_cnt = self.load_conf()

        if ides:
            self.ides.append(ides)

        if browsers:
            self.browsers.append(browsers)

        if len(self.ides) > ide_cnt or len(self.browsers) > browser_cnt or not conf_file.is_file():
            self.save_conf()


    def load_conf(self, conf_file):
            conf_obj = json.load(conf_file)
            self.delay = conf_obj.delay
            self.ides.append(conf_obj.ides)
            self.browsers.append(conf_obj.browsers)
            return len(self.ides), len(self.browsers)

    def save_conf(self):
        cfg_file = Path('~/.codetime/proc_conf.json')
        cfg_obj = {}
        cfg_obj['delay'] = self.delay
        cfg_obj['ides'] = self.ides
        cfg_obj['browsers'] = self.browsers

        with open(cfg_file, 'w') as file:
            json.dump(cfg_obj, file, default=str)

    def detect_applications(self, program):
        pids = []
        previous_app = ''
        app = ''
        msg = '{program.upper}s' if 'i' in program else '{program}s'

        for application in self['{program}s']:
            app = application

            if not pids:
                pids = [
                    process.info['pid'] for process in util.process_iter(attrs=['pid', 'name']) if process.info['name'] == application
                ]
                previous_app = application
            else:
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
            if 'i' in program:
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
            if not self.detect_applications('ide'):
                time.sleep(self.delay)


    def save_config(self):
        if self.ides:
            pass
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
