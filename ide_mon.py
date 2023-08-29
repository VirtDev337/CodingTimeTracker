import codetime
import daemon

from pkg.procs_monitor import ProcMonitor

with daemon.DaemonContext():
    monitor = ProcMonitor()
    try:
        monitor.monitor_processes()
        codetime.run()
    except:
        print("There was an error.  Check the logs for more information.")
