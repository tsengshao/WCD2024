import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import sys, os, glob, io
import xarray as xr
from multiprocessing import Process, Pool

def parsival_bins():
  # volume-equivalent diameter [mm]
  diameter = np.array([\
            0.062,  0.187,  0.312,  0.437,  0.562,\
            0.687,  0.812,  0.937,  1.062,  1.187,\
            1.375,  1.625,  1.875,  2.125,  2.375,\
            2.750,  3.250,  3.750,  4.250,  4.750,\
            5.500,  6.500,  7.500,  8.500,  9.500,\
           11.000, 13.000, 15.000, 17.000, 19.000,\
           21.500, 24.000,\
           ])

  # particle speed [m/s]
  speed   = np.array([\
            0.050,  0.150,  0.250,  0.350,  0.450,\
            0.550,  0.650,  0.750,  0.850,  0.950,\
            1.100,  1.300,  1.500,  1.700,  1.900,\
            2.200,  2.600,  3.000,  3.400,  3.800,\
            4.400,  5.200,  6.000,  6.800,  7.600,\
            8.800, 10.400, 12.000, 13.600, 15.200,\
           17.600, 20.800,\
           ])
  return diameter, speed

def mergeDateTime(df):
  date = pd.to_datetime(df['date']+' '+df['time'], format="%d.%m.%Y %H:%M:%S")
  df['datetime']=date
  return df

def readParWCD(fname):
  columns=['ParNum', 'StnNum', 'date', 'time', \
           'Rain',   'RainAmount', 'Voltage', \
           'status', 'particle'] + \
          [f'num{i}' for i in range(1024)] + \
          ['StnName']
  df = pd.read_csv(fname, names=columns, on_bad_lines='skip')
  idx = df.isnull().sum(axis=1) < 5
  df = df[idx]
  df = mergeDateTime(df)
  return df

def readParWCDcr300(fname):
  #fname='/data2/C.shaoyu/WCD2024/raw/ParsivelWCD_cr300/parsivel31.csv'
  f=open(fname,'r')
  c = f.read().replace('"','').split('\n')[4:]
  instr = io.StringIO('\n'.join(c))
  df = pd.read_csv(instr, skiprows=[0,1,2,3]).iloc[:,3:]
  recols = ['StnNum', 'date', 'time', 'Rain', 'RainAmount',\
            'Voltage', 'status', 'particle', 'StnName'] +\
           [f'num{i}' for i in range(1024)]
  df.columns = recols
  idx = (df!='NAN').all(axis=1)
  df = df[idx]
  df = mergeDateTime(df)
  return df

def combineParWCD(yyyymmdd):
  fname = f'/data2/C.shaoyu/WCD2024/raw/ParsivelWCD/{yyyymmdd}.txt'
  cwcd = readParWCD(fname)
  fdir='/data2/C.shaoyu/WCD2024/raw/ParsivelWCD_cr300/'
  #flist = glob.glob(fdir+f'*{yyyymmdd[6:8]}*.*')
  flist = glob.glob(fdir+'*')
  #if(len(flist)>=1):
  if(cwcd.shape[0]<1440):
    print(flist)
    ccr300 = readParWCDcr300(flist[0])
    for i in range(1,len(flist)):
      print(flist[i])
      if('README.txt' in flist[i]): continue
      c = readParWCDcr300(flist[i])
      ccr300 = pd.concat((ccr300,c), ignore_index=True)
    cwcd = cwcd.merge(ccr300, sort='datetime', how='outer')
  return cwcd 
  

