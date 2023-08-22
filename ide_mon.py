from pkg.procs_monitor import ProcMonitor
import codetime


def main():
    monitor = ProcMonitor()
    try:
        monitor.monitor_ide_processes()
        if monitor.active_ide_parent():
            codetime
    except:
        print("There was an error.  Check the logs for more information.")
