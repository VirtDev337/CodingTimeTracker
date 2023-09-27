import pkg.codetime_gui as codetime_gui
import codetime_cli as codetime_cli
import daemon

from pkg.procs_monitor import ProcMonitor

def monitor(default='gui'):
    with daemon.DaemonContext():
        monitor = ProcMonitor()
        try:
            monitor.monitor_processes()
            codetime_{default}
        except Exception as err:
            print("There was an error:\n{err}.")

