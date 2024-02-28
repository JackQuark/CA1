# ==================================================
import numpy              as np
import matplotlib.pyplot  as plt
import netCDF4            as nc
import function           as func
from matplotlib.ticker    import FuncFormatter       as ffmt
# ==================================================

rootgrp = nc.Dataset('CA1.nc')

time = rootgrp.variables['time'][...]
m_zc = rootgrp.variables['m_zc'][...]
p_zc = rootgrp.variables['p_zc'][...]
TOPO = rootgrp.variables['topo'][0]
Th   = rootgrp.variables['th'  ][...]

T    = np.array([func.th_2_T(th, p_zc) for th in Th]) # th to T
anoT = np.transpose([T[i,:] - np.mean(T[1:144], axis=0) for i in range(145)])

# ==================================================  

f,ax = plt.subplots(1, 2, figsize=(10,6), sharex = 'row')

A    = np.linspace(-2, 2, 20)
CS1  = ax[0].contourf(time, m_zc[TOPO:], anoT[TOPO:,:], levels = A, 
                      cmap = plt.cm.seismic, extend='both')
CS2  = ax[1].contourf(time, p_zc[TOPO:], anoT[TOPO:,:], levels = A, 
                      cmap = plt.cm.seismic, extend='both')

def custom_format(value, _):
    return f'{value:.1f}'

ax[0].set_xlabel('Time [hr]')
ax[0].set_ylabel('Height [m]')
ax[0].set_yticks(np.append(ax[0].get_yticks(), m_zc[TOPO]))
ax[0].set_ylim([m_zc[TOPO], m_zc[-1]])

ax[1].set_xlabel('Time [hr]')
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position("right")
ax[1].set_ylabel('Pressure [hPa]', rotation=-90, labelpad = 16)
ax[1].set_yticks(np.append(ax[1].get_yticks(), p_zc[TOPO]))
ax[1].yaxis.set_major_formatter(ffmt(custom_format))
ax[1].set_ylim([p_zc[TOPO], p_zc[-1]])

cbar = plt.colorbar(CS1, ax=ax, orientation='horizontal', shrink=0.6, aspect=20,
                    ticks = (np.linspace(-2, 2, 11)), pad=0.125, 
                    label = 'Anomaly [K]')

plt.xticks(time[::24], labels=np.linspace(0, 24, 7))
f  .suptitle('TaiwanVVM simulation, tpe20110802cln\n00:00~24:00 @(120.32586. 23.96824)', 
             fontsize=14, y=0.96)

# ==================================================  

plt.savefig('CA1-1', dpi = 500)
plt.show()
