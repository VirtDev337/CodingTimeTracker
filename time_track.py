import argparse
import pkg.codetime as codetime
import pkg.codetime_gui as gui
import pkg.reports
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
    '--datetime',
    type=str,
    help='Generate PDF report for date/time (YYYY-MM-DD or HH:MM)'
)
args = parser.parse_args()
