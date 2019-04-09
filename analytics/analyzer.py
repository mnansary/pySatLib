# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np 
import time
import sys
import os
from termcolor import colored
import matplotlib.pyplot as plt 
from utilities.commonutils import TiffReader,DataPlotter,TiffWriter
from utilities.Sentinel2 import Sentinel2Info,Sentinel2DataPreprocessor

np.seterr(divide='ignore', invalid='ignore') # Ignore Runtime Warnings


class Sentinel2Analyzer(object):
    def __init__(self,mask_path=None,analytics_data_path=None):
        self.mask_path=mask_path
        self.analytics_data_path=analytics_data_path
        self.reader=TiffReader()
        self.writer=TiffWriter()
        self.analytics_parameters=['Satelite_Name', 'Processing_Level', 'Acquisition_Date', 
                                    'Acquisition_Time', 'Tile_Identifier', 'Metadata_Type', 
                                    'Metadata_Version', 'FRE_B2', 'FRE_B3', 'FRE_B4', 'FRE_B5', 
                                    'FRE_B6', 'FRE_B7', 'FRE_B8', 'FRE_B8A', 'FRE_B11', 'FRE_B12', 
                                    'ATB_R1_WVC', 'ATB_R1_AOT', 'ATB_R2_WVC', 'ATB_R2_AOT']
    def normalizeData(self,data):
        data=(data-np.nanmin(data))/(np.nanmax(data)-np.nanmin(data))
        return data
    

    def __processMaskData(self):
        data=self.reader.GetDataArray(self.mask_path)
        data=(data-np.nanmin(data))/(np.nanmax(data)-np.nanmin(data))
        return data
    
    def __dataCheck(self,data,identifier):
        
        image_dir=os.path.join(self.analytics_data_path,self.info.zone)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        image_dir=os.path.join(image_dir,os.path.basename(self.direcroty))
        
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        
        plt.figure(identifier)
        plt.title(identifier)
        plt.grid(True)
        plt.imshow(data)
        savename = os.path.join(image_dir,'{}.png'.format(identifier))
        print('# Saving:     '+colored( identifier,'green')+colored('          at:{}'.format(image_dir),'yellow'))
        plt.savefig(savename)
        plt.clf()
        plt.close()
    
    
    def __genFREAnalytics(self,dataCheck_Flag=False,masked_flag=True):
        P_key='FRE'

        for B_key in self.info.info_dict[P_key]:
            
            identifier='{}_{}'.format(P_key,B_key)

            data_path=self.info.info_dict[P_key][B_key]
        
            print(colored('Processing:','yellow')+colored(data_path,'green'))
        
            if B_key in self.info.info_res:
                cloud_mask_path=self.info.CLM_R1
                data=self.preprocessor.preprocessData(cloud_mask_path,data_path)
            else:
                cloud_mask_path=self.info.CLM_R2
                data=self.preprocessor.preprocessData(cloud_mask_path,data_path,resolution=20)
            
            if masked_flag:
                data[self.mask_data==0]=np.nan

            if dataCheck_Flag:
                
                self.__dataCheck(data,identifier)
            
            data_median=np.nanmedian(data)
            
            print(colored('# Median of {}:   '.format(identifier),'white')+ colored(data_median,'yellow')) 
            
            self.analytics_values.append(data_median)
    
    def __genATBAnalytics(self,dataCheck_Flag=False,masked_flag=True):
        P_key='ATB'
        
        for R_key in self.info.info_dict[P_key]:
            
            WVC_identifier='{}_{}_WVC'.format(P_key,R_key)
            AOT_identifier='{}_{}_AOT'.format(P_key,R_key)
            
            data_path=self.info.info_dict[P_key][R_key]
            print(colored('Processing:','yellow')+colored(data_path,'green'))
            
            self.preprocessor.raster_count=2
            
            if R_key=='R1':
                cloud_mask_path=self.info.CLM_R1
                
                self.preprocessor.raster_num=1
                data_WVC=self.preprocessor.preprocessData(cloud_mask_path,data_path,fromDataSetFlag=True)
                
                self.preprocessor.raster_num=2
                data_AOT=self.preprocessor.preprocessData(cloud_mask_path,data_path,fromDataSetFlag=True)
                
            else:
                cloud_mask_path=self.info.CLM_R2
                
                self.preprocessor.raster_num=1
                data_WVC=self.preprocessor.preprocessData(cloud_mask_path,data_path,resolution=20,fromDataSetFlag=True)
                
                self.preprocessor.raster_num=2
                data_AOT=self.preprocessor.preprocessData(cloud_mask_path,data_path,resolution=20,fromDataSetFlag=True)
            
            if masked_flag:
                data_WVC[self.mask_data==0]=np.nan
                data_AOT[self.mask_data==0]=np.nan

            if dataCheck_Flag:
                self.__dataCheck(data_WVC,WVC_identifier)
                self.__dataCheck(data_AOT,AOT_identifier)
            
            WVC_median=np.nanmedian(data_WVC)
            AOT_median=np.nanmedian(data_AOT)
            
            print(colored('# Median of {}:   '.format(WVC_identifier),'white')+ colored(WVC_median,'yellow')) 
            print(colored('# Median of {}:   '.format(AOT_identifier),'white')+ colored(AOT_median,'yellow'))

            self.analytics_values.append(WVC_median)
            
            self.analytics_values.append(AOT_median)

    def generateAnalytics(self,direcroty,FRE_Flag=True,ATB_Flag=True,dataCheck_Flag=False,masked_flag=True):
        self.direcroty=direcroty
        
        print(colored('# Generating Analytics:'+colored(os.path.basename(self.direcroty),'yellow'),'green'))
        
        self.analytics_data_path=os.path.join(self.analytics_data_path,'Analytics')
        
        if not os.path.exists(self.analytics_data_path):
            os.mkdir(self.analytics_data_path)

        self.info=Sentinel2Info(self.direcroty)
        
        self.analytics_values=self.info.info_value
        
        self.preprocessor=Sentinel2DataPreprocessor()

        if masked_flag:    
            self.mask_data= self.__processMaskData()
        if FRE_Flag:
            self.__genFREAnalytics(dataCheck_Flag=dataCheck_Flag,masked_flag=masked_flag)
        if ATB_Flag:
            self.__genATBAnalytics(dataCheck_Flag=dataCheck_Flag,masked_flag=masked_flag)

    def __saveNDVI(self,masked_flag,save_tiff=True):
        RED=self.preprocessor.preprocessData(self.info.CLM_R1,self.info.FRE_B4)
        NIR=self.preprocessor.preprocessData(self.info.CLM_R1,self.info.FRE_B8)
        NDVI=(NIR-RED)/(NIR+RED)
        if masked_flag:
            NDVI[self.mask_data==0]=np.nan
        NDVI=self.normalizeData(NDVI)
        self.plotter.show(NDVI,'{}_NDVI'.format(self.indetifier))
        if save_tiff:
            self.writer.save(NDVI,'{}_NDVI'.format(self.indetifier))

    def __saveNDWI(self,masked_flag,save_tiff=True):
        NIR=self.preprocessor.preprocessData(self.info.CLM_R1,self.info.FRE_B8)
        SWIR=self.preprocessor.preprocessData(self.info.CLM_R2,self.info.FRE_B11,resolution=20)        
        NDWI=(NIR-SWIR)/(NIR+SWIR)
        if masked_flag:
            NDWI[self.mask_data==0]=np.nan
        NDWI=self.normalizeData(NDWI)
        self.plotter.show(NDWI,'{}_NDWI'.format(self.indetifier))
        if save_tiff:
            self.writer.save(NDWI,'{}_NDWI'.format(self.indetifier))


    def genIndexData(self,direcroty,NDVI_Flag=True,NDWI_Flag=True,masked_flag=True):
        self.analytics_data_path=os.path.join(self.analytics_data_path,'Analytics')
        if not os.path.exists(self.analytics_data_path):
            os.mkdir(self.analytics_data_path)

        self.info=Sentinel2Info(direcroty)
        self.indetifier=self.info.folder

        self.preprocessor=Sentinel2DataPreprocessor()
        
        output_dir=os.path.join(self.analytics_data_path,self.info.zone)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_dir=os.path.join(output_dir,self.indetifier)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)


        self.plotter=DataPlotter(reference_tiff_path=self.mask_path,output_dir=output_dir)

        self.writer.saving_directory=output_dir
        
        self.writer.reference_tiff_path=self.mask_path
        
        if masked_flag:    
            self.mask_data= self.__processMaskData()
        
        if NDVI_Flag:
            self.__saveNDVI(masked_flag)

        if NDWI_Flag:
            self.__saveNDWI(masked_flag)

        
                        

