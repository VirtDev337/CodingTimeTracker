#!/mnt/vault/Development/Workspace/Code/Projects/TimeTracker/venv/bin/python3

import os
import re
import sys
import time
import getopt
import psutil
import keyboard
import optparse
import threading
import subprocess
from tracker import Tracker, get_active_window_title


def xprop_exists():
    # Validates that this is a Linux system and it has the xprop command
    output = subprocess.run(
        ['which', 'xprop'],
        capture_output=True,
        encoding='utf-8'
    )
    return True if 'xprop' in output.stdout else False


def toggle_timer():
    # Returns the start and stop times when VSCode loses focus and regains it
    return time.time()


def get_ide_workspace_directory(name):
    return name.split(' - ')[1]


def check_process_running(process_name):
    process_name = process_name.lower()
    # Checking if there is any running process that contains the given name process_name.
    # Iterate over the running processes
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name in proc.name().lower() or process_name == proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
            pass
    return False


def generate_report(date=time.strftime('%b %d, %Y'), project_name='', dir='~/Documents/timetracker'):
    jfile = os.path.join(dir, '.timetrack.json')
    with open(jfile, 'r') as doc:
        project_data = json.loads(doc)
        for key in project_data.keys():
            if project_name in key:
                pass


def keyboard_monitor():
    # Tracks keypresses, without recording, to determine idle status
    global TIMEOUT
    while (check_process_running('code')):
        if keyboard.read_key():
            print('you pressed a key')
            TIMEOUT = time.time() + 180


def focus_monitor(tracker_obj):
    print('focus_monitor')
    # Tracks the time spent in an application window (Linux only currently)
    global sleep
    browsers = [
        'Firefox',
        'Chrome',
        'Safari',
        'Opera',
        'Edge',
        'Internet Explorer',
    ]
    if (xprop_exists()):
        # If xprop exists, it is a linux machine
        if (check_process_running('code') or check_process_running('codium')):
            # print(get_active_window_title())
            # If code is running, record the start time
            if ('Visual Studio Code' in get_active_window_title() or 'VSCodium' in get_active_window_title):
                tracker_obj.active_time.append(toggle_timer())
                idle = False
                recorded = False
                # Continue as long as VSCode is running
                while (check_process_running('code') or check_process_running('codium')):
                    time.sleep(sleep)
                    active_window = get_active_window_title()
                    # print(active_window)
                    if ('Visual Studio Code' in active_window or 'VSCodium' in active_window):
                        # Disassemble the active window title in order to get the file being edited and project name
                        document, project, app = active_window.split(' - ')
                        # print('\n' + document + '  ' +
                        #       project + '  ' + app + '\n')

                        if project not in tracker_obj.name:
                            tracker_obj = Tracker(process_name=project)

                        if (document not in tracker_obj.edited):
                            tracker_obj.edited.append(document)

                    if (not 'Visual Studio Code' in active_window and not idle):
                        tracker_obj.active_time.append(toggle_timer())
                        idle = True

                    elif ('Visual Studio Code' in active_window and idle):
                        tracker_obj.active_time.append(toggle_timer())
                        tracker_obj.research_time.append(toggle_timer())
                        idle = False
                        recorded = False

                    elif ('Visual Studio Code' not in active_window and idle and not recorded):
                        # print(active_window)
                        tracker_obj.research_time.append(toggle_timer())
                        if (active_window in browsers):
                            tracker_obj.research_names.append(
                                f"{active_window}")
                            recorded = True

                    elif ('Visual Studio Code' not in active_window and active_window not in tracker_obj.research_names):
                        tracker_obj.research_names.append(f"{active_window}")
                    # print(tracker_obj.name)
                    # print(tracker_obj.active_time)
                    # print(tracker_obj.research_time)

                    print(tracker_obj.research_names)
                    tracker_obj.process()
                tracker_obj.save_data()
                exit()


def show_help():
    message = "python3 time-tracker.py [options] [directory] [file name]\n\n\tRunning the monitor without options will create the code tracker process and actively monitor time spent in VSCode.  Any time spent inside a browser, researching, is also tracked altogether.  Adding options allows you to print reports based on date and project.\n\n\t-h, -? or --help will result in this message being shown.  \n\t-r will allow you to create a report.  \n\t-d [date] will allow you to specify the date for a report.  \n\t-n [name] allows you to specify a name for the report."


if __name__ == "__main__":
    sleep = 3
    TIMEOUT = time.time() + 180
    DIR = '~/Documents/timetracker'
    # if (not os.path.exists(os.path.join(DIR, 'timetracker.db'))):
    #     create_db()
    # projects = History()
    tracker = Tracker()
    if not len(sys.argv) > 1:
        print('In first if: (if not len(sys.argv) > 1)')
        try:
            thread1 = threading.Thread(target=keyboard_monitor)
            thread2 = threading.Thread(
                target=focus_monitor, args=(tracker,))
            thread1.start()
            print('thread 1 started')
            thread2.start()
            print('thread 2 started')
        except:
            pass
    else:
        try:
            args, opts, lopts = getopt.getopt(sys.argv)
            if opts or lopts:
                if 'h' in opts or '?' in optparse or 'help' in lopts:
                    show_help()
            if args:
                date = args[0]
                project = args[1]
                # generate_report(date, project)
        except:
            pass


# if __name__ == "__main__":
#     sleep = 3
#     TIMEOUT = time.time() + 180
#     DIR = '~/Documents/timetracker'
#     # if (not os.path.exists(os.path.join(DIR, 'timetracker.db'))):
#     #     create_db()
#     projects = History()
#     tracker = Tracker()
#     if not sys.argv:
#         # thread1 = threading.Thread(target = keyboard_monitor)
#         thread2 = threading.Thread(
#             target=focus_monitor, args=(tracker, projects))
#         # thread1.start()
#         # print('thread 1 started')
#         thread2.start()
#         print('thread 2 started')
#     else:
#         try:
#             args, opts, lopts = getopt.getopt(sys.argv)
#             if opts or lopts:
#                 if 'h' in opts or '?' in optparse or 'help' in lopts:
#                     show_help()
#             if args:
#                 date = args[0]
#                 project = args[1]
#                 generate_report(date, project)
#         except:
#             pass


# FIXME: Track key presses, without recording them
# DONE: Accesses and records the directory being accessed (to differentiate between projects)
# FIXME: Ability to edit the project name
# DONE: Keeps track of web access (whether a browser is in focus) for research and tracks the time seperately.
# TODO: Record site URI for time tracking
# ToDo: When vscode is closed, assemble data into json and write to new/existing file
# ToDo: Assemble report for viewing (cli command? pdf? calc? md?)

'''
class MyClass():
    def __init__(self, param):
        self.param = param


def save(key, value, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value  # Using dict[key] to store
            mydict.commit()  # Need to commit() to actually flush the data
    except Exception as ex:
        print("Error during storing data (Possibly unsupported):", ex)


def load(key, cache_file="cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            # No need to use commit(), since we are only loading data!
            value = mydict[key]
        return value
    except Exception as ex:
        print("Error during loading data:", ex)


obj1 = MyClass(10)
save("MyClass_key", obj1)

obj2 = load("MyClass_key")

print(obj1.param, obj2.param)
print(isinstance(obj1, MyClass), isinstance(obj2, MyClass))
'''
