import glob
import os
from subprocess import call

dataDir='/home/shawn/data/modisBBSLandcover/'
outputDir='/home/shawn/data/modisReprojected/'
mrtPath='/home/shawn/bin/bin/resample'
resampleConfigFile='./resampleConfig.prm'

hdfFiles = glob.glob(os.path.join(dataDir+'*hdf'))

for thisFile in hdfFiles:
    #Keeps the 1st 3 sections of the modis filename. Like MOD13A1-A2008144-h10v04
    outputFile=outputDir+'-'.join(os.path.basename(thisFile).split('.')[0:3])+'.tif'
    call([mrtPath, '-i', thisFile, '-o', outputFile, '-p', resampleConfigFile ])
