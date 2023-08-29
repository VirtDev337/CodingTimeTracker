import pgi
import pkg.trackers as trackers

pgi.require_version('Gtk', '3.0')
from pgi.repository import Gtk as gtk


# GTK frontend


class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, title="CodeTime")

        self.set_border_width(10)
        self.set_default_size(400, 300)

        # Create labels
        self.project_label = gtk.Label(label="Project:")
        self.start_time_label = gtk.Label(label="Start Time:")
        self.end_time_label = gtk.Label(label="End Time:")

        # Create entry boxes
        self.project_entry = gtk.Entry()
        self.start_time_entry = gtk.Entry()
        self.end_time_entry = gtk.Entry()

        # Create buttons
        self.start_button = gtk.Button(label="Start")
        self.stop_button = gtk.Button(label="Stop")
        self.save_button = gtk.Button(label="Save")
        self.report_button = gtk.Button(label="Generate Report")
        self.quit_button = gtk.Button(label="Quit")

        # Add button click events
        self.start_button.connect("clicked", self.on_start_clicked)
        self.stop_button.connect("clicked", self.on_stop_clicked)
        self.save_button.connect("clicked", self.on_save_clicked)
        self.report_button.connect("clicked", self.on_report_clicked)
        self.quit_button.connect("clicked", gtk.main_quit)

        # Add widgets to grid
        grid = gtk.Grid(
            column_homogeneous=True,
            row_spacing=10,
            column_spacing=10
        )
        grid.attach(self.project_label, 0, 0, 1, 1)
        grid.attach(self.project_entry, 1, 0, 1, 1)
        grid.attach(self.start_time_label, 0, 1, 1, 1)
        grid.attach(self.start_time_entry, 1, 1, 1, 1)
        grid.attach(self.end_time_label, 0, 2, 1, 1)
        grid.attach(self.end_time_entry, 1, 2, 1, 1)
        grid.attach(self.start_button, 0, 3, 1, 1)
        grid.attach(self.stop_button, 1, 3, 1, 1)
        grid.attach(self.save_button, 0, 4, 1, 1)
        grid.attach(self.report_button, 1, 4, 1, 1)
        grid.attach(self.quit_button, 0, 5, 1, 1)

        # Add grid to window
        self.add(grid)

    def on_start_clicked(self, widget):
        project_name = self.project_entry.get_text()
        start_time = self.start_time_entry.get_text()
        end_time = self.end_time_entry.get_text()
        trackers.start_project(
            project_name,
            start_time,
            end_time
        )

    def on_stop_clicked(self, widget):
        trackers.stop_project()

    def on_save_clicked(self, widget):
        trackers.save_projects()

    def on_report_clicked(self, widget):
        report_window = ReportWindow()
        report_window.show_all()


class ReportWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, title="CodeTime Report")

        self.set_border_width(10)
        self.set_default_size(400, 300)

        # Create labels
        self.project_label = gtk.Label(label="Project:")
        self.date_label = gtk.Label(label="Date/Time:")

        # Create entry boxes
        self.project_entry = gtk.Entry()
        self.date_entry = gtk.Entry()

        # Create buttons
        self.generate_button = gtk.Button(label="Generate")
        self.close_button = gtk.Button(label="Close")

        # Add button click events
        self.generate_button.connect("clicked", self.on_generate_clicked)
        self.close_button.connect("clicked", self.on_close_clicked)

        # Add widgets to grid
        grid = gtk.Grid(
            column_homogeneous=True,
            row_spacing=10,
            column_spacing=10
        )
        grid.attach(self.project_label, 0, 0, 1, 1)
        grid.attach(self.project_entry, 1, 0, 1, 1)
        grid.attach(self.date_label, 0, 1, 1, 1)
        grid.attach(self.date_entry, 1, 1, 1, 1)
        grid.attach(self.generate_button, 0, 2, 1, 1)
        grid.attach(self.close_button, 1, 2, 1, 1)

        # Add grid to window
        self.add(grid)

    def on_generate_clicked(self, widget):
        project_name = self.project_entry.get_text()
        date_time = self.date_entry.get_text()
        trackers.project_report(project_name, date_time)

    def on_close_clicked(self, widget):
        self.destroy()

if __name__ == '__main__':
    win = MainWindow()
    win.connect("destroy", gtk.main_quit)
    win.show_all()
    gtk.main()
    pgi.require_version('Gtk', '3.0')
