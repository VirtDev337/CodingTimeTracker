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
import matplotlib.pyplot as plt

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


class Tracker ():
    project_name = ''
    edited = []
    research_names = []
    active = 0
    research = 0
    active_time = [] 
    research_time = []
    
    def __init__(self, pname = get_active_window_title()):
        self.project_name = pname.split(' - ')[1]
    
    def __str__(self):
        return self.project_name
    
    def process(self):
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
                        
                        if break_pair[0] + 10 == research_pair[0]:
                            time['research'] += research_pair[1] - research_pair[0]
                            self.research_time.pop(research_pair[0])
                            self.research_time.pop(research_pair[1])
                        
                        else:
                            time['breaks'].append(break_pair[1] - break_pair[0])
                            self.active_time.pop(break_pair[0])
                            self.active_time.pop(break_pair[1])
        
        active = time['active_end'] - time['active_start']
        self.active = active / 60 if active / 60 < 60 else active / 60 / 60
        self.research = time['research'] / 60 if time['research'] / 60 < 60 else time['research'] / 60 / 60
    
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
        bins = 1 + len(self.research_names)
        dataframe['time'] = dataframe['hours'] if type(self.active_time) == float else dataframe['minutes']
        dataframe['active'] = self.active_time
        dataframe['research'] = self.research_time
        dataframe['sites'] = self.research_names
        plt.history(time, bins, objects = self)


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


def focus_monitor(obj):
    # Tracks the time spent in an application window (Linux only currently)
    browsers = ['Firefox', 'Chrome', 'Safari', 'Opera', 'Edge', 'Internet Explorer',]
    if(xprop_exists):
        
        if(check_process_running('code')):
            # 
            if('Visual Studio Code' in get_active_window_title()):
                obj.active_time.append(toggle_timer())
                idle = False
                recorded = False
                dash = ' {en dash} '.encode('utf8')
                while(check_process_running('code')):
                    time.sleep(3)
                    active_window = get_active_window_title()
                    
                    if('Visual Studio Code' in active_window):
                        f, project, app = active_window.split(' - ')
                        print('\n' + f + '  ' + project + '  ' + app + '\n')
                        obj.project_name = project
                        
                        if(f not in obj.edited):
                            obj.edited.append(f)
                            
                    
                    # if('Visual Studio Code' not in active_window):
                    #     s = re.match('/\s\W+_?\s/', active_window)
                    #     sub, org, app = active_window.split(' - ')
                    #     print('\n' + sub + ' ' + org + ' ' + app + '\n')
                    
                    if(not 'Visual Studio Code' in active_window and not idle):
                        obj.active_time.append(toggle_timer())
                        idle = True
                    
                    elif('Visual Studio Code' in active_window and idle):
                        obj.active_time.append(toggle_timer())
                        obj.research_time.append(toggle_timer())
                        idle = False
                        recorded = False
                    
                    elif('Visual Studio Code' not in active_window and idle and not recorded):
                        print(active_window)
                        obj.research_time.append(toggle_timer())
                        if(active_window.split(dash)[-1] in browsers):
                            obj.research_names.append(f"{active_window.split(dash.decode('utf8'))[-2]} -> {active_window.split(dash)[-1]}")
                            recorded = True
                    
                    elif('Visual Studio Code' not in active_window and active_window.split(dash)[0] not in obj.research_name):
                        obj.research_names.append(f"{active_window.split(' -- ')[-2]} -> {active_window.split(' -- ')[-1]}")
                    print(obj.project_name)
                    print(obj.active_time)
                    print(obj.research_time)
                    print(obj.research_names)
            obj.process()
            obj.report()
            exit()


if __name__ == "__main__":
    timeout = time.time() + 180
    
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