import gui
import cli
import daemon
import subprocess

from pkg.procs_monitor import ProcMonitor

def monitor():
    with daemon.DaemonContext():
        monitor = ProcMonitor()
        try:
            monitor.monitor_processes()
            monitor.on_ide_start()
        except Exception as err:
            print("There was an error:\n{err}.")

