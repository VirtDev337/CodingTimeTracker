import codetime
import daemon

from pkg.procs_monitor import ProcMonitor

with daemon.DaemonContext():
    monitor = ProcMonitor()
    try:
        monitor.monitor_processes()
        if monitor.current_ide:
            codetime.run()
    except Exception as err:
        print("There was an error:\n{err}.")
