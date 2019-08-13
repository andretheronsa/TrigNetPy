import os
import zipfile
import csv
import datetime

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
            julian_date = q_file.split('N')[1].split('Z')[0]
            year = "".join(["20", q_file.split('.')[1].split('q')[0]])
            date = datetime.datetime.strptime(year + julian_date, '%Y%j')
            with archive.open(q_file) as data:
                for line in data:
                    if "WGS 84 height" in str(line):
                        height = str(line).split(":")[1].split(" ")[1]
                        heights[str(date.date())] = height
    except Exception as e:
        print("{} {}".format(inputfile, e))

# Write to file
with open('GPS_heights.txt', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(sorted(heights.items()))
