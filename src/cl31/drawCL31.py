import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from netCDF4 import Dataset, num2date
import matplotlib.dates as mdates
import itertools


def readFile(fname):
  nc = Dataset(fname, 'r')
  hei = nc.variables['lev'][:].data
  nctime = nc.variables['time']
  tlist = nctime[:].data * np.timedelta64(1,'s') + \
          np.datetime64(nctime.units.split()[-1])
  data = nc.variables['backcoff'][:].data
  status = nc.variables['status'][:].data
  cbase  = nc.variables['hcloud'][:,:].data.astype(np.float32)

  # process cbase
  cbase[cbase<=0] = np.nan
  idx = status==4
  cbase[idx,:] = np.nan

  return tlist, hei, data, status, cbase

def plotData(tlist, hei, data, status, cbase, clname):
  date=tlist[0].astype(str).split('T')[0].replace('-','')
  cbase = cbase / 1000 #km
  hei   = hei / 1000 #km

  plt.rcParams.update({'font.size':15,
                       'axes.linewidth':2,})
  fig, ax = plt.subplots(figsize=(10,4.8))

  locator = mdates.AutoDateLocator()
  formatter = mdates.ConciseDateFormatter(locator,show_offset=False)
  ax.xaxis.set_major_locator(locator)
  ax.xaxis.set_major_formatter(formatter)

  CS = plt.pcolormesh(tlist, hei, \
                      np.log10(data.T.astype(np.float32)), \
                      vmin=2, vmax=6, cmap=plt.cm.ocean_r)
  cbr = plt.colorbar(CS)
  cbr.set_label('Ceilometer Backscatter Coefficient\n[10$^{-6}$ srad$^{-1}$ km$^{-1}$]', fontsize = 12)

  plt.scatter(tlist, cbase[:,0], s=0.3, fc='#FA8300', ec='none')
  plt.scatter(tlist, cbase[:,1], s=0.3, fc='#FA8300', ec='none')
  plt.scatter(tlist, cbase[:,2], s=0.3, fc='#FA8300', ec='none')

  idx = np.where(status==4)[0]
  if (len(idx)>0):
    plt.scatter(tlist[idx], np.ones(len(idx))*hei[10],\
                marker='x', s=10, fc='r', ec='none')

  plt.title(clname, weight = 'heavy', fontsize = 20, loc = 'left')
  plt.title(date, loc = 'right', fontsize = 15)
  plt.xlabel('LST')
  plt.ylabel('Height [km]')
  plt.xticks(fontsize=12)
  plt.ylim([0, 4])
  plt.tight_layout()
  plt.savefig(f'./fig/{clname}_%s.png'%date, dpi = 300)
  plt.close()
  return


if __name__=='__main__':
  clist = ['CLwcd', 'CLhydro']
  fdir = '/data/C.shaoyu/wcd2024/data/cl31/'
  yyyymmdd = '20240327'

  sdate = datetime(2024,4,1)
  edate = datetime(2024,4,1)
  nday  = int((edate-sdate).total_seconds()//86400+1)
  icl = 1
  for icl, idy in itertools.product([0,1], range(nday)):
    nowtime=sdate+timedelta(days=idy)
    yyyymmdd = nowtime.strftime('%Y%m%d')
    clname = clist[icl]
    print(clname, yyyymmdd)
    fname = f'{fdir}/{clname}_{yyyymmdd}.nc'
    tlist, hei, data, status, cbase = readFile(fname)
    plotData(tlist, hei, data, status, cbase, clname)


