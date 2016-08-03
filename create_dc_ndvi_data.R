library(gdalUtils)
library(raster)
library(stringr)



#############################################################################
#Main function.
#Take all raw modis MOD13Q1 images in a folder, extract the ndvi raster,
#crop them to some extent given by another raster or shapefile, 
#scale to true ndvi values, write them as <prefix>-YYYYDDD.tif
#where DDD is day of year. 
#
#src_folder: name of the folder containing modis hdf images
#dest_folder: folder to write processed ndvi images to.
#extent: extent to crop ndvi images to. can be another raster or shapefile object
#        must be within extent of the modis images
#prefix: prefix given to all the processed images. 
process_modis_images=function(src_folder, dest_folder, extent, prefix) {
  raw_files=list.files(src_folder, full.names = TRUE)
  
  #Don't try to process xml files with get automacially generated sometimes. 
  raw_files=raw_files[!grepl('xml',raw_files)]
  
  dir.create(dest_folder)
  
  for(this_file in raw_files){
    #ndvi is the 1st subdataset of the hdf files, set by sd_index.
    ndvi_raster=gdalUtils::gdal_translate(src_dataset = this_file,
                               sd_index=1,
                               output_Raster = TRUE,
                               dst_dataset = paste(dest_folder,'/temp.tif',sep=''))
    
    #To crop an image it must be the same CRS as the object you are cropping with.
    ndvi_raster = raster::projectRaster(ndvi_raster, extent, method='ngb')
    ndvi_raster = raster::crop(ndvi_raster, extent)

    #Scale to true ndvi value according to metadata    
    #Officially this number should be 0.0001, but that does not transform the actual
    #data to be between -1 and 1
    ndvi_raster = raster::calc(ndvi_raster, fun=function(x){x*0.00000001})
    
    image_date=stringr::str_sub(this_file, -36,-30)
    
    writeRaster(ndvi_raster, paste0(dest_folder,'/',prefix,image_date,'.tif'))
    
    #Delete tempory output file that gdal_translate requires.
    unlink(paste(dest_folder,'/temp.tif',sep=''))
  }
}


########################################################


#Preparation steps. 
#Harvard forest is located within the modis tile h12v04, SanJoaquin in h08v05
#I went to http://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.005/ and downloaded all of those tiles
#within the year 2015 and put them in their respective folder. Then ran this script
#to produce ndvi tifs for 2015 time series at each site.


setwd('~/data/neonTeaching/')

#Harvard forest
harv_reference_raster=raster::raster('/home/shawn/data/neonTeaching/NEON-DS-Airborne-Remote-Sensing/HARV/DSM/HARV_DSMhill.tif')

process_modis_images(src_folder = 'HARV_MODIS',
                     dest_folder = 'HARV_NDVI',
                     extent = harv_reference_raster,
                     prefix = 'HARV_NDVI_')


#San Joaquin Experimental RAnge
sjer_reference_raster=raster::raster('/home/shawn/data/neonTeaching/NEON-DS-Airborne-Remote-Sensing/SJER/DSM/SJER_dsmHill.tif')

process_modis_images(src_folder = 'SJER_MODIS',
                     dest_folder = 'SJER_NDVI',
                     extent = sjer_reference_raster,
                     prefix = 'SJER_NDVI_')





