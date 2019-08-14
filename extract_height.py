import os
import zipfile
import csv
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Find input files in cwd
inputfiles = []
for inputfile in os.listdir():
    if inputfile.endswith(".zip"):
        inputfiles.append(inputfile)

# Extract heights
ts = {}
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
                        ts[date.date()] = {"height": float(height)}
    except Exception as e:
        print("{} {}".format(inputfile, e))

# Pandas work
df = pd.DataFrame.from_dict(ts, orient="index")

# Remove outliers
# Quantiles
q1 = df.quantile(0.25)
q3 = df.quantile(0.75)
iqr = q3 - q1

# z-score
z = np.abs(stats.zscore(df))
df_z = df[(z < 2).all(axis=1)]

# Average
df_z_a = df_z.rolling(3).median()

# Write to file
with open('GPS_heights.txt', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(sorted(heights.items()))
