# -*- coding: utf-8 -*-
from __future__ import print_function
import tarfile
import gzip
import time
from glob import glob
import os 
from termcolor import colored

class LandsatInfo(object):
    def __init__(self,directory):
        self.directory=directory
        
        self.folder=os.path.basename(self.directory)            
        
        self.identifier_string=self.folder.split('_')
        
        sat_sens=self.identifier_string[0]
        ## satellite and sensor information
        if sat_sens[-1]=='8':
            self.satellite_name='Landsat 8'
        elif sat_sens[-1]=='7':
            self.satellite_name='Landsat 7'
        #O = OLI, T = TIRS, C = Combined TIRS and OLI, E = ETM+
        if sat_sens[1]=='C':
            self.sensor='C --Combined TIRS and OLI'
        elif sat_sens[1]=='O':
            self.sensor='O --OLI'
        elif sat_sens[1]=='T':
            self.sensor='T --TIRS'
        elif sat_sens[1]=='E':
            self.sensor='E --ETM+'

        self.processing_level= self.identifier_string[1]

        self.WPS_path=self.identifier_string[2][:3]

        self.WPS_row=self.identifier_string[2][3:]

        self.acquisition_time=self.identifier_string[3][6:]+'-'+self.identifier_string[3][4:6]+'-'+self.identifier_string[3][:4]

        self.processing_time=self.identifier_string[4][6:]+'-'+self.identifier_string[4][4:6]+'-'+self.identifier_string[4][:4]
        
        self.collection_number=self.identifier_string[5]

        self.collection_category=self.identifier_string[6]

        if self.collection_category=='RT':
            self.collection_category=self.collection_category+'--Real Time'
        elif self.collection_category=='T1':
            self.collection_category=self.collection_category+'--Tier 1'
        elif self.collection_category=='T2':
            self.collection_category=self.collection_category+'--Tier 2'
        
            


        
    def displayinfo(self):
        print(colored('--------------------------------------------------------------------------------------','green'))
        print(colored('#       Satelite Name : ','yellow')+ colored(self.satellite_name,'blue'))
        print(colored('#         Sensor Type : ','yellow')+ colored(self.sensor,'blue'))
        print(colored('#    Processing Level : ','yellow')+ colored(self.processing_level,'blue'))
        print(colored('#    Acquisition Date : ','yellow')+ colored(self.acquisition_time,'blue'))
        print(colored('#     Processing Date : ','yellow')+ colored(self.processing_time,'blue'))
        print(colored('#            Path Row : ','yellow')+ colored(self.WPS_path+':'+self.WPS_row,'blue'))
        print(colored('#      Collection No. : ','yellow')+ colored(self.collection_number,'blue'))
        print(colored('#     Collection Type : ','yellow')+ colored(self.collection_category,'blue'))
        
        print(colored('--------------------------------------------------------------------------------------','green'))
        print(colored('#    Listing Files !','yellow'))
        print(colored('--------------------------------------------------------------------------------------','green'))
        
        # B1
        B1=os.path.join(self.directory,str(self.folder)+'_B1.TIF')
        if os.path.isfile(B1):
            print('B1 Found!!')
            self.B1=B1
        else:
            print('B1 Missing!!')
        # B2
        B2=os.path.join(self.directory,str(self.folder)+'_B2.TIF')
        if os.path.isfile(B2):
            print('B2 Found!!')
            self.B2=B2 
        else:
            print('B2 Missing!!')
        # B3
        B3=os.path.join(self.directory,str(self.folder)+'_B3.TIF')
        if os.path.isfile(B3):
            print('B3 Found!!')
            self.B3=B3
        else:
            print('B3 Missing!!')
        # B4
        B4=os.path.join(self.directory,str(self.folder)+'_B4.TIF')
        if os.path.isfile(B4):
            print('B4 Found!!')
            self.B4=B4
        else:
            print('B4 Missing!!')
        # B5
        B5=os.path.join(self.directory,str(self.folder)+'_B5.TIF')
        if os.path.isfile(B5):
            print('B5 Found!!')
            self.B5=B5 
        else:
            print('B5 Missing!!')
        # B6
        if self.satellite_name=='Landsat 8':
            B6=os.path.join(self.directory,str(self.folder)+'_B6.TIF')
            if os.path.isfile(B6):
                print('B6 Found!!')
                self.B6=B6 
            else:
                print('B6 Missing!!')
        elif self.satellite_name=='Landsat 7':
            B6_VCID_1=os.path.join(self.directory,str(self.folder)+'_B6_VCID_1.TIF')
            if os.path.isfile(B6_VCID_1):
                print('B6 Visual Channel Identifier 1 Found!!')
                self.B6_VCID_1=B6_VCID_1 
            else:
                print('B6 Visual Channel Identifier 1  Missing!!')
            B6_VCID_2=os.path.join(self.directory,str(self.folder)+'_B6_VCID_2.TIF')
            if os.path.isfile(B6_VCID_2):
                print('B6 Visual Channel Identifier 2 Found!!')
                self.B6_VCID_2=B6_VCID_2 
            else:
                print('B6 Visual Channel Identifier 2  Missing!!')
        # B7
        B7=os.path.join(self.directory,str(self.folder)+'_B7.TIF')
        if os.path.isfile(B7):
            print('B7 Found!!')
            self.B7=B7
        else:
            print('B7 Missing!!')
        # B8
        B8=os.path.join(self.directory,str(self.folder)+'_B8.TIF')
        if os.path.isfile(B8):
            print('B8 Found!!')
            self.B8=B8
        else:
            print('B8 Missing!!')
        
        if self.satellite_name=='Landsat 8':    
            # B9
            B9=os.path.join(self.directory,str(self.folder)+'_B9.TIF')
            if os.path.isfile(B9):
                print('B9 Found!!')
                self.B9=B9
            else:
                print('B9 Missing!!')
            # B10
            B10=os.path.join(self.directory,str(self.folder)+'_B10.TIF')
            if os.path.isfile(B10):
                print('B10 Found!!')
                self.B10=B10
            else:
                print('B10 Missing!!')
            # B11
            B11=os.path.join(self.directory,str(self.folder)+'_B11.TIF')
            if os.path.isfile(B11):
                print('B11 Found!!')
                self.B11=B11
            else:
                print('B11 Missing!!')
            # BQA
            BQA=os.path.join(self.directory,str(self.folder)+'_BQA.TIF')
            if os.path.isfile(BQA):
                print('BQA Found!!')
                self.BQA=BQA
            else:
                print('BQA Missing!!')
        else:
            # BQA
            BQA=os.path.join(self.directory,str(self.folder)+'_BQA.TIF')
            if os.path.isfile(BQA):
                print('BQA Found!!')
                self.BQA=BQA
            else:
                print('BQA Missing!!')
            
            gap_mask_folder=os.path.join(self.directory,'gap_mask')
            if os.path.exists(gap_mask_folder):
                print('#    Gap Mask Folder Found')
                # GM_B1        
                GM_B1=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B1.TIF')
                if os.path.isfile(GM_B1):
                    print(colored('#    Gap Mask for B1 found!!!','yellow'))
                    self.GM_B1=GM_B1
                else:
                    print(colored('#    Gap Mask for B1 Missing!!!','red'))
                # GM_B2        
                GM_B2=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B2.TIF')
                if os.path.isfile(GM_B2):
                    print(colored('#    Gap Mask for B2 found!!!','yellow'))
                    self.GM_B2=GM_B2
                else:
                    print(colored('#    Gap Mask for B2 Missing!!!','red'))
                # GM_B3        
                GM_B3=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B3.TIF')
                if os.path.isfile(GM_B3):
                    print(colored('#    Gap Mask for B3 found!!!','yellow'))
                    self.GM_B3=GM_B3
                else:
                    print(colored('#    Gap Mask for B3 Missing!!!','red'))
                # GM_B4        
                GM_B4=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B4.TIF')
                if os.path.isfile(GM_B4):
                    print(colored('#    Gap Mask for B4 found!!!','yellow'))
                    self.GM_B4=GM_B4
                else:
                    print(colored('#    Gap Mask for B4 Missing!!!','red'))
                # GM_B5        
                GM_B5=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B5.TIF')
                if os.path.isfile(GM_B5):
                    print(colored('#    Gap Mask for B5 found!!!','yellow'))
                    self.GM_B5=GM_B5
                else:
                    print(colored('#    Gap Mask for B5 Missing!!!','red'))
                # GM_B6_VCID_1        
                GM_B6_VCID_1=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B6_VCID_1.TIF')
                if os.path.isfile(GM_B6_VCID_1):
                    print(colored('#    Gap Mask for B6 VCID 1 found!!!','yellow'))
                    self.GM_B6_VCID_1=GM_B6_VCID_1
                else:
                    print(colored('#    Gap Mask for B6 VCID 1 Missing!!!','red'))
                # GM_B6_VCID_2        
                GM_B6_VCID_2=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B6_VCID_2.TIF')
                if os.path.isfile(GM_B6_VCID_2):
                    print(colored('#    Gap Mask for B6 VCID 2 found!!!','yellow'))
                    self.GM_B6_VCID_2=GM_B6_VCID_2
                else:
                    print(colored('#    Gap Mask for B6 VCID 2 Missing!!!','red'))
                # GM_B7        
                GM_B7=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B7.TIF')
                if os.path.isfile(GM_B7):
                    print(colored('#    Gap Mask for B7 found!!!','yellow'))
                    self.GM_B7=GM_B7
                else:
                    print(colored('#    Gap Mask for B7 Missing!!!','red'))
                # GM_B8        
                GM_B8=os.path.join(gap_mask_folder,str(self.folder)+'_GM_B8.TIF')
                if os.path.isfile(GM_B8):
                    print(colored('#    Gap Mask for B8 found!!!','yellow'))
                    self.GM_B8=GM_B8
                else:
                    print(colored('#    Gap Mask for B8 Missing!!!','red'))
            else:
                print(colored('#    Gap Mask folder Missing!!!','red'))

        print(colored('--------------------------------------------------------------------------------------','green'))
    

