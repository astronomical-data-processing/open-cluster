import os
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import Galactic
from astropy.coordinates import SkyCoord
def gen_ginfo(arr):
    arr=arr.dropna(subset=['ra','dec'])
    ra = arr['ra']
    dec = arr['dec']
    plx = arr['parallax']
    pmra = arr['pmra']
    pmdec = arr['pmdec']

    # correct for 0 ~ 360 jump
    if np.max(ra) - np.min(ra) > 180.:
        ids = np.where(ra > 180.)[0]
        ra[ids] -= 360.
    # print(arr.describe())

    c_sigma = SkyCoord(ra=ra.values* u.degree, dec=dec.values * u.degree, frame='icrs')
    l_arr = c_sigma.galactic.l.degree
    b_arr = c_sigma.galactic.b.degree

    ra0 = np.average(ra)
    ra_sigma=np.var(ra)
    dec0 = np.average(dec)
    dec_sigma=np.var(dec)
    pmra0 = np.average(pmra)
    pmra_sigma= np.var(pmra)
    pmdec0 = np.average(pmdec)
    pmdec_sigma=np.var(pmdec)
    plx0 = np.average(plx)
    plx_sigma=np.var(plx)

    # # icrs ---> galactic

    l0=np.average(l_arr)
    l_sigma=np.var(l_arr)
    b0 =np.average(b_arr)
    b_sigma=np.var(b_arr)

    #
    # g0 = Galactic(l=l0* u.degree, b=b0 * u.degree)
    #
    # c = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='icrs')
    # d = c.galactic
    # l, b = d.l, d.b
    #
    # gs = Galactic(l=l * u.degree, b=b * u.degree)
    #
    # rs = g0.separation(gs).degree
    # r_max = np.max(rs) # radius max
    # r_avg =  np.mean(rs) # radius avg
    #
    # dpm = np.sqrt((pmra - pmra0) ** 2 + (pmdec - pmdec0) ** 2)
    # dpm_max = np.max(dpm)
    #
    # dplx_max = np.max(np.abs(plx - plx0))

    tpl = [len(arr), ra0,ra_sigma,dec0,dec_sigma,plx0,plx_sigma,pmra0,pmra_sigma,pmdec0,pmdec_sigma,l0,l_sigma,b0,b_sigma]
    return tpl
if __name__=="__main__":
    base_dir= "2stata/"
    dist_dir='.'
    if not(os.path.exists(dist_dir)):
        os.mkdir(dist_dir)
    sc_info=[]
    for root, sub_dir, file in os.walk(base_dir):
        for name in file:
            file_dir=os.path.join(root,name)
            data_origin = pd.DataFrame()
            if name.endswith('.npy'):
                data_np = np.load(file_dir, allow_pickle=True)
                data_origin = pd.DataFrame(data_np)
                print(data_origin.shape)
                # 0.14
            elif name.endswith('.csv'):
                data_origin = pd.read_csv(file_dir,sep=,')

            data=data_origin
            if len(data)==0:
                print('Name is null')
                continue
            # print(data.columns)
            # r = data[data['probs_final'] > 0.5]
            # print(r)

            id_sc = name.split('c')[1][0:-1]
            print(id_sc)
            # breakpoint()
            d=gen_ginfo(data)


            # print(name_list)

            print(d)
            r=np.append((id_sc),d)
            # print(r)

            sc_info.append(r)
    sc_info=np.array(sc_info).astype(float)
    # print(sc_info)
    # print(sc_info.shape)

    # np.savetxt(dist_dir+'stat_info_1000'+".dat",sc_info,fmt='%05d , %d, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %.4f')
    name=['ID','len', 'ra','ra_sigma', 'dec','dec_sigma','plx','plx_sigma','pmra','pmra_sigma','pmdec','pmdec_sigma','l','l_sigma','b','b_sigma']

    r=pd.DataFrame(sc_info,columns=name)
    r = r.round(4)
    r['ID']=r['ID'].apply(lambda x : '{:0>5d}'.format(int(x)))
    r['len'] = r['len'].apply(lambda x: int(x))
    r.to_csv(dist_dir+'stat_m67'+".dat",sep=',',index=False)


