import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys, os, io
from io import StringIO

def my_to_datetime(date_str):
    if date_str[8:10] != '24':
        return pd.to_datetime(date_str, format='%Y%m%d%H%M')

    date_str = date_str[0:8] + '00' + date_str[10:]
    return pd.to_datetime(date_str, format='%Y%m%d%H%M') + \
           timedelta(days=1)

def dstr2dstr(dstr):
    return my_to_datetime(dstr).strftime('%Y%m%d%H%M')

def getcolumn(datype):
  if datype=='MN':
    cols={1:'STATIONID',\
          2:'DKIND',\
          3:'DTIME',\
          4:'surP',\
          5:'slP',\
          6:'T',\
          7:'Td',\
          8:'RH',\
          9:'e',\
          10:'es',\
          11:'WD_10min',\
          12:'WS_10min',\
          15:'rain_min',\
          16:'rain_hr',\
          50:'solar_min',\
          51:'solar_hr',\
          }
  else:
    sys.exit('please add column and its index for new data type')
  return cols.keys(), cols.values()

def readdata(fname, datype):
  f = open(fname, 'r')
  csvstr = ''
  while True:
    line = f.readline()
    if len(line)==0: break
    if f',{datype},' in line:
      csvstr+=line
  csvstr = io.StringIO(csvstr)
  cols, columns = getcolumn(datype)
  output = pd.read_csv(csvstr, sep=',', usecols=cols, names=columns)
  output['DTIME'] = output.DTIME.astype(str).apply(dstr2dstr)
  return output

if __name__=='__main__':
  datestr = '20240331'
  datype  = 'MN'
  fname = f'../../raw/NTUstn/{datestr}.txt'
  data = readdata(fname, datype)
  fout  = f'../../data/NTUstn/{datype}_{datestr}.txt'
  print(fout)
  data.to_csv(fout, index=False)

