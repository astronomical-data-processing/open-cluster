#!/usr/bin/env python

import os, sys
import numpy as np

from sklearn.neighbors import KDTree
from astropy import units as u
from astropy.coordinates import SkyCoord, Galactic

import pandas as pd


D2R         =   np.pi / 180.
n_star_min  =   10

nseg=200

b_link=[0.1,0.2,0.3]

prefix_sel  =   'src/step4'
prefix_sel_5data  =   'src/step2'

# Generate keys that store the individual index for each star. For single 
# sky area, the seg part can be ignored, which makes the function pretty 
# simple:
def load_stars_single(file_path):
    '''

    :param file_path: arr: store indiviual stellar info (l, b, plx, pmra, pmdec). (xxx.npy)
    :return:
    '''
    if file_path.endswith('.npy'):
        arr = np.load(file_path,allow_pickle=True)
    elif file_path.endswith('.csv'):
        arr=pd.read_csv(file_path,sep=',')
        arr=arr.to_numpy()
    keys = np.arange(len(arr))
    return arr, keys


def load_stars(id_task): # id_task 分区标识
    l_arr = []
    l_key = []
    for i in range(nseg):
        name_ids = '%s/stars_in_seg%04d.npy' % (prefix_sel, i)
        ids = np.load(name_ids,allow_pickle=True)[id_task]
        if len(ids) == 0:
            continue
        name_sel = '%s/sel%04d.npy' % (prefix_sel_5data, i)
        arr = np.load(name_sel)[ids]
        ns = len(arr)
        print('Partition %d, load seg %d, %d stars.' % (id_task, i, ns))
        l_arr.append(arr)
        key = (np.ones(len(ids), dtype='i8') << 32) * i
        key += ids
        l_key.append(key)

    return np.concatenate(l_arr, axis=0), np.concatenate(l_key, axis=0)


def norm(arr):

    v0  =   np.min(arr)
    v1  =   np.max(arr)


    return (arr - v0) / (v1 - v0)

class Group(object):

# You may use your own input array
    def __init__(self, arr, keys,b_link):

        self.nstar  =   len(arr)
        print ('stars: %d' % (self.nstar))
        self.l      =   arr[:, 0]
        self.b      =   arr[:, 1]
        self.plx    =   arr[:, 2]
        self.pmra   =   arr[:, 3]
        self.pmdec  =   arr[:, 4]
        self.arr    =   arr
        self.keys   =   keys
        self.b_link=b_link

        if np.max(self.l) - np.min(self.l) > 180.:
            ids =   np.where(self.l > 180.)[0]
            self.l[ids] -=  360.
    
        wra     =   np.cos(np.median(self.b) * D2R)
        self.w  =   np.array([wra, 1., 0.5, 1., 1.])
        self.w  /=  np.average(self.w)

#        

        self.b_fof   =   np.power(1.0 / self.nstar, 1. / 5.) * self.b_link
        print ('linking length: %f' % (self.b_fof))

        self.groups  =   []
        self.ngroup  =   0
        self.s2g     =   np.zeros(self.nstar, dtype = int) - 1
        self.nassigned  =   0

    def build_tree(self):

        x0  =   norm(self.l)[:, np.newaxis]
        x1  =   norm(self.b)[:, np.newaxis]
        x2  =   norm(self.plx)[:, np.newaxis]
        x3  =   norm(self.pmra)[:, np.newaxis]
        x4  =   norm(self.pmdec)[:, np.newaxis]

        self.X   =   np.concatenate((x0, x1, x2, x3, x4), axis = 1)
        self.X   *=  self.w

        tree    =   KDTree(self.X, leaf_size = 2)

        return tree

    def merge_group(self, gid0, gid1):
        for k in self.groups[gid1]:
            self.s2g[k]    =   gid0
        self.groups[gid0]   +=  self.groups[gid1]
        self.groups[gid1]   =   []

    def update_neighbor(self, gid0, ids):
        gid =   gid0
        for k in ids:
            if self.s2g[k]  < 0:
                self.s2g[k] = gid
                self.groups[gid].append(k)
                self.nassigned  +=  1
            elif self.s2g[k] != gid:
                gid1    =   self.s2g[k]
                if gid > gid1:
                    gid, gid1  =   gid1, gid
                self.merge_group(gid, gid1)

    def clear_group(self):

        while len(self.groups[-1]) == 0:
            del self.groups[-1]
            self.ngroup -=  1

        gid =   0
        while gid < self.ngroup - 1:
            if len(self.groups[gid]) == 0:
                self.merge_group(gid, self.ngroup - 1)
                while len(self.groups[-1]) == 0:
                    del self.groups[-1]
                    self.ngroup -=  1
            gid +=  1

    def fof(self):

        tree    =   self.build_tree()
        nloop   =   0
        while self.nassigned < self.nstar:
        
            for i in range(self.nstar):
                if self.s2g[i] > 0:
                    continue
                ids =   tree.query_radius([self.X[i]], r = self.b_fof)[0]
                gid =   -1
                for k in ids:
                    if self.s2g[k] >= 0:
                        gid =   self.s2g[i]
                        break
                if gid < 0:
                    self.groups.append([])
                    gid =   self.ngroup
                    self.ngroup +=  1
            
                self.update_neighbor(gid, ids)

            nloop   +=  1
            print ('loop %d: %d stars assigned, %d groups' % \
                (nloop, self.nassigned, self.ngroup))
        
        self.clear_group()
        print ('%d groups constructed.' % (self.ngroup))

        ginfo0  =   []
        lens    =   []
        l_key   =   []
        for grp in self.groups:
            if len(grp) < n_star_min:
                continue

            lens.append(len(grp))

            l       =   self.l[grp]
            b       =   self.b[grp]
            plx     =   self.plx[grp]
            pmra    =   self.pmra[grp]
            pmdec   =   self.pmdec[grp]
            l_key.append(self.keys[grp])

