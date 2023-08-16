from pkg.procs_monitor import ProcMonitor
import codetime


def main():
    monitor = ProcMonitor()
    monitor.monitor_ide_processes()
    if monitor.active_ide_parent:
        codetime
