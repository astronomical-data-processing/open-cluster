import matplotlib
import pandas as pd
import numpy as np

from astropy.coordinates import SkyCoord
import os

matplotlib.use('agg')

import matplotlib.pyplot as plt

source_dir = '../output'
dist_dir = "./"
SMALL_SIZE = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 30
MARKERSIZE = 3
plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y label
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick label
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick label
plt.rc('legend', fontsize=18)
ms=5

if not (os.path.exists(dist_dir)):
    os.mkdir(dist_dir)


matched_info_file = "../cross_match_modual/cross_match/matched_CG2017.txt"
fit_dir = "../CMD_fitting_modual/cmd_all/"
matched = pd.read_table(matched_info_file, encoding='utf_8_sig', engine='python', header=None)
matched_id = matched.loc[0] # read first line
reference_id=matched.loc[1]
# print(matched_id[0])
# print(reference_id[0])
# matched_id[0][1:-2].split(',') 去掉两端的[]
# dict_matched={14090:'NGC_2682',3252:'NGC_188',14531:'NGC_1662',14529:'NGC_752',3250:'NGC_6254',3:'NGC_104',28:'NGC_6752',29:'NGC_6809',14677:'NGC_752'}
dict_matched=dict(zip(matched_id[0][1:-1].split(',') ,reference_id[0][1:-1].split(',')))
# print(dict_matched)
# breakpoint()
name = ['RAdeg', 'DEdeg', 'GaiaDR2', 'GLON', 'GLAT', 'Plx', 'e_Plx', 'pmRA*', 'e_pmRA*', 'pmDE', 'e_pmDE',
       'RADEcor', 'RAPlxcor', 'RApmRAcor', 'RApmDEcor', 'DEPlxcor', 'DEpmRAcor', 'DEpmDEcor', 'PlxpmRAcor',
       'PlxpmDEcor'
       'pmRApmDEcor', 'o_Gmag', 'Gmag', 'BP-RP', 'proba', 'Cluster', 'Teff50']
list_ = [i for i in range(11)]
CG20_meter= pd.read_csv('../cross_match_modual/catalog_public_ocs/CG20members.dat',delimiter="\s+",usecols=list_,names=['RAdeg', 'DEdeg', 'GaiaDR2', 'GLON', 'GLAT', 'Plx', 'e_Plx', 'pmRA*', 'e_pmRA*', 'pmDE', 'e_pmDE'])
# print("CG:", CG20_meter)
colspecs=[(442,452),(454,466),(467,474 ),(475,492)]
CG20_mag = pd.read_fwf('../cross_match_modual/catalog_public_ocs/CG20members.dat', colspecs=colspecs,names=['Gmag', 'BP-RP', 'proba', 'Cluster'] )
# print("CG:", CG20_mag)
CG20=pd.concat([CG20_meter,CG20_mag],axis=1,join='outer')
# CG20['Cluster']=CG20['Cluster'].to_string().strip()
print('cluster:',type(CG20.loc[5600,'Cluster']))

for root, subdir, files in os.walk(source_dir):
    for file in files:

            for key,value in dict_matched.items():


                    ref_data=CG20[CG20['Cluster']=='NGC_2682']
                    print(ref_data)
                    # breakpoint()

                    ref_data.to_csv("ngc2682.csv")
                    breakpoint()


