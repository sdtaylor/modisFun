from urllib.request import urlopen
from urllib.request import urlretrieve
from getpass import getpass
import os

#From a list of h and v tile ranges make a list of all tiles in that grid
#ie. ['h07v13', 'h07v14', 'h08v13', 'h08v14']
def make_tile_list(h_tiles, v_tiles):
    tiles=[]
    for h in h_tiles:
        for v in v_tiles:
            tiles.append('h'+str(h).zfill(2)+'v'+str(v).zfill(2))
    return(tiles)

#Takes a string in format YYYY-MM-DD and returns YYYYDOY
from datetime import datetime
def date_to_modis_timestamp(d):
    date=datetime.strptime(d, '%Y-%m-%d')
    year=date.year
    doy=date.timetuple().tm_yday
    return(str(year)+str(doy))


#Get all the dates available from a given product
#start and end dates are in the format 'YYYY-MM-DD'. 
#If both are none include all dates.
#If only start_date specified include all dates after it.
#If only end_date specified include all dates up until it.
def get_modis_dates(url, start_date=None, end_date=None):
    if start_date != None:
        start_date=datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date=datetime.strptime('1900-01-01', '%Y-%m-%d')

    if end_date != None:
        end_date=datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date=datetime.strptime('2050-01-01', '%Y-%m-%d')

    date_list=[]
    html=urlopen(url).read()
    for filename in html.splitlines():
        filename=str(filename)
        if '[DIR]' in filename:
            #print(filename.split('href="')[1][0:10])
            #dates.append(filename.split('href="')[1][0:10])
            this_date=filename.split('href="')[1][0:10]
            if start_date <= datetime.strptime(this_date, '%Y.%m.%d') <= end_date:
                date_list.append(this_date)
    return(date_list)

#Get all the filenames from a given product+date and list of tiles wanted. 
def get_tile_filenames(date_url, tiles):
    files=[]
    html=urlopen(date_url).read()

    for this_line in html.splitlines():
        this_line=str(this_line)
        if 'hdf' in this_line and 'xml' not in this_line:
            for this_tile in tiles:
                if this_tile in this_line:
                    #print(this_line.split('"')[5])
                    files.append(this_line.split('"')[5])
    return(files)

#########################################################################

parent_dir='http://e4ftl01.cr.usgs.gov/MOLT/'
save_dir = '/home/shawn/data/MOD13Q1/'
product='MOD13Q1.006'

base_dir=parent_dir+product+'/'

start_date='2000-01-01'
end_date='2017-01-31'

h_tile_range=[7,8,9,10,11,12,13,14]
v_tile_range=[2,3,4,5,6]
tiles=make_tile_list(h_tile_range, v_tile_range)

modis_dates=get_modis_dates(base_dir, start_date=start_date, end_date=end_date)

username = input('NASA EarthLogin username: ')
password  = getpass('NASA Earthlogin password: ')

total_files=len(modis_dates)*len(tiles)
i=1
for this_date in modis_dates:
    image_files=get_tile_filenames(base_dir+this_date+'/', tiles)
    for this_file in image_files:
        print('downloading '+str(i)+' of '+str(total_files))
        i+=1
        os.system('wget --user={0} --password={1} -P {2} {3}{4}/{5}'.format(username, password, save_dir, base_dir, this_date, this_file))
