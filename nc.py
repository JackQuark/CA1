# abcdefghijklmnopqrstuvwxyz
import numpy              as np
import netCDF4            as nc
from   concurrent.futures import ProcessPoolExecutor

rootgrp = nc.Dataset("/home/B12/b12209017/CA1/tpe20110802cln/TOPO.nc")
TOPO = rootgrp.variables['TOPO'][...]
lat  = rootgrp.variables['lat' ][...]
lon  = rootgrp.variables['lon' ][...]
rootgrp.close()

location = [120.32586,23.96824] # [lon, lat]
y    = np.abs(lat - location[1]).argmin()
x    = np.abs(lon - location[0]).argmin()

def process_file(i):
    file_path = "/home/B12/b12209017/CA1/tpe20110802cln/archive/tpe20110802cln.L.Thermodynamic-000%03d.nc" % i
    rootgrp = nc.Dataset(file_path)
    return rootgrp.variables['th'][0,:,y,x]
    
with ProcessPoolExecutor() as executor:
    Th = np.array(list(executor.map(process_file, range(145))))

fw = nc.Dataset('CA1.nc', 'w', format = 'NETCDF4')

fw . createDimension('time', 145)
fw . createDimension('lev' , 70 )
fw . createDimension('TOPO', 1  )

fw . createVariable('time', np.int32  , ('time'))
fw . createVariable('m_zc', np.float32, ('lev' ))
fw . createVariable('p_zc', np.float32, ('lev' ))
fw . createVariable('th'  , np.float32, ('time', 'lev'))
fw . createVariable('topo', np.int32  , ('TOPO'))

rootgrp = nc.Dataset("/home/B12/b12209017/CA1/tpe20110802cln/archive/tpe20110802cln.L.Thermodynamic-000000.nc")

fw . variables['time'][:] = np.linspace(0,144,145)
fw . variables['m_zc'][:] = rootgrp.variables['zc'][...]
fw . variables['p_zc'][:] = np.loadtxt('/home/B12/b12209017/CA1/tpe20110802cln/pressure.txt', skiprows=3, unpack=True, usecols=1) / 100
fw . variables['th'  ][:] = Th
fw . variables['topo'][:] = TOPO[y,x]

rootgrp.close()
fw.close()