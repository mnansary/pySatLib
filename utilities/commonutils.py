# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np 
import matplotlib.pyplot as plt
import time
import sys
import os
from osgeo import gdal,osr,gdalconst,ogr
from mpl_toolkits.basemap import Basemap
from termcolor import colored
        
class TiffReader(object):

    '''
        The purpose of this class is to contain necessary functions to Read GeoTiff data
    '''
    def __init__(self):
        self.__success_flag=True

    def GetDataSet(self,tiff_file_path):
        '''
            Reads the Dataset
        '''
        gdal.UseExceptions()
        
        try:
            data_set=gdal.Open(tiff_file_path,gdal.GA_ReadOnly)        
            return data_set

        except RuntimeError as e_read:                             
            print(colored('#    Error while reading dataset!','red'))
            print(colored('#    Error Details:','blue'))
            print(colored(e_read,'yellow'))
            self.__success_flag=False
            sys.exit(1)
            
    def GetDataArray(self,tiff_file_path,raster_count=1,raster_num=1):
        '''
            Returns single Raster data as array
        '''
        data_set=self.GetDataSet(tiff_file_path)
        
        if(data_set.RasterCount==raster_count):                          
            try:
                raster_band_data=data_set.GetRasterBand(raster_num)
                data=raster_band_data.ReadAsArray()
                return data

            except RuntimeError as e_array:
                print(colored('#    Error while getting data as array!','red'))
                print(colored('#    Error Details:','blue'))
                print(colored(e_array,'yellow'))
                self.__success_flag=False
                sys.exit(1)
        else:
            print('#    The file contains {} bands!'.format(data_set.RasterCount))
            sys.exit(1)

class TiffWriter(object):
    
    '''
        The purpose of this class is to write Array data as Geotiff
    '''

    def __init__(self):
        self.reference_tiff_path=None
        self.saving_directory=None

    def save(self,data_array,data_identifier):
        '''
            Saving array Data as geotiff
        '''
        start_time=time.time()
        
        geotiff=os.path.join(self.saving_directory,data_identifier+'.tif')
        [col, row] = data_array.shape
        Reader=TiffReader()
        data_set=Reader.GetDataSet(self.reference_tiff_path)

        print(colored('#    Saving: '+data_identifier+'.tif at: '+self.saving_directory,'blue'))
        
        try:
            driver = gdal.GetDriverByName('GTiff')
            output_dataset = driver.Create(geotiff,row,col,1,gdal.GDT_Float32)
            output_dataset.GetRasterBand(1).WriteArray(data_array)
            output_dataset.SetGeoTransform(data_set.GetGeoTransform())
            output_dataset.SetProjection(data_set.GetProjection())
            output_dataset.FlushCache()
            print(colored("#    Elapsed Time(GeoTiff Saving): %s seconds !!" % (time.time() - start_time),'green'))

        except RuntimeError as e_saving:
            print(colored('#    Error while saving data!','red'))
            print(colored('#    Error Details:','blue'))
            print(colored(e_saving,'yellow'))
            sys.exit(1)
     
