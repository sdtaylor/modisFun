import glob
import os
import gdalnumeric
import numpy as np
import time
from matplotlib import pyplot as plt

dataDir='/home/shawn/data/modisReprojected/'

filesNDVI = glob.glob(os.path.join(dataDir+'*2009*NDVI.tif'))
#pixel reliability -1: Not processed     0: Good       1: Probably Good    2: Snow/Ice    3: Cloudy
filesPR = glob.glob(os.path.join(dataDir+'*2009*pixel_reliability.tif'))

#Take a list of images. read them, return the stacked array of all of them
def stackImages(fileList):
    fileList=sorted(fileList)
    #Read in all rasters and stack them into a single array. (rows x column x numRasters)
    fullYear=gdalnumeric.LoadFile(fileList[0])
    for thisImage in fileList[1:]:
        image=gdalnumeric.LoadFile(thisImage)
        fullYear=np.dstack((fullYear, image))
    return(fullYear)

#Return day of year for each image
def getDOY(fileList):
    doyList=[]
    for thisFile in fileList:
        doyList.append(int(thisFile.split('-')[1][-3:]))
    return(sorted(doyList))

imageDOY=np.array(getDOY(filesNDVI))

ndvi=stackImages(filesNDVI)
pr=stackImages(filesPR)


def numElements(a, element):
    return(np.sum((a==element)))

#snow=np.apply_along_axis(numElements,axis=2, arr=pr, element=2)

import random
pixelsToShow=random.sample(range(1,pr.shape[0]*pr.shape[1]),100)
#shuffle(pixelsToShow)
#pixelsToShow=pixelsToShow[1:100]
print(list(imageDOY))

from scipy.interpolate import UnivariateSpline as spline
#Go through and process each pixel. 
count=0
for row in range(1,ndvi.shape[0]):
    for col in range(1, ndvi.shape[1]):
        if count in pixelsToShow:
            pixelPR=pr[row,col,]
            if sum(pixelPR==-1)==pr.shape[2]:
                continue

            print(pixelPR)
            thisPixel=ndvi[row,col,]

            #thisPixel[pixelPR==3]=0
            print(list(thisPixel))

            spl=spline(thisPixel, imageDOY)
            xs=np.linspace(1,365,2000)
            
            #plt.scatter(imageDOY, thisPixel, c=pixelPR)
            #plt.plot(imageDOY, thisPixel, 'ro')
            #plt.plot(xs, spl(xs), 'g')
            classes=[-1,0,1,2,3]

            negone=plt.scatter(imageDOY[pixelPR==classes[0]], thisPixel[pixelPR==classes[0]], color='k')
            zero=plt.scatter(imageDOY[pixelPR==classes[1]], thisPixel[pixelPR==classes[1]], color='b')
            one=plt.scatter(imageDOY[pixelPR==classes[2]], thisPixel[pixelPR==classes[2]], color='g')
            two=plt.scatter(imageDOY[pixelPR==classes[3]], thisPixel[pixelPR==classes[3]], color='y')
            three=plt.scatter(imageDOY[pixelPR==classes[4]], thisPixel[pixelPR==classes[4]], color='r')

            plt.legend((negone, zero, one, two, three), 
                       ('Not Processed', 'Good', 'Probably Good','Snow','Clouds'), 
                       scatterpoints=1,
                       loc='lower center',
                       ncol=3,
                       bbox_to_anchor=(0.5, -0.12))
            plt.show()
        count+=1


