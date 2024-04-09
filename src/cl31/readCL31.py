import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import sys, os, glob
import xarray as xr

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

def hex2dec(string_num):
    return float(twos_comp(int(string_num.upper(), 16), 20))

def decoader(fname):
    f = open(fname, 'r', encoding='big5')

    timelist = []
    detstatus   = []
    alldata  = []
        
    for i in range(2):
        heading = f.readline()
        #print(heading)
        
    while True:
        # read timestep or newline
        f.read(1)
        t_tmp = f.read(19)
        f.read(1) #read newline char
        if t_tmp[:11] == 'File Closed' or t_tmp=='':
            break

        t = datetime.strptime(t_tmp,'%Y-%m-%d %H:%M:%S')
        timelist.append(t)

        # 1ST LINE, ^ACL020213^B
        line = f.readline()
        sky_condi = True if line[7]=='2' else False
        if line[8]=='3':
            nz=1500
            dz=5 #meter
        elif line[8]=='2':
            nz=385
            dz=20 #meter
        else:
            sys.exit('please check the resolution options of this data')
       
        #2ND LINE
        status = f.readline().split()
        line = [status[0][0].replace('/','-999'), \
                status[1].replace('/','0'), \
                status[2].replace('/','0'), \
                status[3].replace('/','0'), \
               ]
        line = list(map(int, line))
        detstatus.append(line)

        # 3RD LINE
        if sky_condi: f.readline()
        f.readline()

        # 4TH LINE, data
        data_profile = []
        for k in range(nz):
            data_tmp = f.read(5)   
            data_tmp = hex2dec(data_tmp)
            data_profile.append(data_tmp)
        alldata.append(data_profile)
        f.readline()

        # 5TH LINE, last
        line = f.readline()
        line = hex2dec(line[1:5])
        
        # newline
        f.readline() 
    f.close()

    alldata = np.array(alldata)
    height  = np.arange(nz)*dz
    detstatus = np.array(detstatus)
    return pd.to_datetime(timelist), height, detstatus, alldata

def toNC(ofname, tlist, lev, data, cldhei):
   ds = xr.Dataset()
   ds['backcoff'] = xr.DataArray(data, name='backcoff', dims=['time','lev'], attrs={'units':'1e-6 srad^-1 km^-1'})
   ds['hcloud']   = xr.DataArray(cldhei[:,1:], name='hcloud', dims=['time','layer'], attrs={'units':'meter'})
   ds['status']   = xr.DataArray(cldhei[:,0],  name='status', dims=['time'], attrs={'long_name':'detection status'})
   ds = ds.assign_coords({
                    'time':(['time'], tlist, {'standard_name': 'time', 'axis': 'T'}),\
                    'lev':(['lev'], lev, {'axis': 'Z'}),\
                    'layer':(['layer'],[1,2,3]),
                    }
        )
   ds.to_netcdf(ofname, \
                encoding={'time':{'units': "seconds since 2024-01-01 00:00:00"},\
                          'backcoff':{'chunksizes': (1,lev.size)}}, \
                unlimited_dims=['time'],)
   return

def mergedata(flist):
    tlist = []
    status = []
    data = []
    for fname in flist:
        print('read ... ',fname)
        result = decoader(fname)
        tlist.append(result[0])
        height = result[1]
        status.append(result[2])
        data.append(result[3])
    tlist  = np.concatenate(tlist)
    status = np.concatenate(status)
    data   = np.concatenate(data)
    return tlist, height, status, data
        

if __name__=='__main__':
    fdir='/data2/C.shaoyu/WCD2024/raw/'
    fdirout = '/data2/C.shaoyu/WCD2024/data/cl31/'
    os.system('mkdir -p '+fdirout)
    dirlist = ['CLwcd', 'CLhydro']
    sdate = datetime(2024,3,31)
    edate = datetime(2024,4,1)
    nday  = int((edate-sdate).total_seconds()//86400+1)
    for idir in [0, 1]: 
      clname=dirlist[idir]
      for idy in range(nday):
        nowdate = sdate+timedelta(days=idy)
        print(nowdate)
        mmdd = nowdate.strftime('%m%d')
        print(fdir+clname+'/A4'+mmdd+'*')
        flist = np.sort(glob.glob(fdir+clname+'/A4'+mmdd+'*'))
        result = mergedata(flist)
        toNC(f'{fdirout}/{clname}_2024{mmdd}.nc',\
             tlist=pd.to_datetime(result[0]), lev=result[1], data=result[3], cldhei=result[2])
