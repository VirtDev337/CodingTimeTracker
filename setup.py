import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='CodeTime',
    version='0.1',
    scripts=['codetime'],
    author="Lee Harvey",
    author_email="com.virtdev@gmail.com",
    description="A coding timer for IDE's.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="//mnt/vault/Development/Workspace/Code/Projects/TimeTracker/ReadMe.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ELv2 License",
        "Operating System :: OS Independent",
    ],
)