def readParNTU(fname):
  # the order must be increase
  coldicts = {
             'Rain'       :[1, float], \
             'RainAmount' :[2, float], \
             'Voltage'    :[17, float], \
             'status'     :[18, int], \
             'time'       :[20, str],\
             'date'       :[21, str], \
             'StnName'    :[22, str], \
             'particle'   :[60, int],\
            }

  f = open(fname, 'r')
  c = f.read().split('\n')
  lines = list(filter(None, c))
  f.close()

  cols = list(coldicts.keys())
  df = pd.DataFrame(columns=cols, index=[0])
  if (len(lines)==0):
    print('empty-file: ,',fname)
    return df

  line93 = -1
  ikey = 0
  keylist = list(coldicts.keys())
  for line in lines:
    idx = int(line[:2])
    dat = line[3:]
    if dat=='': dat='0'

    if (ikey < len(keylist)):
      key = keylist[ikey]
      value = coldicts[key]

    if idx==93:
      line93 = line
      ikey += 1
      continue
    if idx==value[0]:
      dat = value[1](dat)
      df[key] = dat
      #print(key, dat)
      ikey += 1
      continue

  line = line93
  if(type(line93)==type(3)): print(lines)
  idx = int(line[:2])
  dat = list(map(int,line[3:-1].split(';')))
  df2 = pd.DataFrame([dat], columns=[f'num{i}' for i in range(1024)], index=[0])
  df  = pd.concat((df, df2), axis=1)
  return df


def combineParNTU(yyyymmdd):
  ParID = '000PA3'
  fdir = '/data2/C.shaoyu/WCD2024/raw/ParsivelNTU/'
  flist = glob.glob(fdir + f'{yyyymmdd}/{ParID}-NTU_{yyyymmdd}_*.txt')

  pool = Pool()
  results = pool.map(readParNTU, flist)
  pool.close()
  pool.join()

  df = pd.concat(results, ignore_index=True, axis=0)
  df = mergeDateTime(df)
  df = df.sort_values('datetime')
  return df

def checkSTATUS(dfall):
  idx = dfall['status']>=2
  if (np.sum(idx)>0):
    print('!!! status=2 or 3, '+\
          'the data can not used in some timestep, '+\
          'please check the Parsival!!!')
  return dfall[~idx]

def process_data(yyyymmdd, dfall, resolution=1):
  # [input] yyyymmdd: str, 'yyyymmdd'
  # [input] dfall:   pandas.DataFrame, 
  #                  columns include [datetime, Rain, Voltage, status, particle, num0-1023]
  # [input] resolution: float, min, defalut: 1 minute

  dfall = checkSTATUS(dfall)

  tmpstr = yyyymmdd[:4]+'-'+yyyymmdd[4:6]+'-'+yyyymmdd[6:8]
  timebins = np.datetime64(tmpstr,'ms') + np.arange(24*60//resolution+1)*np.timedelta64(resolution, 'm')
  ntime = timebins.size
  tmin, tmax = timebins.min(), timebins.max()
  idx = (dfall['datetime']<=tmax)*(dfall['datetime']>=tmin)
  df  = dfall[idx]
  tcenter = timebins[:-1]+np.diff(timebins)/2-np.timedelta64(1,'s')
  print(tcenter)
  df['timeidx'] = np.argmin(np.abs(tcenter[:,np.newaxis] - df['datetime'].values), axis=0)
  print(df[['datetime', 'timeidx']])
  sumcols = ['particle'] + [f'num{i}' for i in range(1024)]
  avecols = ['Rain', 'Voltage', 'status']
  c = df.groupby('timeidx')[sumcols].sum().reset_index()
  d = df.groupby('timeidx')[avecols].mean().reset_index()

  merge = pd.DataFrame()
  merge['datetime'] = timebins[:-1]
  merge['timeidx']  = np.arange(tcenter.size)
  merge = merge.merge(d, on='timeidx',how='left').merge(c, on='timeidx',how='left')

  idx = np.nonzero(['num' in x for x in merge.columns])[0]
  dat1024 = merge.iloc[:,idx].apply(lambda x: np.array(list(x)), axis=1)

  outcols = ['datetime', 'Rain', 'Voltage', 'status', 'particle']
  merge = merge[outcols]
  merge['dat1024'] = dat1024
  return timebins, merge

if __name__=='__main__':
  yyyymmdd = '20240406'
  cwcd = combineParWCD(yyyymmdd)
  cntu =  combineParNTU(yyyymmdd)
  trange, df_wcd = process_data(yyyymmdd, cwcd)
  trange, df_ntu = process_data(yyyymmdd, cntu)

  



