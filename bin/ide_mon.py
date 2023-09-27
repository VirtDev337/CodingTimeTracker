import pkg.codetime_gui as codetime_gui
import codetime_cli as codetime_cli
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

