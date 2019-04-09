# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
import numpy as np
import os
import argparse
import time
import pandas as pd
from termcolor import colored
from analytics.analyzer import Sentinel2Analyzer


parser = argparse.ArgumentParser(description='Sentinel 2 All band median analytics ')
parser.add_argument("datafolder", help="/path/to/Data/Folder")
parser.add_argument("maskPath", help="/path/to/geotiff/mask.tiff")
parser.add_argument("analyticsSavingPath", help="/path/to/save/analytics_data")

args = parser.parse_args()
data_dir=args.datafolder
mask_path=args.maskPath
analytics_data_path=args.analyticsSavingPath

analyzer=Sentinel2Analyzer()

df=pd.DataFrame(columns=analyzer.analytics_parameters)

saveAsCSV=True


def moduleRun(data_dir,df):
    zones=os.listdir(data_dir)    
    for zone in zones:
        dpath=os.path.join(data_dir,zone)
        fpaths=os.listdir(dpath)
        for fpath in fpaths:
            start_time = time.time()
            
            directory=os.path.join(data_dir,zone,fpath)
            
            get_analytics(directory,mask_path,analytics_data_path)
            
            temp=pd.DataFrame([analyzer.analytics_values],columns=analyzer.analytics_parameters)
            
            df=df.append(temp,ignore_index=True)

            print(colored('\t|- Time Elapsed : {file_name:s} in {te:s}'.format(file_name=os.path.basename(directory),te=str(time.time()-start_time)),'red'))
            
            print()
    
    return df 

def get_analytics(directory,mask_path,analytics_data_path):
    analyzer.mask_path=mask_path
    analyzer.analytics_data_path=analytics_data_path
    analyzer.generateAnalytics(directory)

'''
CODE TO TURN CSV INTO DF:
csv_file_name=''
df=pd.read_csv(csv_file_name,sep='\t',skiprows=[0],names=col_names)
    
'''


if __name__=='__main__':
    
    df=moduleRun(data_dir,df)
    
    df['Acquisition_Date']=pd.to_datetime(df['Acquisition_Date'])
    
    df.set_index(['Acquisition_Date'],inplace=True)
    
    df=df.sort_index()
    
    csv_file_name=os.path.join(analyzer.analytics_data_path,'analytics.csv')

    df.to_csv(csv_file_name, sep='\t', encoding='utf-8')

    print(colored('# Saved analytics at: {}'.format(csv_file_name),'green'))
    