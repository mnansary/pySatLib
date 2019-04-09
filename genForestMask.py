# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
import numpy as np 
from termcolor import colored
import argparse
from utilities.commonutils import TiffReader,TiffWriter
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Forest Mask Creation from WaterMask And Area Mask')
parser.add_argument("water_mask_path", help="/path/to/water_mask/file.tif")
parser.add_argument("area_mask_path", help="/path/to/area_mask/file.tif")
parser.add_argument("mask_path", help="/path/to/save/mask.tif")
parser.add_argument("identifier", help="location identifier")

args = parser.parse_args()
water_mask_path=args.water_mask_path
area_mask_path=args.area_mask_path
mask_path=args.mask_path
identifier=args.identifier

def create_mask():
    reader=TiffReader()
    water_mask_data=reader.GetDataArray(water_mask_path)
    area_mask_data=reader.GetDataArray(area_mask_path)
    
    forest_mask_data=np.zeros(area_mask_data.shape)
    forest_mask_data[area_mask_data==255]=1
    forest_mask_data[water_mask_data==1]=0

    writer=TiffWriter()
    writer.reference_tiff_path=area_mask_path
    writer.saving_directory=mask_path
    writer.save(forest_mask_data,identifier)


if __name__=="__main__":
    create_mask()