class LandsatDataExtractor(object):
    
    def __init__(self, indir, outdir):
        self.input_dir = indir
        self.data_dir = os.path.join(outdir, 'LandsatData')
        self.info=None
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
    
    def __listpathrows(self):
        path_rows=[]
        for data_path in glob(os.path.join(self.input_dir,'**/*.tar.gz'),recursive=True):
            tar_file=os.path.basename(data_path).replace('.tar.gz','')
            self.info=LandsatInfo(tar_file)
            path_row=self.info.WPS_path+self.info.WPS_row
            path_rows.append(path_row)
            
            

        
        path_rows=set(path_rows)
        self.path_rows=path_rows

    def __createpathrowsdirectory(self):
        self.pathrowdir=[]
        for path_row in self.path_rows:
            path_row_folder=os.path.join(self.data_dir,str(path_row))
            if not os.path.exists(path_row_folder):
                os.mkdir(path_row_folder)
            self.pathrowdir.append(path_row_folder)
    
    def __extracttodir(self):
        for fname in  glob(os.path.join(self.input_dir,'**/*.tar.gz'),recursive=True):     
            start_time=time.time()
            
            tar_file=os.path.basename(fname).replace('.tar.gz','')
            path_row=self.info.WPS_path+self.info.WPS_row

            tar = tarfile.open(fname, "r:gz")
            print(colored('#    Uncompressing: {} !!!'.format(fname),'yellow'))
            tar.extractall(path=os.path.join(self.data_dir,path_row,tar_file))
            tar.close()
            print('#    Time Taken:' + str(time.time()-start_time))

            if self.info.satellite_name=='Landsat 7':
                gap_mask_path=os.path.join(self.input_dir,'LandsatData',path_row,tar_file,'gap_mask')
                
                if os.path.exists(gap_mask_path):
                    
                    for gz_file_path in glob(os.path.join(gap_mask_path,'**/*.gz'),recursive=True):
                        
                        with gzip.open(gz_file_path, 'rb') as f_in:
                            file_content = f_in.read()

                        tif_file_path=os.path.join(gap_mask_path,os.path.basename(gz_file_path).replace('.gz',''))
                        with open(tif_file_path, 'wb') as f_out:
                            f_out.write(file_content)
                        os.remove(gz_file_path)
                        print(colored('Deleting: {} !!!'.format(gz_file_path),'red'))
    
    def extract(self):
        self.__listpathrows()
        self.__createpathrowsdirectory()
        self.__extracttodir()