import glob
import os
import gdalnumeric
import numpy as np
#from matplotlib import plt

dataDir='/home/shawn/data/modisReprojected/'

files = glob.glob(os.path.join(dataDir+'*2009*'))

files=sorted(files)
#pixels=np.array()

for thisImage in files:
    image=gdalnumeric.LoadFile(thisImage)
    print(thisImage, image.shape)
    
