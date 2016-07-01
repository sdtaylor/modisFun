from urllib.request import urlopen
from urllib.request import urlretrieve
import os

#From a list of h and v tile ranges make a list of all tiles in that grid
#ie. ['h07v13', 'h07v14', 'h08v13', 'h08v14']
def make_tile_list(h_tiles, v_tiles)
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
def get_modis_dates(url):
    dates=[]
    html=urlopen(url).read()
    for filename in html.splitlines():
        filename=str(filename)
        if '[DIR]' in filename:
            #print(filename.split('href="')[1][0:10])
            dates.append(filename.split('href="')[1][0:10])
    return(dates)

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
product='MOD13Q1.005'

base_dir=parent_dir+product+'/'

start_date='2013-01-01'
end_date='2015-12-31'

h_tile_range=[7,8,9,10,11,12,13,14]
v_tile_range=[2,3,4,5,6]
tiles=make_tile_list(h_tile_range, v_tile_range)

all_dates=get_modis_dates(base_dir)
total_files=len(all_dates)*len(tiles)

i=1
for this_date in all_dates:
    image_files=get_tile_filenames(base_dir+this_date+'/', tiles)
    for this_file in image_files:
        print('downloading '+str(i)+' of '+str(total_files))
        i+=1
        #urlretrieve(base_dir+this_date+'/'+this_file, this_file)
        os.system('wget '+base_dir+this_date+'/'+this_file)

