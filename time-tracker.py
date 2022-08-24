#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import json
import fpdf
import pandas
import psutil
import codecs
import keyboard
import threading
import subprocess
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig

def get_active_window_title():
    # Returns the title of the window in focus using the `xprop` command
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None
    # Finds and returns the name property for the active window
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").decode('UTF-8').strip('"')
    return None


class Tracker():
    date = ''
    time = ''
    project_name = ''
    edited = []
    research_names = []
    active = 0
    research = 0
    active_time = [] 
    research_time = []
    
    def __init__(self, pname = get_active_window_title()):
        self.date = time.strftime('%b %d, %Y') # 'Oct 18, 2010'
        self.time = time.strftime('%I:%M%p') # '1:36PM'
        self.project_name = pname.split(' - ')[1]
    
    def __str__(self):
        return self.project_name
    
    def process(self):
        global sleep
        time = {
            'active_start': self.active_time.pop(0),
            'active_end': self.active_time.pop(-1),
            'active': 0,
            'research': 0,
            'breaks': []
        }
        for break_pair in self.active_time.slice[0::3]:
            if not len(break_pair) == 1:
                print(break_pair)
                
                for research_pair in self.research_time.slice[0::3]:
                    if not len(research_pair) == 1:
                        
                        if break_pair[0] + sleep == research_pair[0]:
                            time['research'] += research_pair[1] - research_pair[0]
                            self.research_time.pop(research_pair[0])
                            self.research_time.pop(research_pair[1])
                        
                        else:
                            time['breaks'].append(break_pair[1] - break_pair[0])
                            self.active_time.pop(break_pair[0])
                            self.active_time.pop(break_pair[1])
        
        active = (time['active_end'] - time['active_start']) - time['research'] - time['breaks']
        self.active = active / 60 if active / 60 < 60 else active / 60 / 60
        self.research = time['research'] / 60 if time['research'] / 60 < 60 else time['research'] / 60 / 60
    
    def save_data(self, history):
        history.projects.append(self)


class History():
    date = ''
    projects = []
    
    def __init__(self):
        self.date = time.strftime('%b %d, %Y') # 'Oct 18, 2010'
    
    def __str__(self):
        return self.date
    
    def save_data(self, dir = '~/Documents', fname = '.time-track.json'):
        json_object = json.dumps(self, indent = 4)
        if '~/Documents' == dir:
            dir = os.path.join(dir, 'timetracker')
            if not os.exists(dir):
                os.makedir(dir)
                os.chdir(dir)
        
        jreport = os.join.path(dir, fname)
        if os.exists(jreport):
            with open(jreport, 'a') as doc:
                doc.write(json_object)
        else:
            with open(jreport, 'w') as doc:
                doc.write(json_object)
        self.create_pdf()
    
    def create_pdf(self, dir = '~/Documents/timetracker', fname = 'time-track'):
        dataframe = pandas.DataFrame()
        dataframe['minutes'] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        dataframe['hours'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for project in self.projects:
            if time.strftime('%b %d, %Y') == project.date:
                dataframe['time'] = dataframe['hours'] if type(project.active_time) == float else dataframe['minutes']
                dataframe['active'] = (project.project_name, project.active_time,)
                dataframe['research'] = (project.project_name, project.research_time,)
                dataframe['sites'] = (project.project_name, project.research_names,)
                
                title("Coding Time Tracker")
                xlabel('Coding & Research')
                ylabel('Time')
                
                c = [2.0, 4.0, 6.0, 8.0]
                m = [x - 0.5 for x in c]

                xticks(c, dataframe['Question'])

                bar(m, dataframe['active'], width=0.5, color="#91eb87", label="Mike")
                bar(c, dataframe['research'], width=0.5, color="#eb879c", label="Charles")
    
    def generate_report(date = time.strftime('%b %d, %Y'), project_name = ''):
        pass


def xprop_exists(): 
    # Validates that his is a Linux system and it has the xprop command
    return True if 'xprop' in os.system('xprop -version') else False


def toggle_timer():
    # Returns the start and stop times when VSCode loses focus and regains it
    return time.time()


def get_vscode_workspace_directory(name):
    return name.split(' - ')[1]


def check_process_running(process_name):
    # Checking if there is any running process that contains the given name process_name.
    # Iterate over the running processes
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
            pass
    return False;


def keyboard_monitor():
    # Tracks keypresses, without recording, to determine idle status
    global timeout
    while(check_process_running('code')):
        if keyboard.read_key():
            print('you pressed a key')
            timeout = time.time() + 180


def focus_monitor(tracker_obj, history_obj):
    # Tracks the time spent in an application window (Linux only currently)
    global sleep
    browsers = ['Firefox', 'Chrome', 'Safari', 'Opera', 'Edge', 'Internet Explorer',]
    if(xprop_exists()):
        # If xprop exists, it is a linux machine
        if(check_process_running('code')):
            # If code is running, record the start time
            if('Visual Studio Code' in get_active_window_title()):
                tracker_obj.active_time.append(toggle_timer())
                idle = False
                recorded = False
                # Continue as long as VSCode is running
                while(check_process_running('code')):
                    time.sleep(sleep)
                    active_window = get_active_window_title()
                    
                    if('Visual Studio Code' in active_window):
                        # Disassemble the active window title in order to get the file being edited and project name
                        f, project, app = active_window.split(' - ')
                        print('\n' + f + '  ' + project + '  ' + app + '\n')
                        
                        if project not in tracker_obj.project_name:
                            history_obj.append(tracker_obj)
                            tracker_obj = Tracker(pname = project)
                        
                        if(f not in tracker_obj.edited):
                            tracker_obj.edited.append(f)
                    
                    if(not 'Visual Studio Code' in active_window and not idle):
                        tracker_obj.active_time.append(toggle_timer())
                        idle = True
                    
                    elif('Visual Studio Code' in active_window and idle):
                        tracker_obj.active_time.append(toggle_timer())
                        tracker_obj.research_time.append(toggle_timer())
                        idle = False
                        recorded = False
                    
                    elif('Visual Studio Code' not in active_window and idle and not recorded):
                        print(active_window)
                        tracker_obj.research_time.append(toggle_timer())
                        if(active_window in browsers):
                            tracker_obj.research_names.append(f"{active_window}")
                            recorded = True
                    
                    elif('Visual Studio Code' not in active_window and active_window not in tracker_obj.research_names):
                        tracker_obj.research_names.append(f"{active_window}")
                    print(tracker_obj.project_name)
                    print(tracker_obj.active_time)
                    print(tracker_obj.research_time)
                    print(tracker_obj.research_names)
                
                tracker_obj.process()
                tracker_obj.save_data(history_obj)
                history_obj.save_data()
                exit()


if __name__ == "__main__":
    sleep = 3
    timeout = time.time() + 180
    projects = History()
    tracker = Tracker()
    # thread1 = threading.Thread(target = keyboard_monitor)
    thread2 = threading.Thread(target = focus_monitor, args = (tracker,))
    # thread1.start()
    # print('thread 1 started')
    thread2.start()
    print('thread 2 started')



        
    
    
# FIXME: Track key presses, without recording them
# DONE: Accesses and records the directory being accessed (to differentiate between projects)
# FIXME: Ability to edit the project name
# DONE: Keeps track of web access (whether a browser is in focus) for research and tracks the time seperately.
# TODO: Record site URI for time tracking
# ToDo: When vscode is closed, assemble data into json and write to new/existing file
# ToDo: Assemble report for viewing (cli command? pdf? calc? md?)