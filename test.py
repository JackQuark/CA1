# abcdefghijklmnopqrstuvwxyz
import numpy              as np
import netCDF4            as nc

rootgrp = nc.Dataset("/home/B12/b12209017/CA1/tpe20110802cln/TOPO.nc")
TOPO = rootgrp.variables['TOPO'][...]
lat  = rootgrp.variables['lat' ][...]
lon  = rootgrp.variables['lon' ][...]
rootgrp.close()

num = 1
rootgrp = nc.Dataset("/home/B12/b12209017/CA1/tpe20110802cln/archive/tpe20110802cln.L.Thermodynamic-000%03d.nc" %(num))
qv = rootgrp.variables['qv'][0,...]
qv = np.where(qv != 0, qv, np.nan)
rootgrp.close()

E, N = np.loadtxt("/home/B12/b12209017/CA1/B12.csv", unpack=True, delimiter=',')

q_index = np.zeros((45))
topo    = np.zeros((45))

def find(arr):

    mask = ~np.isnan(arr)
    
    if np.any(mask):
        return np.argmax(mask)
    else:
        return None

for i in range(45):

    loc = [E[i], N[i]] # [lon, lat]
    y   = np.abs(lat - loc[1]).argmin()
    x   = np.abs(lon - loc[0]).argmin()
    
    q_index[i] = find(qv[:,y,x])
    topo[i]    = TOPO[y,x]
    
result = np.vstack((E, N, q_index, topo)).T
np.savetxt('output%06d.csv' %(num), result, fmt='%9.5f, %9.5f, %3d, %3d', delimiter=',', 
            header='lon, lat, qv_find, TOPO')