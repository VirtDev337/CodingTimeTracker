import os
import re
import time
import fpdf
import json
import codecs
import pandas
import subprocess
from sqlitedict import SqliteDict
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig


def get_active_window_title():
    # Returns the title of the window in focus using the `xprop` command
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    active = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if active != None:
        window_id = active.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None
    # Finds and returns the name property for the active window
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").decode('UTF-8').strip('"')
    return None

# Class to create objects to be added to the database


class Tracker():
    date = ''
    time = ''
    name = ''
    edited = []
    research_names = []
    active = 0
    research = 0
    active_time = []
    research_time = []
    times = {}

    def __init__(self, process_name=get_active_window_title()):
        self.date = time.strftime('%m-%d-%Y')  # '10-18-2010'
        self.time = time.strftime('%I:%M%p')  # '1:36PM'
        if ('Visual Studio Code' in process_name):
            self.name = process_name.split(' - ')[1]

    def __str__(self):
        return self.name

    def process(self):
        global sleep
        if len(self.active_time) > 1:
            self.times = {
                'active_start': '',
                'active_end': '',
                'active': 0,
                'research': 0,
                'breaks': 0,
            }

            if not self.times['active_start']:
                self.times['active_start'] = self.active_time.pop(0)

            for break_pair in self.active_time[0::3]:
                if type(break_pair) == 'list':
                    print(break_pair)

                    for research_pair in self.research_time[0::3]:
                        if type(research_pair) == 'list':

                            if break_pair[0] + sleep == research_pair[0]:
                                self.times['research'] += research_pair[1] - \
                                    research_pair[0]
                                self.research_time.pop(research_pair[0])
                                self.research_time.pop(research_pair[1])

                            else:
                                self.times['breaks'] += (break_pair[1] -
                                                         break_pair[0])
                                self.active_time.pop(break_pair[0])
                                self.active_time.pop(break_pair[1])

            self.research = self.times['research'] / 60 if self.times['research'] / \
                60 < 60 else self.times['research'] / 60 / 60
            self.save_data()

    def save_data(self, database='timetracker.db'):
        if '.db' not in database:
            database = database + '.db'
        if self.active_time and len(self.active_time) == 1:
            if not self.times['active_end']:
                self.times['active_end'] = self.active_time.pop()

            active = (self.times['active_end'] - self.times['active_start']
                      ) - self.times['research'] - self.times['breaks']
            self.active = active / 60 if active / 60 < 60 else active / 60 / 60

        try:
            with SqliteDict(database) as mydict:
                for attrib in self:
                    mydict[attrib] = self.attrib
                mydict.commit()
        except Exception as ex:
            print("Error during storing data (Possibly unsupported):", ex)

    def load_data(self, database='timetracker.db'):
        try:
            with SqliteDict(database) as mydict:
                # No need to use commit(), since we are only loading data!
                for key in mydict:
                    self[key] = mydict[key]
                return
        except Exception as ex:
            print("Error during loading data:", ex)


class History():
    date = ''
    projects = []

    def __init__(self, date=time.strftime('%b %d, %Y'), projects=[]):
        self.date = date
        self.projects.extend(projects)

    def __str__(self):
        return self.date

    def save_data(self, dir='~/Documents', fname='.time-track.json'):
        json_object = json.dumps(self, indent=4)
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

    def load_data(self, database='timetracker.db'):
        try:
            with SqliteDict(database) as mydict:
                # No need to use commit(), since we are only loading data!
                for key in mydict:
                    self[key] = mydict[key]
                return
        except Exception as ex:
            print("Error during loading data:", ex)

    def create_pdf(self, dir='~/Documents/timetracker', fname='time-track'):
        dataframe = pandas.DataFrame()
        dataframe['minutes'] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        dataframe['hours'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for project in self.projects:
            if time.strftime('%b %d, %Y') == project.date:
                dataframe['project'] = project.name
                dataframe['project']['time'] = dataframe['hours'] if type(
                    project.active) == float else dataframe['minutes']
                dataframe['project']['active'] = (
                    project.project_name, project.active_time,)
                dataframe['project']['research'] = (
                    project.project_name, project.research_time,)
                dataframe['project']['sites'] = (
                    project.project_name, project.research_names,)

                title("Coding Time Tracker")
                xlabel('Coding & Research')
                ylabel('Time')

                xticks(dataframe['project']['research'],
                       dataframe['project']['sites'])

                bar(dataframe['project']['time'], dataframe['project']
                    ['active'], width=0.5, color="cyan", label="VSCode")
                bar(dataframe['project']['time'], dataframe['project']
                    ['research'], width=0.5, color="blue", label="Research")

                legend()
                axis([0, 10, 0, 8])
                savefig('barchart.png')

                pdf = fpdf()
                pdf.add_page()
                pdf.set_xy(0, 0)
                pdf.set_font('arial', 'B', 12)
                pdf.cell(60)
                pdf.cell(
                    75, 10, "A Tabular and Graphical Report of time spent in VSCode", 0, 2, 'C')
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.cell(-40)
                pdf.cell(50, 10, 'Research Sites', 1, 0, 'C')
                pdf.cell(40, 10, 'Project', 1, 0, 'C')
                pdf.cell(-90)
                pdf.set_font('arial', '', 12)
                for i in range(0, len(dataframe)):
                    pdf.cell(40, 10, '%s' %
                             (str(dataframe.active.iloc[i])), 1, 0, 'C')
                    pdf.cell(40, 10, '%s' %
                             (str(dataframe.research.iloc[i])), 1, 2, 'C')
                    pdf.cell(-90)
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.cell(-30)
                pdf.image('barchart.png', x=None, y=None,
                          w=0, h=0, type='', link='')
                pdf.output('report{time.strftime("%I%M%p%b%d%Y")}.pdf', 'F')
