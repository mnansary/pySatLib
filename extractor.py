# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import print_function
from utilities.Landsat import LandsatDataExtractor
from utilities.Sentinel2 import Sentinel2DataExtractor
from termcolor import colored

import argparse
parser = argparse.ArgumentParser(description='Data Extraction from compressed data files.')
parser.add_argument("source", help="/path/to/compressed/data")
parser.add_argument("target", help="/desired/path/for/uncommpressing/the/data")
parser.add_argument("satellite", help="Satellite Name: Landsat / Sentinel2")

args = parser.parse_args()
source=args.source
target=args.target
satellite=args.satellite

def extract_Landsat(source,target):
    data_extractor=LandsatDataExtractor(source,target)
    data_extractor.extract()

def extract_Sentinel2(source,target):
    data_extractor=Sentinel2DataExtractor(source,target)
    data_extractor.extract()

if __name__ == "__main__":
    if satellite=='Landsat':
        extract_Landsat(source,target)
    elif satellite=='Sentinel2':
        extract_Sentinel2(source,target)
    else:
        print(colored('Check Satellite Name: Landsat / Sentinel2!!!','red'))