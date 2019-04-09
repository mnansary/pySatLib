# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
import numpy as np 
import os
import argparse
from termcolor import colored
import scipy
import scipy.ndimage.measurements
from utilities.commonutils import TiffReader,TiffWriter,DataPlotter
from utilities.Sentinel2 import Sentinel2Info,Sentinel2DataPreprocessor

parser = argparse.ArgumentParser(description='Sentinel 2 WaterMask creater with half std threshold and blob filter ')
parser.add_argument("data_dir", help="/path/to/Data/Folder")
parser.add_argument("output_path", help="/path/to/save/mask/")

args = parser.parse_args()
data_dir=args.data_dir
output_path=args.output_path

def processSWIR(directory):
    info=Sentinel2Info(directory)
    preprocessor=Sentinel2DataPreprocessor()
    SWIR_B12=preprocessor.preprocessData(info.CLM_R2,info.FRE_B12,resolution=20)
    return SWIR_B12

def reference_tiff(data_dir,zone):
    dataPath=str(os.path.join(data_dir,zone))
    dataFolders=os.listdir(dataPath)
    directory=os.path.join(dataPath,dataFolders[0])
    info=Sentinel2Info(directory)
    ref_tiff_path=info.FRE_B8
    return ref_tiff_path


def moduleRun(data_dir,output_path,factor=0.5,water_blob_size=10000,land_blob_size=5000):
    reader=TiffReader()
    zones=os.listdir(data_dir)    
    for zone in zones:
        dpath=os.path.join(data_dir,zone)
        fpaths=os.listdir(dpath)

        ref_tiff_path=reference_tiff(data_dir,zone)
        ref_tiff_data=reader.GetDataArray(ref_tiff_path)
        
        combined_data=np.empty(ref_tiff_data.shape)
        combined_data=combined_data.astype(np.float)
        combined_data[:]=np.nan
        
        data_holder=np.empty((ref_tiff_data.shape[0],ref_tiff_data.shape[1],2),dtype=np.float)
        
        for fpath in fpaths:
            directory=os.path.join(data_dir,zone,fpath)
            data=processSWIR(directory)
            data_holder[:,:,0]=combined_data
            data_holder[:,:,1]=data
        
            combined_data = np.nanmean(data_holder,axis=-1,keepdims=False)
        
        combined_data = (combined_data-np.nanmin(combined_data))/(np.nanmax(combined_data)-np.nanmin(combined_data))

        combined_data=combined_data/np.nanstd(combined_data)

        water_mask_data=np.ones(combined_data.shape)
        
        water_mask_data[combined_data>factor]=0
        
        WF=np.zeros(water_mask_data.shape)
        
        #WaterFilter
        Thresh=water_blob_size
        LabeledData,_=scipy.ndimage.measurements.label(water_mask_data)
        _,PixelCount=np.unique(LabeledData,return_counts=True)
        __SignificantFeatures=np.argwhere(PixelCount>Thresh).ravel()
        __SignificantFeatures=__SignificantFeatures[__SignificantFeatures>0]
        
        for sigF in __SignificantFeatures:
            WF[LabeledData==sigF]=1
        
        #LandFilter
        Land=1-WF
        Thresh=land_blob_size
        LabeledData,_=scipy.ndimage.measurements.label(Land)
        _,PixelCount=np.unique(LabeledData,return_counts=True)
        __SignificantFeatures=np.argwhere(PixelCount>Thresh).ravel()
        __SignificantFeatures=__SignificantFeatures[__SignificantFeatures>0]
        for sigF in __SignificantFeatures:
            Land[LabeledData==sigF]=0
        
        WF[Land==1]=1


        writer=TiffWriter()
        writer.reference_tiff_path=ref_tiff_path
        writer.saving_directory=output_path
        writer.save(WF,'WaterMask_Sentinel2_{}'.format(zone))
        plotter=DataPlotter(reference_tiff_path=ref_tiff_path,output_dir=output_path)
        plotter.show(WF,'WaterMask_Sentinel2_{}'.format(zone))


if __name__=='__main__':
    moduleRun(data_dir,output_path)