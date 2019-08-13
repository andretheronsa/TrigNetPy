# TrigNetPy
Trignetpy is a bulk downloader to download zipped GPS data from the South African TrigNet GPS network.

Trgnetpy requires a start date, end date, station code and product description:  
`python down_trignet.py -b 20150101 -e 20160701 -s LGBN -p L1L2_30sec`  
This will download all the L1L2_30sec data for the Langebaan station between 2015/01/01 and 2016/07/01.

A folder will be created in the current folder where data will be stored.  
The new folder will be named using the input parameters (start_end_product_station).  
All the available products will be downloaded to this one folder.  
Since the product filenames on Trignet are named only according to station name and julian day there would be  
confusion for data on the same days for the same stations over different years.  
The short year (15, 16, 17 etc.) is therefore prefixed to the file name.  

# Extract_height.py
Small little script to extract all the WGS84 heights from the bulk downloaded zip files.
Run in the folder containing the downloaded files.
It crates a CSV with the height files

# Installation
Only Python3 is required to run.

# Notes 
Very little testing has been done and program will likely fail and not deal with ftp exceptions well.  
It should be able to deal with leap years and download the 366th days data for such years.
It will automatically set the start date to not before 2000-01-01 or the end date to not after today and fail if start and end days are flipped.  
*  -d toggles FTP debug mode for extra info if your downloads are failing  
*  -h For help  
