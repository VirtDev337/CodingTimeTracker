- Process monitor:
  - ProcMonitor object:
    - delay
    - ide_apps
    - active_ide_parent
    - ide_pids

  - First run:
    - Check for proc_monitor service
    - Install proc_monitor service

- Call main process (gui) on ide start:
  - MainWindow
    - Start minimized setting?
    - populate labels (last accessed?)
    - state renewal (if not first run?)

  - Prepare codetime object:
    - Projects
    - projects_dir
    - verbose
    - process

  - Prepare project object:
    - Name
    - modified_files
    - time_spent
    - date
    - last_modified_date
    - created
    - complete
    - dir
    - browser

  - Handler preparation:
    - codetime object
    - get/create project
    - initialize start time
    - update created date
    - configure file monitor
