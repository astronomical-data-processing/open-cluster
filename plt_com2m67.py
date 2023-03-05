import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 25
MARKERSIZE=3
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=16)

dist_dir='m67_comparison/'
if not (os.path.exists(dist_dir)):
    os.mkdir(dist_dir)
if __name__=="__main__":
    fig = plt.figure(figsize=(30, 6))
    ax1 = fig.add_subplot(1, 4, 1, facecolor="#f5f6f7")
    mem_data_1=pd.read_csv('m67_0.1/1.csv')
    mem_data_2 = pd.read_csv('m67_0.2/1.csv')
    mem_data_3 = pd.read_csv('m67_0.3/2.csv')
    CG20=pd.read_csv('ngc2682.csv',sep=',')
    mem_data=mem_data_1

    plt.plot(mem_data_1['l'], mem_data_1['b'], '.', c='blue',label='$b_{FoF}$=0.1')
    plt.plot(mem_data_2['l'], mem_data_2['b'], 'o', c='orange',label='$b_{FoF}$=0.2')
    plt.plot(mem_data_3['l'], mem_data_3['b'], '.', c='green',alpha=0.5,label='$b_{FoF}$=0.3')
    plt.plot(CG20['GLON'], CG20['GLAT'], '.', c='red',alpha=0.5,label='CG20')

    plt.xlabel(r'l (deg)', fontsize=BIGGER_SIZE)
    plt.ylabel(r'b (deg)', fontsize=BIGGER_SIZE)
    plt.xlim(mem_data_1['l'].min() - 3 * mem_data_1['l'].std(), mem_data['l'].max() + 3 * mem_data['l'].std())
    plt.ylim(mem_data_1['b'].min() - 3 * mem_data_1['b'].std(), mem_data['b'].max() + 3 * mem_data['b'].std())
    plt.legend()
    # plt.savefig(dist_dir+"Spatial_Distribution"+file+".png")
    # plt.savefig(dist_dir+"position"+file+".eps",format='eps',dpi = 100,bbox_inches = 'tight')

    '''
    2:plt VPD
    '''
    # fig = plt.figure(figsize=(6, 6))
    ax2 = fig.add_subplot(1, 4, 2, facecolor="#f5f6f7")
    # plt.plot(source_data['pmra'], source_data['pmdec'], ',',c='gray')
    plt.xlim(mem_data['pmra'].min() - 3 * mem_data['pmra'].std(), mem_data['pmra'].max() + 3 * mem_data['pmra'].std())
    plt.ylim(mem_data['pmdec'].min() - 3 * mem_data['pmdec'].std(),
             mem_data['pmdec'].max() + 3 * mem_data['pmdec'].std())
    plt.plot(mem_data_1['pmra'], mem_data_1['pmdec'], '.', c='blue', markersize=5,label='$b_{FoF}$=0.1')
    plt.plot(mem_data_2['pmra'], mem_data_2['pmdec'], 'o', c='orange',alpha=0.5,markersize=5,label='$b_{FoF}$=0.2')
    plt.plot(mem_data_3['pmra'], mem_data_3['pmdec'], '.', c='green',markersize=5,label='$b_{FoF}$=0.3')
    plt.plot(CG20['pmRA'], CG20['pmDE'], '.', c='red',alpha=0.5,markersize=5,label='CG20')

    plt.xlabel(r'$\mu_{\alpha*}$ (mas/yr)', fontsize=BIGGER_SIZE)
    plt.ylabel(r'$\mu_{\delta}$ (mas/yr)', fontsize=BIGGER_SIZE)
    plt.legend()
    # plt.xlim(-5,5)
    # plt.ylim(-5,5)

    # plt.savefig(dist_dir+"Vector_Point_Diagram"+file+".png")
    # plt.savefig(dist_dir+"Vector_Point_Diagram"+file+".eps",format='eps',dpi = 100,bbox_inches = 'tight')
    '''
    3:plt pmdec---parallax
    '''
    # fig = plt.figure(figsize=(6, 6))
    ax3 = fig.add_subplot(1, 4, 3, facecolor="#f5f6f7")
    # plt.plot(source_data['parallax'],source_data['pmra'],  ',', c='gray')
    plt.xlim(mem_data['parallax'].min() - 3 * mem_data['parallax'].std(),
             mem_data['parallax'].max() + 3 * mem_data['parallax'].std())
    plt.ylim(mem_data['pmra'].min() - 3 * mem_data['pmra'].std(),
             mem_data['pmra'].max() + 3 * mem_data['pmra'].std())
    plt.plot(mem_data_1['parallax'], mem_data_1['pmra'], '.', c='blue',label='$b_{FoF}$=0.1')
    plt.plot(mem_data_2['parallax'], mem_data_2['pmra'], 'o', c='orange',label='$b_{FoF}$=0.2')
    plt.plot(mem_data_3['parallax'], mem_data_3['pmra'], '.', c='green',alpha=0.5,label='$b_{FoF}$=0.3')
    plt.plot(CG20['Plx'], CG20['pmRA'], '.', c='red',alpha=0.5,label='CG20')

    plt.legend()
    plt.xlabel(r'$\varpi$ (mas/yr)', fontsize=BIGGER_SIZE)
    plt.ylabel(r'$\mu_{\delta*}$ (mas/yr)', fontsize=BIGGER_SIZE)

    # plt.xlim(0, 0.6)
    # plt.ylim(-5, 5)

    # plt.savefig(dist_dir+"distribution"+file+".png")
    # plt.savefig(dist_dir+"distribution" + file + ".eps", format='eps', dpi=100, bbox_inches='tight')
    '''
    4:plt CMD
    '''
    # fig = plt.figure(figsize=(6, 6))
    ax4 = fig.add_subplot(1, 4, 4, facecolor="#f5f6f7")
    # plt.plot(source_data['phot_bp_mean_mag']-source_data['phot_rp_mean_mag'], source_data['phot_g_mean_mag'], ',',c='gray')
    plt.plot(mem_data_1['phot_bp_mean_mag'] - mem_data_1['phot_rp_mean_mag'], mem_data_1['phot_g_mean_mag'], '.', c='blue',label='$b_{FoF}$=0.1')
    plt.plot(mem_data_2['phot_bp_mean_mag'] - mem_data_2['phot_rp_mean_mag'], mem_data_2['phot_g_mean_mag'], 'o', c='orange',label='$b_{FoF}$=0.2')
    plt.plot(mem_data_3['phot_bp_mean_mag'] - mem_data_3['phot_rp_mean_mag'], mem_data_3['phot_g_mean_mag'], '.', c='green',alpha=0.5,label='$b_{FoF}$=0.3')
    plt.plot(CG20['BP-RP'] , CG20['Gmag'], '.', c='red',alpha=0.5,label='CG20')



    ax = plt.gca()
    ax.invert_yaxis()
    # plt.xlim(-0.5, 4.)

    plt.xlabel('BP - RP', fontsize=BIGGER_SIZE)
    plt.ylabel('G', fontsize=BIGGER_SIZE)
    plt.ylim(mem_data['phot_g_mean_mag'].max() + 0.1, mem_data['phot_g_mean_mag'].min())

    # plt.savefig(dist_dir+"distribution"+file+".jpg")
    plt.legend()
    plt.savefig('com_m67'+ ".pdf", format='pdf', dpi=100, bbox_inches='tight')

    # plt.show()