############################################################
# Project: Trignet bulk downloader                        #
# Author: Andre Theron (andretheronsa@gmail.com)           #
# Created: July 2019                                       #
############################################################

from ftplib import FTP
import datetime
from pathlib import Path
import argparse

# Main fetching program
def fetch(args):
    start_date, end_date, station, product, debug = args[0], args[1], args[2], args[3], args[4]
    print("User input: start_date: {}, end_date: {}, station: {}, product: {}".format(start_date, end_date, station, product))

    # Check if end date is after start date
    if start_date > end_date:
        print("End date before start date - exit")
        return

    # Check if end date is later than today - use today if it is
    start_dt = datetime.datetime.strptime(str(start_date), '%Y%m%d')
    first_data = datetime.datetime.strptime('20000101', '%Y%m%d')
    if start_dt > first_data:
        start_short = start_dt.year - 2000
    else:
        print("Start date before data capture started - using 2000/01/01")
        start_short = first_data.year - 2000

    # Check if end date is later than today - use today if it is
    end_dt = datetime.datetime.strptime(str(end_date), '%Y%m%d')
    last_data = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
    if end_dt < last_data:
        end_short = end_dt.year - 1999
    else:
        print("End date later than today - using today as end date...")
        end_short = datetime.date.today().year - 1999

    # Determine relevant leap years
    leaps = [year for year in list(range(start_short, end_short)) if year % 4 == 0]

    # Iterate over all possible dates for all years from start to finish
    paths = []
    for year in list(range(start_short, end_short)):

        # Start and end on a specefic day in the first and last year of search - but download all days for other years
        if year == start_short:
            start = int(start_dt.strftime('%j'))
        else:
            start = 1
        if year == end_short:
            end = int(end_dt.strftime('%j'))

        # end var is used in range which is not inclusive so its days + 1
        elif year in leaps:
            end = 367
        else:
            end = 366

        # Create list of full ftp filepaths of all expected files wi 0 padded julian days
        paths.extend([
            "RefData." + str(year) + "/" + '{0:03d}'.format(day) + "/" + str(product) + "/" + str(station) + '{0:03d}'.format(day) + "Z.zip" 
            for day in list(range(start, end))
            ])

    # Create directory in cwd to store data
    workdir = Path(str(start_date) + "_" + str(end_date) + "_" + str(product) + "_" + str(station))
    workdir.mkdir(parents=True, exist_ok=True)
    
    # Set debug level
    if debug:
        debug_level = 2
    else:
        debug_level = 0
    
    # Fetch file from ftp
    for path in paths:

        # Create expected filepaths
        filepath = '/'.join(path.split('/')[:3])
        remote_filename = path.split('/')[3]
        local_filename = workdir / (path.split('/')[0].split('.')[1] + path.split('/')[3])

        # Check if file is already there
        if local_filename.is_file():
            print("Local file {} found".format(str(local_filename)))
            continue
        
        # Log into trignet, change dir and download file
        try:
            with FTP('ftp.trignet.co.za', timeout=600) as ftp:
                ftp.set_debuglevel(debug_level)
                ftp.login()
                print("Change remote path to {}".format(filepath))
                ftp.cwd(filepath)
                if remote_filename in ftp.nlst():
                    print("Remote file found - Downloading file {} to {}".format(remote_filename, str(local_filename)))
                    lf = open(str(local_filename), "wb")
                    ftp.retrbinary("RETR " + remote_filename, lf.write)
                    lf.close()
                    ftp.close()
                else:
                    print("Remote file {} not found in {}".format(remote_filename, filepath))
        except Exception as e:
            print("FTP error while changing dir / downloading. skip. Error code: {}".format(remote_filename, e))
            
# Parse input
def cmd_line_parse(iargs=None):
    EXAMPLE = "example: down_trignet.py -b 20150101 -e 20160701 -s LGBN -p L1L2_30sec"
    parser = argparse.ArgumentParser(description='Trignet batch downloading script', formatter_class=argparse.RawTextHelpFormatter, epilog=EXAMPLE)
    parser.add_argument('-b','--begin', dest='start_date', required=True, help='Start date in yyyymmdd format eg. 20161102')
    parser.add_argument('-e','--end', dest='end_date', required=True, help='End date in yyyymmdd format eg. 20170531')
    parser.add_argument('-s','--station', dest='station', required=True, help='Station code - eg. LGBN')
    parser.add_argument('-p','--product', dest='product', required=True, help='Product detail eg. L1L2_30sec')
    parser.add_argument('-d','--debug', action='store_true', help='Turn on verbose debug mode')
    args = parser.parse_args(args=iargs)
    return(args.start_date, args.end_date, args.station, args.product, args.debug)

# def main program run
def main(iargs=None):
    args = cmd_line_parse(iargs)
    fetch(args)

if __name__ == "__main__":
    main()
