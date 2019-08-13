############################################################
# Project: Extract height from bulk downloaded zip files   #
# Author: Andre Theron (andretheronsa@gmail.com)           #
# Created: July 2019                                       #
############################################################

import os
import zipfile
import csv

# Find input files in cwd
inputfiles = []
for inputfile in os.listdir():
    if inputfile.endswith(".zip"):
        inputfiles.append(inputfile)

# Extract heights
heights = {}
for inputfile in inputfiles:
    try:
        with zipfile.ZipFile(inputfile, 'r') as archive:
            for archive_file in archive.namelist():
                if archive_file.endswith("q"):
                    q_file = archive_file
                    break
            date = "".join(["20", q_file.split('.')[1].split('q')[0], q_file.split('N')[1].split('Z')[0]])
            with archive.open(q_file) as data:
                for line in data:
                    if "WGS 84 height" in str(line):
                        height = str(line).split(":")[1].split(" ")[1]
                        heights[date] = height
    except Exception as e:
        print("{} {}".format(inputfile, e))

# Write to file
with open('GPS_heights.txt', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(heights.items())
