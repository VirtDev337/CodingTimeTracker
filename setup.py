
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# def read(*names, **kwargs):
#     with io.open(
#         join(dirname(__file__), *names),
#         encoding=kwargs.get('encoding', 'utf8')
#     ) as fh:
#         return fh.read()


setup(
    name='CodeTime',
    version='0.1',
    scripts=['ide_mon', 'codetime_gui', 'codetime_cli'],
    author="VirtDev337",
    author_email="com.virtdev@gmail.com",
    description="A coding timer for IDE's.  Currently supports VSCode, Codium and RStudio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="//mnt/vault/Development/Workspace/Code/Projects/TimeTracker/ReadMe.md",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ELv2 License",
        "Operating System :: OS Independent",
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development',
    ],
    project_urls={
        'Changelog': 'https://github.com/ionelmc/python-nameless/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/ionelmc/python-nameless/issues',
    },
    keywords=[
        'Development', 'Tracker', 'Time', 'Modifications', 'IDE'
    ],
    python_requires='>=3.8.*, >=3.9.*, >=3.10.*',
    install_requires=[
        'asgiref'==3.5.2,
        'argparse'==1.4.0,
        'calcure'==2.6,
        'convertdate'==2.4.0,
        'DateTime'==5.2,
        'docutils'==0.20.1,
        'hijri-converter'==2.3.1,
        'holidays'==0.18,
        'iniconfig'==1.1.1,
        'jdatetime'==4.1.0,
        'korean-lunar-calendar'==0.3.1,
        'lockfile'==0.12.2,
        'pgi'==0.0.11.2,
        'Pillow'==10.0.1,
        'psutil'==5.9.5,
        'py'==1.11.0,
        'PyMeeus'==0.5.12,
        'python-daemon'==3.0.1,
        'python-dateutil'==2.8.2,
        'pytz'==2020.1,
        'reportlab'==4.0.4,
        'six'==1.16.0,
        'tqdm'==4.64.1,
        'watchdog'==3.0.0,
        'zope.interface'==6.0
    ],
    extras_require={
        # eg:
        'rst': ['docutils>=0.11'],
        'gtk': ['pgi>=0.0.11.*'],
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'codetime = CodeTime.cli:main',
        ],
        'graphical_scripts': [
            'codetime = CodeTime.gui:main',
        ],
        'service_scripts': [
            'codetime = CodeTime.mon:main',
        ],
    }
)
