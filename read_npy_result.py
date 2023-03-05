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
plt.rc('legend', fontsize=10)
data=np.load('ginfos_m7_1.2.npy',allow_pickle=True)
print(data.shape)
data_fof=np.load('keys_m67_1.2.npy',allow_pickle=True)
print(data_fof)
print('Found %d star clusters!'% len(data_fof))
# breakpoint()
#### get each group#######################
members=pd.read_csv('m67.csv') # stars 42568 after processing
print(members)
j = 1
dist_dir='m67_1.2/'
if not (os.path.exists(dist_dir)):
    os.mkdir(dist_dir)
for i in data_fof:

    print(i)
    group=members.loc[i]
    group.to_csv(dist_dir+str(j)+".csv")
    print(group)
    plt.suptitle("ID:%04d" % (j), fontsize=20)
    # plt.plot(source_data['ra'], source_data['dec'], ',',c='gray')
    # galactic_coord = SkyCoord(l=mem_data['ra'] * u.degree, b=mem_data['dec'] * u.degree, frame='galactic')  # for l ,b
    # print(galactic_coord.icrs)
    fig = plt.figure(figsize=(30, 6))
    ax1 = fig.add_subplot(1, 4, 1, facecolor="#f5f6f7")
    mem_data=group
    plt.plot(mem_data['l'], mem_data['b'], '.', c='blue')

    plt.xlabel(r'l (deg)', fontsize=BIGGER_SIZE)
    plt.ylabel(r'b (deg)', fontsize=BIGGER_SIZE)
    plt.xlim(mem_data['l'].min() - 3 * mem_data['l'].std(), mem_data['l'].max() + 3 * mem_data['l'].std())
    plt.ylim(mem_data['b'].min() - 3 * mem_data['b'].std(), mem_data['b'].max() + 3 * mem_data['b'].std())

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
    plt.plot(mem_data['pmra'], mem_data['pmdec'], '.', c='blue', markersize=5)

    plt.xlabel(r'$\mu_{\alpha*}$ (mas/yr)', fontsize=BIGGER_SIZE)
    plt.ylabel(r'$\mu_{\delta}$ (mas/yr)', fontsize=BIGGER_SIZE)

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
    plt.plot(mem_data['parallax'], mem_data['pmra'], '.', c='blue')

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
    plt.plot(mem_data['phot_bp_mean_mag'] - mem_data['phot_rp_mean_mag'], mem_data['phot_g_mean_mag'], '.', c='blue')
    ax = plt.gca()
    ax.invert_yaxis()
    # plt.xlim(-0.5, 4.)

    plt.xlabel('bp - rp', fontsize=BIGGER_SIZE)
    plt.ylabel('g', fontsize=BIGGER_SIZE)
    plt.ylim(mem_data['phot_g_mean_mag'].max() + 0.1, mem_data['phot_g_mean_mag'].min())

    # plt.savefig(dist_dir+"distribution"+file+".jpg")
    plt.savefig(dist_dir + str(j) + ".pdf", format='pdf', dpi=100, bbox_inches='tight')
    j+=1
    # plt.show()