import pkg.codetime as codetime
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib import colors


def create_project_report(project):
    # Set up canvas
    canvas = canvas.Canvas(
        project.name + '.pdf',
        pagesize=landscape(letter)
    )
    canvas.setTitle(project.name + ' CodeTime Report')

    # Set up grid
    y_grid = [i * inch for i in range(1, 13)]
    x_grid = [i * inch for i in range(1, len(project.modified_files) + 2)]
    canvas.grid(x_grid, y_grid)

    # Draw time spent data
    max_time = project.get_total_time_spent()
    time_step = max_time / 12

    for i in range(12):
        canvas.drawString(
            0.5 * inch, (12 - i) * inch,
            '{:.2f}'.format(time_step * i)
        )
    canvas.drawString(
        0.5 * inch, 0.5 * inch,
        'Time spent (hours)'
    )

    # Draw modified files data
    for i, modified_file in enumerate(project.modified_files):
        canvas.drawString(
            (i + 1.5) * inch,
            0.25 * inch,
            modified_file
        )

    # Draw browser usage data
    browser_usage = project.get_browser_usage()
    for i, usage in enumerate(browser_usage):
        canvas.drawString(
            (i + 1.5) * inch,
            0.75 * inch,
            '{} ({:.2f} min)'.format(
                usage['title'],
                usage['time'] / 60
            )
        )

    # Save and close canvas
    canvas.showPage()
    canvas.save()


# This function takes a date_time parameter as a string and creates a PDF report for that date/time. It first attempts to parse the date/time string as a date in the YYYY-MM-DD format, and if that fails it tries to parse it as a time in the HH:MM format. If neither format is valid, it prints an error message and returns.
def create_datetime_report(date_time):
    # Parse date/time
    try:
        datetime_obj = datetime.strptime(date_time, '%Y-%m-%d')
        time_step = timedelta(days=1)

    except ValueError:
        try:
            datetime_obj = datetime.strptime(date_time, '%H:%M')
            time_step = timedelta(minutes=60)

        except ValueError:
            print('Invalid date/time format, please use YYYY-MM-DD or HH:MM')
            return

    # Set up canvas
    c = canvas.Canvas(
        date_time + '.pdf',
        pagesize=portrait(letter)
    )
    c.setTitle(date_time + ' CodeTime Report')

    # Set up grid
    y_grid = [i * inch for i in range(1, len(codetime.projects) + 2)]
    x_grid = [i * inch for i in range(1, 13)]
    c.grid(x_grid, y_grid)

    # Draw project data
    for i, project in enumerate(codetime.projects):
        time_spent = project.get_time_spent(
            datetime_obj,
            datetime_obj + time_step
        )
        if time_spent > 0:
            c.drawString(
                0.5 * inch,
                (len(codetime.projects) - i) * inch,
                project.name
            )
            c.rect(
                1 * inch,
                (len(codetime.projects) - i + 0.5) * inch,
                time_spent / 60 * inch,
                0.5 * inch,
                fill=1
            )
            c.drawString(
                (time_spent / 60 + 1) * inch,
                (len(codetime.projects) - i) * inch,
                '{:.2f} min'.format(time_spent)
            )

    # Save and close canvas
    c.showPage()
    c.save()
