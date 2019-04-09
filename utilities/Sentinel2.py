# -*- coding: utf-8 -*-
from __future__ import print_function
import os 
import numpy as np
from termcolor import colored
from glob import glob
import zipfile
import time

from .commonutils import TiffReader

class Sentinel2Info(object):
    '''
        The purpose of this class is to collect useable data from the input data
    '''


    def __init__(self,directory):
        
        self.directory=directory                                          
        
        self.folder=os.path.basename(self.directory)    
        
        identifiers=self.folder.split('_')
        
        self.satellite_name=identifiers[0]
        
        date_time_stamp=identifiers[1].split('-')        #Time stamp data 
        
        self.date=date_time_stamp[0][6:]+'-'+date_time_stamp[0][4:6]+'-'+date_time_stamp[0][0:4]
        
        self.time=date_time_stamp[1][0:2]+':'+date_time_stamp[1][2:4]+':'+date_time_stamp[1][4:]+':'+date_time_stamp[2]+' ms'

        self.processing_level=identifiers[2]
        
        self.zone=identifiers[3]
    
        self.meta_data_type=identifiers[4]
        
        self.meta_data_version=identifiers[5] 
       

        self.info_value=[self.satellite_name,self.processing_level,self.date,self.time,self.zone,self.meta_data_type,self.meta_data_version]
        
        self.info_dict={'ATB':{},'FRE':{}}

        self.info_res=['B2','B3','B4','B8']

        self.__collectInfo()
    
    def __collectInfo(self):
        '''
            Displays information about the data
        '''
        print(colored('--------------------------------------------------------------------------------------','green'))
        print(colored('#       Satelite Name : ','yellow')+ colored(self.satellite_name,'blue'))
        print(colored('#    Processing Level : ','yellow')+ colored(self.processing_level,'blue'))
        print(colored('#    Acquisition Date : ','yellow')+ colored(self.date,'blue'))
        print(colored('#    Acquisition Time : ','yellow')+ colored(self.time,'blue'))
        print(colored('#     Tile Identifier : ','yellow')+ colored(self.zone,'blue'))
        print(colored('#       Metadata Type : ','yellow')+ colored(self.meta_data_type,'blue'))
        print(colored('#    Metadata Version : ','yellow')+ colored(self.meta_data_version,'blue'))
        
        print(colored('--------------------------------------------------------------------------------------','green'))
        print(colored('#    Listing Files !','yellow'))
        print(colored('--------------------------------------------------------------------------------------','green'))
        



        #ATB_R1
        ATB_R1=os.path.join(self.directory,str(self.folder)+'_ATB_R1.tif')
        if os.path.isfile(ATB_R1):
            print('ATB R1 found!!!')
            print(colored('#    Atmospheric and biophysical parameter Band: Coastal Aerosol and Water Vapour content - 2 raster - 10m','cyan'))
            self.ATB_R1=ATB_R1
            self.info_dict['ATB']['R1']=self.ATB_R1
        else:
            print('ATB R1 missing!!!')
        #ATB_R2
        ATB_R2=os.path.join(self.directory,str(self.folder)+'_ATB_R2.tif')
        if os.path.isfile(ATB_R2):
            print('ATB R2 found!!!')
            print(colored('#    Atmospheric and biophysical parameter Band: Coastal Aerosol and Water Vapour content - 2 raster - 20m','cyan'))
            self.ATB_R2=ATB_R2
            self.info_dict['ATB']['R2']=self.ATB_R2
        else:
            print('ATB R2 missing!!!')
        #------------------------FRE-------------------------------------------
        #FRE_B2
        FRE_B2=os.path.join(self.directory,str(self.folder)+'_FRE_B2.tif')
        if os.path.isfile(FRE_B2):
            print('FRE B2 found!!!')
            print(colored('#    Blue Band -with the correction of slope effects- 1 raster - 10m','cyan'))
            self.FRE_B2=FRE_B2
            self.info_dict['FRE']['B2']=self.FRE_B2
        else:
            print('FRE B2 missing!!!')
        #FRE_B3
        FRE_B3=os.path.join(self.directory,str(self.folder)+'_FRE_B3.tif')
        if os.path.isfile(FRE_B3):
            print('FRE B3 found!!!')
            print(colored('#    Green Band -with the correction of slope effects- 1 raster - 10m','cyan'))
            self.FRE_B3=FRE_B3
            self.info_dict['FRE']['B3']=self.FRE_B3
        else:
            print('FRE B3 missing!!!')
        #FRE_B4
        FRE_B4=os.path.join(self.directory,str(self.folder)+'_FRE_B4.tif')
        if os.path.isfile(FRE_B4):
            print('FRE B4 found!!!')
            print(colored('#    Red Band -with the correction of slope effects- 1 raster - 10m','cyan'))
            self.FRE_B4=FRE_B4
            self.info_dict['FRE']['B4']=self.FRE_B4
        else:
            print('FRE B4 missing!!!')
        #FRE_B5
        FRE_B5=os.path.join(self.directory,str(self.folder)+'_FRE_B5.tif')
        if os.path.isfile(FRE_B5):
            print('FRE B5 found!!!')
            print(colored('#    Vegetation red edge -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B5=FRE_B5
            self.info_dict['FRE']['B5']=self.FRE_B5
        else:
            print('FRE B5 missing!!!')
        #FRE_B6
        FRE_B6=os.path.join(self.directory,str(self.folder)+'_FRE_B6.tif')
        if os.path.isfile(FRE_B6):
            print('FRE B6 found!!!')
            print(colored('#    Vegetation red edge -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B6=FRE_B6
            self.info_dict['FRE']['B6']=self.FRE_B6
        else:
            print('FRE B6 missing!!!')
        #FRE_B7
        FRE_B7=os.path.join(self.directory,str(self.folder)+'_FRE_B7.tif')
        if os.path.isfile(FRE_B7):
            print('FRE B7 found!!!')
            print(colored('#    Vegetation red edge -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B7=FRE_B7
            self.info_dict['FRE']['B7']=self.FRE_B7
        else:
            print('FRE B7 missing!!!')
        #FRE_B8
        FRE_B8=os.path.join(self.directory,str(self.folder)+'_FRE_B8.tif')
        if os.path.isfile(FRE_B8):
            print('FRE B8 found!!!')
            print(colored('#    NIR:Near Infrared -with the correction of slope effects- 1 raster - 10m','cyan'))
            self.FRE_B8=FRE_B8
            self.info_dict['FRE']['B8']=self.FRE_B8

        else:
            print('FRE B8 missing!!!')
        #FRE_B8A
        FRE_B8A=os.path.join(self.directory,str(self.folder)+'_FRE_B8A.tif')
        if os.path.isfile(FRE_B8A):
            print('FRE B8A found!!!')
            print(colored('#    Vegetation red edge -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B8A=FRE_B8A
            self.info_dict['FRE']['B8A']=self.FRE_B8A
        else:
            print('FRE B8A missing!!!')
        #FRE_B11
        FRE_B11=os.path.join(self.directory,str(self.folder)+'_FRE_B11.tif')
        if os.path.isfile(FRE_B11):
            print('FRE B11 found!!!')
            print(colored('#    SWIR: Short Wave Infrared -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B11=FRE_B11
            self.info_dict['FRE']['B11']=self.FRE_B11
        else:
            print('FRE B11 missing!!!')
        #FRE_B12
        FRE_B12=os.path.join(self.directory,str(self.folder)+'_FRE_B12.tif')
        if os.path.isfile(FRE_B12):
            print('FRE B12 found!!!')
            print(colored('#    SWIR: Short Wave Infrared -with the correction of slope effects- 1 raster - 20m','cyan'))
            self.FRE_B12=FRE_B12
            self.info_dict['FRE']['B12']=self.FRE_B12
        else:
            print('FRE B12 missing!!!')
        #------------------------SRE-------------------------------------------
        #SRE_B2
        SRE_B2=os.path.join(self.directory,str(self.folder)+'_SRE_B2.tif')
        if os.path.isfile(SRE_B2):
            print('SRE B2 found!!!')
            print(colored('#    Blue Band -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 10m','cyan'),'cyan'))
            self.SRE_B2=SRE_B2
        else:
            print('SRE B2 missing!!!')
        #SRE_B3
        SRE_B3=os.path.join(self.directory,str(self.folder)+'_SRE_B3.tif')
        if os.path.isfile(SRE_B3):
            print('SRE B3 found!!!')
            print(colored('#    Green Band -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 10m','cyan'),'cyan'))
            self.SRE_B3=SRE_B3
        else:
            print('SRE B3 missing!!!')
        #SRE_B4
        SRE_B4=os.path.join(self.directory,str(self.folder)+'_SRE_B4.tif')
        if os.path.isfile(SRE_B4):
            print('SRE B4 found!!!')
            print(colored('#    Red Band -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 10m','cyan'),'cyan'))
            self.SRE_B4=SRE_B4
        else:
            print('SRE B4 missing!!!')
        #SRE_B5
        SRE_B5=os.path.join(self.directory,str(self.folder)+'_SRE_B5.tif')
        if os.path.isfile(SRE_B5):
            print('SRE B5 found!!!')
            print(colored('#    Vegetation red edge -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B5=SRE_B5
        else:
            print('SRE B5 missing!!!')
        #SRE_B6
        SRE_B6=os.path.join(self.directory,str(self.folder)+'_SRE_B6.tif')
        if os.path.isfile(SRE_B6):
            print('SRE B6 found!!!')
            print(colored('#    Vegetation red edge -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B6=SRE_B6
        else:
            print('SRE B6 missing!!!')
        #SRE_B7
        SRE_B7=os.path.join(self.directory,str(self.folder)+'_SRE_B7.tif')
        if os.path.isfile(SRE_B7):
            print('SRE B7 found!!!')
            print(colored('#    Vegetation red edge -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B7=SRE_B7
        else:
            print('SRE B7 missing!!!')
        #SRE_B8
        SRE_B8=os.path.join(self.directory,str(self.folder)+'_SRE_B8.tif')
        if os.path.isfile(SRE_B8):
            print('SRE B8 found!!!')
            print(colored('#    NIR:Near Infrared -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 10m','cyan'),'cyan'))
            self.SRE_B8=SRE_B8
        else:
            print('SRE B8 missing!!!')
        #SRE_B8A
        SRE_B8A=os.path.join(self.directory,str(self.folder)+'_SRE_B8A.tif')
        if os.path.isfile(SRE_B8A):
            print('SRE B8A found!!!')
            print(colored('#    Vegetation red edge -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B8A=SRE_B8A
        else:
            print('SRE B8A missing!!!')
        #SRE_B11
        SRE_B11=os.path.join(self.directory,str(self.folder)+'_SRE_B11.tif')
        if os.path.isfile(SRE_B11):
            print('SRE B11 found!!!')
            print(colored('#    SWIR: Short Wave Infrared -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B11=SRE_B11
        else:
            print('SRE B11 missing!!!')
        #SRE_B12
        SRE_B12=os.path.join(self.directory,str(self.folder)+'_SRE_B12.tif')
        if os.path.isfile(SRE_B12):
            print('SRE B12 found!!!')
            print(colored('#    SWIR: Short Wave Infrared -'+colored('with out','red')+colored(' the correction of slope effects- 1 raster - 20m','cyan'),'cyan'))
            self.SRE_B12=SRE_B12
        else:
            print('SRE B12 missing!!!')
        #--------------------------------MASKS-------------------------------------------
        mask_folder=os.path.join(self.directory,'MASKS')
        print()
        print(colored('#    Cloud Masks','blue'))
        #CLM_R1
        CLM_R1=os.path.join(mask_folder,str(self.folder)+'_CLM_R1.tif')
        if os.path.isfile(CLM_R1):
            print(colored('#    CLM R1 found!!!','yellow'))
            self.CLM_R1=CLM_R1
        else:
            print(colored('#    CLM R1 missing!!!','red'))   
        #CLM_R2
        CLM_R2=os.path.join(mask_folder,str(self.folder)+'_CLM_R2.tif')
        if os.path.isfile(CLM_R2):
            print(colored('#    CLM R2 found!!!','yellow'))
            self.CLM_R2=CLM_R2
        else:
            print(colored('#    CLM R2 missing!!!','red'))   
        
        print(colored('#    Edge/Nodata Masks','blue'))
        #EDG_R1
        EDG_R1=os.path.join(mask_folder,str(self.folder)+'_EDG_R1.tif')
        if os.path.isfile(EDG_R1):
            print(colored('#    EDG R1 found!!!','yellow'))
            self.EDG_R1=EDG_R1
        else:
            print(colored('#    EDG R1 missing!!!','red'))   
        #EDG_R2
        EDG_R2=os.path.join(mask_folder,str(self.folder)+'_EDG_R2.tif')
        if os.path.isfile(EDG_R2):
            print(colored('#    EDG R2 found!!!','yellow'))
            self.EDG_R2=EDG_R2
        else:
            print(colored('#    EDG R2 missing!!!','red'))   

        print(colored('#    Saturation Masks','blue'))
        #SAT_R1
        SAT_R1=os.path.join(mask_folder,str(self.folder)+'_SAT_R1.tif')
        if os.path.isfile(SAT_R1):
            print(colored('#    SAT R1 found!!!','yellow'))
            self.SAT_R1=SAT_R1
        else:
            print(colored('#    SAT R1 missing!!!','red'))   
        #SAT_R2
        SAT_R2=os.path.join(mask_folder,str(self.folder)+'_SAT_R2.tif')
        if os.path.isfile(SAT_R2):
            print(colored('#    SAT R2 found!!!','yellow'))
            self.SAT_R2=SAT_R2
        else:
            print(colored('#    SAT R2 missing!!!','red')) 
        
        print(colored('#    Defective Pixels Masks','blue'))
        #DFP_R1
        DFP_R1=os.path.join(mask_folder,str(self.folder)+'_DFP_R1.tif')
        if os.path.isfile(DFP_R1):
            print(colored('#    DFP R1 found!!!','yellow'))
            self.DFP_R1=DFP_R1
        else:
            print(colored('#    DFP R1 missing!!!','red'))   
        #DFP_R2
        DFP_R2=os.path.join(mask_folder,str(self.folder)+'_DFP_R2.tif')
        if os.path.isfile(DFP_R2):
            print(colored('#    DFP R2 found!!!','yellow'))
            self.SAT_R2=SAT_R2
        else:
            print(colored('#    DFP R2 missing!!!','red')) 
        
        print(colored('#    Geophysical Masks','blue'))
        #MG2_R1
        MG2_R1=os.path.join(mask_folder,str(self.folder)+'_MG2_R1.tif')
        if os.path.isfile(MG2_R1):
            print(colored('#    MG2 R1 found!!!','yellow'))
            self.MG2_R1=MG2_R1
        else:
            print(colored('#    MG2 R1 missing!!!','red'))   
        #MG2_R2
        MG2_R2=os.path.join(mask_folder,str(self.folder)+'_MG2_R2.tif')
        if os.path.isfile(MG2_R2):
            print(colored('#    MG2 R2 found!!!','yellow'))
            self.MG2_R2=MG2_R2
        else:
            print(colored('#    MG2 R2 missing!!!','red')) 
        
        if int(self.meta_data_version[-1])>=7:
            print(colored('#    IAB Masks','blue'))
            #IAB_R1
            IAB_R1=os.path.join(mask_folder,str(self.folder)+'_IAB_R1.tif')
            if os.path.isfile(IAB_R1):
                print(colored('#    IAB R1 found!!!','yellow'))
                self.IAB_R1=IAB_R1
            else:
                print(colored('#    IAB R1 missing!!!','red'))   
            #IAB_R2
            IAB_R2=os.path.join(mask_folder,str(self.folder)+'_IAB_R2.tif')
            if os.path.isfile(IAB_R2):
                print(colored('#    IAB R2 found!!!','yellow'))
                self.IAB_R2=IAB_R2
            else:
                print(colored('#    IAB R2 missing!!!','red'))
        else:
            print(colored('#    Interpolated AOT pixels','blue'))
            #IAO_R1
            IAO_R1=os.path.join(mask_folder,str(self.folder)+'_IAO_R1.tif')
            if os.path.isfile(IAO_R1):
                print(colored('#    IAO R1 found!!!','yellow'))
                self.IAO_R1=IAO_R1
            else:
                print(colored('#    IAO R1 missing!!!','red'))   
            #IAB_R2
            IAO_R2=os.path.join(mask_folder,str(self.folder)+'_IAO_R2.tif')
            if os.path.isfile(IAO_R2):
                print(colored('#    IAO R2 found!!!','yellow'))
                self.IAO_R2=IAO_R2
            else:
                print(colored('#    IAO R2 missing!!!','red'))

        print(colored('--------------------------------------------------------------------------------------','green'))

class Sentinel2DataExtractor(object):
    def __init__(self, input_dir, output_dir):
        '''
        DataExtractor Class implements the functionality to discover data in 
        a directory and extract them to a target directory arranged by the tiles.
        '''
        self.input_dir = input_dir
        self.output_dir = os.path.join(output_dir,'Sentinel2Data')
        self.zones = []
        
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def __list_zones(self):
        for fname in glob(os.path.join(self.input_dir, '**/*.zip'), recursive=True):
            basename = os.path.basename(fname).replace('.zip', '')
            zone = basename.split('_')[3]
            self.zones.append(zone)

    def extract(self):
        self.__list_zones()
        for zone in self.zones:
            zone_dir = os.path.join(self.output_dir, zone)
            if not os.path.exists(zone_dir):
                os.mkdir(zone_dir)        
            for fname in glob(os.path.join(self.input_dir, '**/*.zip'), recursive=True):
                print(colored('#    Unzipping: {}'.format(fname),'yellow'))
                start_time = time.time()
                zfile = zipfile.ZipFile(file=fname)
                zfile.extractall(zone_dir)
                zfile.close()
                print('\t|- Extracted : {zone_name:s} - {file_name:s} in {te:s}'.format(zone_name=zone,file_name=os.path.basename(fname),te=str(time.time()-start_time)))

class Sentinel2DataPreprocessor(object):
    def __init__(self,cloud_mask_flag=True,no_data_flag=True,normalize_flag=True):
        self.cloud_mask_flag=cloud_mask_flag
        self.no_data_flag=no_data_flag
        self.normalize_flag=normalize_flag
        self.raster_num=None
        self.raster_count=None

    def __GetDecimalsWithEndBit(self,max_value):
        __results=[]
        
        for i in range(0,max_value+1):
        
            __BinaryString=format(i,'08b')
        
            if(__BinaryString[-1]=='1'):
        
                __results.append(i)
        
        return __results
    
    def __CloudMaskCorrection(self,mask):                                                                           
        
        __decimals=self.__GetDecimalsWithEndBit(np.nanmax(mask))
        
        for v in __decimals:
            self.data[mask==v]=-10000 # NaN values
         
        
    #Section- Preprocessing

    def __NanConversion(self):
        self.data = self.data.astype(np.float)
        self.data[self.data==-10000] = np.nan

    def __NormalizeData(self):
        self.data = (self.data-np.nanmin(self.data))/(np.nanmax(self.data)-np.nanmin(self.data))
        
    def preprocessData(self,cloud_mask_path,data_path,resolution=10,fromDataSetFlag=False):
        
        data_reader=TiffReader()
        
        if fromDataSetFlag:
            dataSet=data_reader.GetDataSet(data_path)
            self.data=data_reader.GetDataArray(data_path,raster_count=self.raster_count,raster_num=self.raster_num)
            dataSet=None
        else:
            self.data=data_reader.GetDataArray(data_path)

        if self.cloud_mask_flag:
            mask=data_reader.GetDataArray(cloud_mask_path)
            self.__CloudMaskCorrection(mask)
        
        if self.no_data_flag:
            self.__NanConversion()
        
        if self.normalize_flag:
            self.__NormalizeData()
        
        if resolution==20:
            self.data=np.array(self.data.repeat(2,axis=0).repeat(2,axis=1))
        
        return self.data