# 0 to 360 jump of l has been corrected.  
            l0      =   np.average(l)
            b0      =   np.average(b)
            pmra0   =   np.average(pmra)
            pmdec0  =   np.average(pmdec)
            plx0    =   np.average(plx)
            
            g0  =   Galactic(l = l0 * u.degree, b = b0 * u.degree)
            gs  =   Galactic(l = l * u.degree, b = b * u.degree)

            rs  =   g0.separation(gs).degree
            r_max   =   np.max(rs)
            
            dpm     =   np.sqrt((pmra - pmra0) ** 2 + (pmdec - pmdec0) ** 2)
            dpm_max =   np.max(dpm) 
            
            dplx_max=   np.max(np.abs(plx - plx0))
            
#          
            tpl =   [len(grp), l0, b0, r_max, pmra0, pmdec0, dpm_max, plx0, dplx_max]
            ginfo0.append(tpl)

        ids =   np.argsort(lens)[::-1]
        l_key1  =   []
        ginfos  =   []
        for id in ids:
            ginfos.append(ginfo0[id])
            l_key1.append(l_key[id])

        return ginfos, l_key1
 

def runfof(id_file,b_link):
    '''

    :param id_file:
    :return:
    ginfos_pXXXX.npy: 2D floating array. Each row is a list that gives the basic information of a star cluster identified in this partition.
    Meaning of each element in the list: cluster star number, l, b, r_max, pmra, pmdec, r_pm, parallax, r_parallax.
    keys_sel_pXXXX.npy: each row is a list that contains all keys for that cluster.
    '''
    

    # arr, keys =   load_stars(id_file)
    arr, keys = process_data(id_file)



    g   =   Group(arr, keys,b_link)
    print(np.mean(g.l))
    print(np.mean(g.b))
    ginfos, l_keys  =   g.fof()
    np.save('ginfos_m7_1.2.npy' , ginfos)
    np.save('keys_m67_1.2.npy'  , l_keys)
     

def process_data(file_path):
    data=pd.read_csv(file_path,sep=',')
    print(data.shape)
    # remove pmnan
    data=data.dropna(subset=['ra','dec','parallax','pmra','pmdec','phot_g_mean_mag','phot_bp_mean_mag','phot_rp_mean_mag'])
    # select by mag_g   parallax (0.2 mas - 7 mas)
    print(data.shape)
    data=data[(data['phot_g_mean_mag']<=18) & (data['parallax']<=7.0) & (data['parallax']>=0.2)]
    print(data.shape)
    # select by pm < 30 mas/yr
    data=data[(data['pmra'].abs()<30) & (data['pmdec'].abs()<30)]
    c = SkyCoord(ra=data['ra'] * u.degree, dec=data['dec'] * u.degree, frame='icrs')

    c_G = c.transform_to(Galactic)
    data['l'] = c_G.l.degree
    data['b'] = c_G.b.degree
    data=data[['l','b','parallax','pmra','pmdec','phot_g_mean_mag','phot_bp_mean_mag','phot_rp_mean_mag']]
    data.to_csv("m67.csv",index=True)
    arr = data.to_numpy()
    keys = np.arange(len(arr))
    return arr, keys
    # return data


if __name__ == '__main__':
    id_file='data/square_m67.csv'
    b_link = 1.2

    runfof(id_file,b_link)

