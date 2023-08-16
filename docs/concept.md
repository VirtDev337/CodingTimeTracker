# CodingTimeTracker

This project was created so that coders can easily track their coding time, per project, without any unnecessary interaction. Most of the tools available today require you to manually activate a timer that will, after configuration, provide you with an acurate record of the time spent in a project. This application, once added to the startup applications, will run in the background and check for the VSCode process.

When the IDE is running, it will get the project name, record the start time, record any time spent in an internet browser for research, along with the pages visited. This information is recorded in a squlite database for easy access. The script can be called with a date, project name or time and all projects with that criteria will be assembled into a pdf report. It will provide a report by one, multiple or all of the arguments provided.

## Workflow

- Application monitors processes in order to determine if VSCode is accessed.
- Run the script that accesses and tracks project and time.
- - Keep a record of elapsed time in the IDE.
- - Keep a record of the files accessed and modified in the IDE.
- Run the script to monitor for browser use.
- - Record web page url, current tab and time spent in the browser.
- Write the project and browser records to json upon IDE termination.
- Create report on event for the specific date or project.
- Return to monitoring for IDE activation.

## Class Workflow

								|- -> complete
- VSCodeHandler -> CodeTime -> Project - -> date
								L - -> FileModifiedHandler -> Project.Files
- BrowserHandler -> CodeTime -> Project
									L	-> urls

## Notes

### FUNCTIONALITY

- Add *complete* functionality
- - Determines what can be skipped for tracking.
- - Allows for storage of untracked projects for reports.
- Add *remove* functionality
- - Ability to delete old projects.
- Add *status* functionality
- - Display information for the project including complete, created, last modified and location
- Add *verbose* functionality
- - Whether detailed information of a project is displayed or reported.


### GUI

- ct-gui -> on_start_clicked():
- - Add check if VSCode is open.
- - If report clicked, need to provide input window:
- - - Determine if date or project is provided
- - - If projects or all in input, show all projects (button maybe)
- - - Short or Full report functionality
- - - Populate project details