class DataPlotter(object):
    
    
        #The purpose of this class is to view specific data as Plot or Print the data
    

    def __init__(self,reference_tiff_path,output_dir=None):
        self.output_dir=output_dir
        self.reference_tiff_path=reference_tiff_path

        Reader=TiffReader()
        data_set=Reader.GetDataSet(self.reference_tiff_path)
        GeoTransFormation=data_set.GetGeoTransform()
        Projection=data_set.GetProjection()
        width  = data_set.RasterXSize
        height = data_set.RasterYSize
        [x_offset,pixel_width,x_rotation,y_offset,y_rotation,pixel_height]=GeoTransFormation
        min_x = x_offset
        max_x = x_offset + pixel_width  * width  + x_rotation * height
        min_y = y_offset + pixel_height * height + y_rotation * width
        max_y = y_offset
        xps=[min_x,max_x]
        yps=[min_y,max_y]
        
        ##get CRS from dataset
        coordinate_reference_system=osr.SpatialReference()                     #Get Co-ordinate reference
        coordinate_reference_system.ImportFromWkt(Projection)                  #projection reference

        ## create lat/long CRS with WGS84 datum<GDALINFO for details>
        coordinate_reference_system_data=osr.SpatialReference()
        coordinate_reference_system_data.ImportFromEPSG(4326)                   # 4326 is the EPSG id of lat/long CRS

        transformation_term = osr.CoordinateTransformation(coordinate_reference_system,coordinate_reference_system_data)
        lons=[]
        lats=[]
        for idx in range(len(xps)):
            (lat,lon, _ ) =transformation_term.TransformPoint(xps[idx], yps[idx])
            lons.append(lon)
            lats.append(lat)

        self.extent=[lats[0],lats[1],lons[0],lons[1]]
        
    def show(self,data,identifier,plot_immediate=False,cmap='Dark2',save_png=True):
        
        print(colored('#    Plotting in Map !','green'))
        _, ax = plt.subplots(figsize=(9, 9))
        ax = Basemap(llcrnrlon=self.extent[0], llcrnrlat=self.extent[2], urcrnrlon=self.extent[1],urcrnrlat=self.extent[3], projection='merc', resolution='f')
        img = ax.imshow(data, extent=self.extent, origin='upper', cmap=cmap, vmax=1, vmin=0)
        ax.drawparallels(circles=np.arange(np.round(self.extent[2], 1), np.round(self.extent[3], 2), 0.2), labels=[True, False, False, True], dashes=[2, 2])
        ax.drawmeridians(meridians=np.arange(np.round(self.extent[0], 1), np.round(self.extent[1], 2), 0.2), labels=[True, False, False, True], dashes=[2, 2])
        ax.colorbar(img, location='right')
        plt.title(identifier)

        if save_png:
            png_path=os.path.join(self.output_dir,identifier+'.png') 
            print(colored('#    Saving figure : '+identifier+'.png at:'+self.output_dir,'green'))
            plt.savefig(png_path)
        
        if plot_immediate:
            plt.show()
        
        plt.clf()
        plt.close() 

class MaskCreator(object):
    def __init__(self,shape_file_path,reference_geotiff,mask_path,identifier):
        self.shape_file_path=shape_file_path
        self.reference_geotiff=reference_geotiff
        self.mask_path=mask_path
        self.identifier=identifier
    
    def createMask(self):
        start_time=time.time()

        reader=TiffReader()
        
        data_set=reader.GetDataSet(self.reference_geotiff)
        
        data_array=reader.GetDataArray(self.reference_geotiff)
        
        data_array=np.zeros(data_array.shape)

        shp_vector = ogr.Open(self.shape_file_path)
        
        shp_layer = shp_vector.GetLayer()
        
        geotiff=os.path.join(self.mask_path,str(self.identifier)+'_mask.tif')
        
        [col, row] = data_array.shape
        
        print(colored('#    Saving Mask: '+self.identifier+'_mask.tif at: '+self.mask_path,'blue'))
        
        try:
            driver = gdal.GetDriverByName('GTiff')
            
            output_dataset = driver.Create(geotiff,row,col,1,gdal.GDT_Float32)

            output_dataset.SetGeoTransform(data_set.GetGeoTransform())
            
            output_dataset.SetProjection(data_set.GetProjection())
            
            band = output_dataset.GetRasterBand(1)
            
            no_data_value = 0
            
            band.SetNoDataValue(no_data_value)

            band.FlushCache()
            
            gdal.RasterizeLayer(output_dataset, [1], shp_layer)

            print(colored("#    Elapsed Time(GeoTiff Saving): %s seconds !!" % (time.time() - start_time),'green'))
        
        except RuntimeError as e_saving:
            print(colored('#    Error while saving data!','red'))
            print(colored('#    Error Details:','blue'))
            print(colored(e_saving,'yellow'))
            sys.exit(1)