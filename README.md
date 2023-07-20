# <div align="center">CodingTimeTracker</div>
&nbsp;&nbsp;&nbsp;&nbsp; This project was created so that coders can easily track their coding time, per project, without any unnecessary interaction.  Most of the tools available today require you to manually activate a timer that will, after configuration, provide you with an acurate record of the time spent in a project.  This application, once added to the startup applications, will run in the background and check for the VSCode process.  When the IDE is running, it will get the project name, record the start time, record any time spent in an internet browser for research, along with the pages visited.  This information is recorded in a squlite database for easy access.  The script can be called with a date, project name or time and all projects with that criteria will be assembled into a pdf report.  It will provide a report by one, multiple or all of the arguments provided.

### State:
&nbsp;&nbsp;&nbsp;&nbsp;Reimagined the manner of coding this project.  Reorganized code into classes.  Organized classes into files in the pkg/ directory.

### Features:
#### &nbsp;&nbsp;&nbsp;&nbsp;Soon to be implemented:
     - PDF reports.
     - Installation script to simplify the process.
     - Packaging, to remove the dependency on the system it is installed.
     - Add support for other IDE applications.

<iframe src="https://github.com/sponsors/VirtDev337/card" title="Sponsor" height="225" width="600" style="border: 0;"></iframe>
