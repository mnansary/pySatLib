# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
from termcolor import colored
import argparse
from utilities.commonutils import MaskCreator,TiffReader
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Mask Creation from shape file and Geotiff')
parser.add_argument("shp_path", help="/path/to/shape/file.shp")
parser.add_argument("ref_tif_path", help="/path/to/geotiff/file.tif")
parser.add_argument("mask_path", help="/path/to/save/mask.tif")
parser.add_argument("identifier", help="location identifier")


args = parser.parse_args()
shape_file_path=args.shp_path
reference_tif_file_path=args.ref_tif_path
mask_path=args.mask_path
identifier=args.identifier

def create_mask(reference_tif_file_path,shape_file_path,mask_path,identifier):
    genObj=MaskCreator(shape_file_path,reference_tif_file_path,mask_path,identifier)
    genObj.createMask()

if __name__=="__main__":
    create_mask(reference_tif_file_path,shape_file_path,mask_path,identifier)
    