from distutils.core import setup

VERSION = "0.2"

DESCRIPTION = """\
FASTQCParser is a tool for automating the processing of basic FastQC results in Python.
Given the contents of picard_report.txt, it will parse the results into an object that can
then be used in code.
"""

setup(
    name="picard_parser", 
    version=VERSION, 
    description="Parses Picard result files into Python",
    long_description=DESCRIPTION,
    url="https://github.com/StamLab/picard-parser",
    packages=["picard_parser"],
    license="Python",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        ],
    )
