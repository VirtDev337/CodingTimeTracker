import argparse
import pkg.codetime_gui as gui
import attempts.reports
import psutil as util
import ide_mon

from pkg.trackers import BrowserTracker
from pkg.codetime_lib import CodeTime
from typing import List, Dict

def run():
    # Initialize CodeTime instance
    codetime = CodeTime()

    # Define command line arguments
    parser = argparse.ArgumentParser(
        prog='codetime',
        description="\nCode Time records time spent in the IDE and internet browsers automatically.  It tracks the time spent and the project (directory by default) you are working in, the files modified and the URL's visited for research on your project."
    )
    parser.add_argument(
        '-b',
        '--browser',
        type=str,
        nargs='?',
        help='Add the process name of a browser.\n(Firefox, Chrome and Brave are included).'
    )
    parser.add_argument(
        '-c',
        '--complete',
        action='store_true',
        default=False,
        help='Toggles projects status for active tracking.'
    )
    parser.add_argument(
        '-d',
        '--date',
        type=str,
        help='Generate PDF report for date/time (YYYY-MM-DD or HH:MM).\nCan be used in conjunction with -p to specify a time period of that project.'
    )
    parser.add_argument(
        '-D',
        '--delay',
        type=str,
        help='The interval between checks for an active IDE process (in seconds).'
    )
    parser.add_argument(
        '-g',
        '--gui',
        action='store_true',
        default=False,
        help='Start the graphical user interface for Code Time.'
    )
    # parser.add_argument(
    #     '-h',
    #     '--help',
    #     action=CodeTime().help(),
    #     help='This help message.'
    # )
    parser.add_argument(
        '-i',
        '--ide',
        type=str,
        nargs='?',
        help='Add the process name of an IDE.\n(VSCode, Codium and RStudio are included).'
    )
    parser.add_argument(
        '-p',
        '--project',
        type=str,
        nargs='?',
        help='Generate PDF report for the project provided.\nUsed with other arguments to define a single or "list" of project(s) for that operation.'
    )
    parser.add_argument(
        '-r',
        '--remove',
        action='store_true',
        default=False,
        help='Used in conjuction with "-p" to remove all data associated with the project specified.\nSeveral projects can be specified using a space delimited list in quotes. i.e.:\n"codetime react_extension calculator"'
    )
    parser.add_argument(
        '-s',
        '--status',
        action='store_true',
        default=False,
        help='Used in conjuction with "-p" to display the status associated with the project specified.'
    )
    parser.add_argument(
        '-V',
        '--verbose',
        action='store_true',
        default=False,
        help='Used in conjuction with "-p" to display the status associated with the project specified.'
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 2.4'
    )
    args = parser.parse_args()

    print(args)
    if len(args) > 0:
        if all(
                key in args for key in [
                    'p',
                    'r'
                ]
            ) or all(
                key in args for key in [
                    'project',
                    'remove'
                ]
        ):

            if len(args['project'].split(" ")) > 1:
                for task in args['project']:
                    codetime.delete_project(task)
            else:
                codetime.delete_project(args['project'])

        elif all(
            key in args for key in [
                'p',
                's',
            ]
        ) or all(
            key in args for key in [
                'project',
                'status'
            ]
        ):
            verbose = True if 'V' in args or 'Verbose' in args else False

            if len(args['project'].split(" ")) > 1:
                for task in args['project'].split(" "):
                    codetime.project_status(task, verbose)
            else:
                codetime.project_status(args['project'], verbose)

        elif all(
            key in args for key in [
                'p',
                'd',
            ]
        ) or all(
            key in args for key in [
                'project',
                'date'
            ]
        ):
            if len(args['project'].split(" ")) > 1:
                for task in args['project'].split(" "):
                    codetime.date_project_report(args['date'], task)
            else:
                codetime.date_project_report(args['date'], args['project'])

        elif 'date' in args or 'd' in args:
            codetime.date_report(args['date'])

        elif 'project' in args or 'p' in args:
            if len(args['project'].split(" ")) > 1:
                for task in args['project'].split(" "):
                    codetime.project_report(task)
            else:
                codetime.project_report(args['project'])
        elif 'g' in args or 'gui' in args:
            codetime.stop()
            gui
            exit()
    else:
        codetime.ide_process = ide_mon.main()
        codetime.start()


if __name__ == '__main__':
    run()