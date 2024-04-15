import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve
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

  idx = np.where(status==4)[0]
  if (len(idx)>0):
    plt.scatter(tlist[idx], np.ones(len(idx))*hei[5],\
                marker='X', s=3, fc='r', ec='none')
    cbase[idx,:] = np.nan

  plt.scatter(tlist, cbase[:,0], s=0.3, fc='#FA8300', ec='none')
  plt.scatter(tlist, cbase[:,1], s=0.3, fc='#FA8300', ec='none')
  plt.scatter(tlist, cbase[:,2], s=0.3, fc='#FA8300', ec='none')

  plt.title(clname, weight = 'heavy', fontsize = 20, loc = 'left')
  plt.title(date, loc = 'right', fontsize = 15)
  plt.xlabel('LST')
  plt.ylabel('Height [km]')
  plt.xticks(fontsize=12)
  plt.ylim([0, 4])
  plt.tight_layout()
  return fig, ax

def target_function(Tc, T0_K, e0_Pa):
    return Tc-5420/np.log(2.53e11/e0_Pa*(T0_K/Tc)**0.286)
def target_function_qv(Tc, T0_K, p0_Pa, qv0_kgkg):
    return Tc-5420/np.log(2.53e11*0.622/p0_Pa/qv0_kgkg*(T0_K/Tc)**0.286)
def cal_lcl_pres(Tc, P0, T0):
    return P0*(Tc/T0)**(1/0.286)
def cal_hypsomec_hei(z0, Tv_bar, P1, P0):
    return z0+287*Tv_bar/9.8*np.log(P0/P1)
def cal_qv_from_e(e_pa, p_pa):
    return 0.622*e_pa/p_pa
def cal_es_from_t(t_K):
    return 2.53e11*np.exp(-5420/t_K)

def read_obs(fname):
  data = pd.read_csv(fname)
  data['DTIME'] = pd.to_datetime(data.DTIME, format='%Y%m%d%H%M')
  xtime = data['DTIME']
  Ti = data['T'].values+273.15    #[K]
  Td = data['Td'].values+273.15    #[K]
  Pi = data['surP'].values*100    #[Pa]
  ei = data['e'].values*100       #[Pa]
  es = data['es'].values*100       #[Pa]
  rh = data['RH'].values
  return xtime, Ti, Pi, ei, rh, Td, es

def calculate_cloud_base(Ti, Pi, ei):
  qv = cal_qv_from_e(ei, Pi)
  Tc = np.zeros(Ti.shape)*np.nan
  for it in range(Ti.size):
    #Tc[it] = fsolve(target_function, Ti[it], args=(Ti[it], ei[it]))
    Tc[it] = fsolve(target_function_qv, Ti[it], args=(Ti[it], Pi[it], qv[it]))
  lcl_pres = cal_lcl_pres(Tc, Pi, Ti)
  print('lcl_pres: ', lcl_pres.min(), lcl_pres.max())
  lcl_hei  = cal_hypsomec_hei(0, Ti, lcl_pres, Pi)
  print('lcl_hei: ', lcl_hei.min(), lcl_hei.max())
  return Tc, lcl_hei, lcl_pres

if __name__=='__main__':
  yyyymmdd = '20240401'
  print(yyyymmdd)
  data_path = '/data2/C.shaoyu/WCD2024/data/'

  clname='CLwcd'
  fname = f'{data_path}/cl31/{clname}_{yyyymmdd}.nc'
  tlist, hei, data, status, cbase = readFile(fname)

  fname  = f'{data_path}/NTUstn/MN_{yyyymmdd}.txt'
  xtime, ti, pi, ei, rh, Td, es = read_obs(fname)
  Tc, lcl_hei, lcl_pres = calculate_cloud_base(ti, pi, ei)

  fig, ax = plotData(tlist, hei, data, status, cbase, clname)
  plt.scatter(xtime, lcl_hei/1000, marker='.', s=10, fc='magenta', ec='none')

  plt.savefig(f'./fig/{yyyymmdd}.png', dpi = 300)
  plt.close()


