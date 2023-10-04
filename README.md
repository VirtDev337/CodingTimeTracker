# <div align="center">CodingTimeTracker</div>
&nbsp;&nbsp;&nbsp;&nbsp; This project was created so that coders can easily track their coding time, per project, without any unnecessary interaction.  Most of the tools available today require you to manually activate a timer that will, after configuration, provide you with an acurate record of the time spent in a project.  This application, once added to the startup applications, will run in the background and check for the VSCode, Codium or RStudio processes.  When the IDE is running, it will get the project name, record the start time, record any time spent in an internet browser for research, along with the pages visited.  This information is recorded in a json file for easy access.  The script can be called with a date, project name or time and all projects with that criteria will be assembled into a pdf report.  It will provide a report by one, multiple or all of the arguments provided.

### State:
<ul>
     <li>Reimagined the manner of coding this project.</li>
     <li>Reorganized code into classes.</li>
     <li>Organized classes into files in the pkg/ directory.</li>
     <li>Continued reorganization for installation (setup) of the application.</li>
     <li>Working out dependency installation and inclusion.</li>
</ul>

### Features:
#### &nbsp;&nbsp;&nbsp;&nbsp;Soon to be implemented:
     - PDF reports.
     - Installation script to simplify the process.
     - Packaging, to remove the dependency on the system it is installed.
     - Add support for additional IDE applications.
     - Add support for additional browsers (currently Chrome, FireFox and Brave are supported).

<iframe src="https://github.com/sponsors/VirtDev337/card" title="Sponsor" height="225" width="600" style="border: 0;"></iframe>
