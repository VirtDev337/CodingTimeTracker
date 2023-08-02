import argparse
from pkg.trackers import BrowserTracker
from pkg.codetime import CodeTime
import pkg.codetime_gui as gui
import attempts.reports
import psutil as util

from typing import List, Dict


# Initialize CodeTime instance
codetime = CodeTime()

# Define command line arguments
parser = argparse.ArgumentParser(
    description='Track coding projects and browser usage'
)
parser.add_argument(
    '-c',
    '--complete',
    type=str,
    help='Toggles projects status for active tracking.'
)
parser.add_argument(
    '-d',
    '--date',
    type=str,
    help='Generate PDF report for date/time (YYYY-MM-DD or HH:MM)'
)
parser.add_argument(
    '-h',
    '--help',
    type=str,
    help='Generate PDF report for date/time (YYYY-MM-DD or HH:MM)'
)
parser.add_argument(
    '-p',
    '--project',
    type=str,
    help='Generate PDF report for project name'
)
parser.add_argument(
    '-r',
    '--remove',
    type=str,
    help='Used in conjuction with "-p" to remove all data associated with the project specified.'
)
parser.add_argument(
    '-s',
    '--status',
    type=str,
    help='Used in conjuction with "-p" to display the status associated with the project specified.'
)
parser.add_argument(
    '-v',
    '--verbose',
    type=str,
    help='Used in conjuction with "-p" to display the status associated with the project specified.'
)
args = parser.parse_args()

if __name__ == '__main__':
    if len(args) > 0:
        if ("help" in args or "h" in args):
            codetime.help()

        elif all(key in args for key in ['p', 'project', 'r', 'remove']):
            if len(args['project'].split(" ")) > 1:
                for task in args['project']:
                    codetime.delete_project(task)

            else:
                codetime.delete_project(args['project'])
        elif all(key in args for key in ['p', 'project', 's', 'status']):
            if len(args['project'].split(" ")) > 1:
                for task in args['project']:
                    codetime.project_status(task)

            else:
                codetime.project_status(args['project'])

        elif all(key in args for key in ['p', 'project', 'd', 'date']):
            codetime.date_project_report(args['date'], args['project'])

        elif 'date' in args or 'd' in args:
            codetime.date_report(args['date'])

        elif 'project' in args or 'p' in args:
            codetime.project_report(args['project'])

        codetime.start()

    else:
        pass
