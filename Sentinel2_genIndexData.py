# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
import numpy as np 
import os
import argparse
from termcolor import colored

from analytics.analyzer import Sentinel2Analyzer

parser = argparse.ArgumentParser()
parser.add_argument("datafolder", help="/path/to/Data/Folder")
parser.add_argument("maskPath", help="/path/to/geotiff/mask.tiff")
parser.add_argument("analyticsSavingPath", help="/path/to/save/analytics_data")

args = parser.parse_args()
data_dir=args.datafolder
mask_path=args.maskPath
analytics_data_path=args.analyticsSavingPath



def moduleRun(data_dir,mask_path,analytics_data_path):
    zones=os.listdir(data_dir)    
    for zone in zones:
        dpath=os.path.join(data_dir,zone)
        fpaths=os.listdir(dpath)
        for fpath in fpaths:
            directory=os.path.join(data_dir,zone,fpath)
            saveIndexBands(directory,mask_path,analytics_data_path)

def saveIndexBands(directory,mask_path,analytics_data_path):
    analyzer=Sentinel2Analyzer(mask_path=mask_path,analytics_data_path=analytics_data_path)
    analyzer.genIndexData(directory,masked_flag=False)
    
if __name__=='__main__':
    #saveIndexBands(data_dir,mask_path,analytics_data_path)    
    moduleRun(data_dir,mask_path,analytics_data_path)