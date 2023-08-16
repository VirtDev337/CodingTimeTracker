import time
import psutil as util
import platform


class ProcMonitor:
    def __init__(self, delay=1, applications=[]):
        self.delay = delay
        self.ide_apps = [
            "code",
            "codium",
            "rstudio"
        ]
        self.active_ide_parent = ''
        self.ide_pids = []

        if applications:
            self.ide_apps.append(applications)

    def ide_is_running(self):
        for app in self.ide_apps:
            for process in util.process_iter(attrs=['pid', 'name']):
                if app.capitalize() in process.info['name'] or process.info['name'] == app.lower():
                    self.ide_pids.append.process.pid()

        if self.ide_pids:
            self.get_ide_parent()
            return True

        return False

    def get_ide_parent(self):
        ide_process = ''

        # Iterate over the applications defined in the initilization of the ProcHandler
        for pid in self.ide_pids:
            try:
                process = util.Process(pid)
                if not process.name.lower() in process.parent().name:
                    self.active_ide_parent = process
            except util.NoSuchProcess or util.AccessDenied as err:
                print("There is a problem getting the parent process: " + err)

    def monitor_ide_processes(self):
        while not self.active_ide_parent:
            if not self.ide_is_running():
                time.sleep(self.delay)

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
        browser_pids = []

        if platform.system() == "Darwin":
            browser_pids = [
                p.info['pid'] for p in util.process_iter(
                    attrs=['pid', 'name']) if p.info['name'] in browsers
            ]
        elif platform.system() == "Linux":
            browser_pids = [
                p.info['pid'] for p in util.process_iter(
                    attrs=['pid', 'name']) if p.info['name'] in browsers]

        if browser_pids:
            return True
        return False
