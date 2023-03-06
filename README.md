# <div align="center">CodingTimeTracker</div>
&nbsp;&nbsp;&nbsp;&nbsp; This project was created so that coders can easily track their coding time, per project, without any unnecessary interaction.  Most of the tools available today require you to manually activate a timer that will, after configuration, provide you with an acurate record of the time spent in a project.  This application, once added to the startup applications, will run in the background and check for the VSCode process.  When the IDE is running, it will get the project name, record the start time, record any time spent in an internet browser for research, along with the pages visited.  This information is recorded in a squlite database for easy access.  The script can be called with a date, project name or time and all projects with that criteria will be assembled into a pdf report.  It will provide a report by one, multiple or all of the arguments provided.

### State:
&nbsp;&nbsp;&nbsp;&nbsp;Currently, there is an issue with the storage of the tracker object.  Once this is resolved, the arguments provided at the command line will be implemented.

### Features:
#### &nbsp;&nbsp;&nbsp;&nbsp;Soon to be implemented:
     - PDF reports.
     - Installation script to simplify the process.
     - Packaging, to remove the dependency on the system it is installed.
     - Add support for other IDE applications.
