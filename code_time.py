import argparse
import pkg.codetime as codetime
import pkg.codetime_gui as gui
import attempts.reports
import psutil as util

from typing import List, Dict


# Initialize CodeTime instance
codetime = codetime.CodeTimeTracker()

# Define command line arguments
parser = argparse.ArgumentParser(
    description='Track coding projects and browser usage'
)
parser.add_argument(
    '-p',
    '--project',
    type=str,
    help='Generate PDF report for project name'
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
args = parser.parse_args()

if __name__ == '__main__':
    if len(args) > 0:
        if "help" in args or "h" in args:
            codetime.help()
        elif 'project' in args or 'p' in args and 'date' in args or 'd' in args:
            codetime.date_project_report(args['date'], args['project'])
        elif 'date' in args or 'd' in args:
            codetime.date_report(args['date'])
        elif 'project' in args or 'p' in args:
            codetime.project_report(args['project'])

        exit()
    else:
        codetime.start()
