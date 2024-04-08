import os
import numpy as np
import datetime
import glob
import pandas as pd

path = os.getcwd()
file = glob.glob('*.DAT')

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

def hex2dec(string_num):
    return float(twos_comp(int(string_num.upper(), 16), 20))
       
for files in file:
    f = open(path+'\\'+files)    
    alldata = []
    tt = []
    ceildata = []
    all_logdata = []
        
    for i in range(2):
        heading = f.readline()
        print (heading)
        
    for j in range(43200): 
        data = []   
        f.read(1)
        t_tmp = f.read(19)
        if t_tmp[:11] == 'File Closed' :
            break
        t = datetime.datetime.strptime(t_tmp,'%Y-%m-%d %H:%M:%S')
        tt.append(t)
        for i in range(4):
            status = f.readline()
        for k in range(1500):
            data_tmp = f.read(5)           
            data_tmp = hex2dec(data_tmp)
            data.append(data_tmp)                              
        alldata.append(data)
        f.readline()
        total = f.readline()
        total = hex2dec(total[1:5])
        f.readline() 

    alldata = np.array(alldata)
    f.close()    

    ttt = []
    for i in range(np.shape(alldata)[0]):
        ttt.append(datetime.datetime.strftime(tt[i],'%H:%M:%S'))
    h = np.arange(5,7501,5)
    rrr = list(map(lambda x:"{}m".format(x),h))
    df = pd.DataFrame(alldata,index=ttt,columns=rrr)
    df.to_csv(files[:-4]+'.csv')


    # cm = plt.get_cmap('jet')
    # idx = [0, 3600, 7200, 10800, 14400]
    # x = np.arange(j)
    # hhh = np.arange(5,7501,5)
    # plt.figure(figsize=[9,5],dpi=300)
    # C=plt.pcolormesh(x,hhh,np.log10(np.transpose(alldata)),cmap=cm, vmin=2, vmax=6)
    # CB=plt.colorbar(C,extend='max')
    # plt.title('Ceilometer Backscatter Coefficient [10$^{-6}$ srad$^{-1}$ km$^{-1}$]',fontsize=14)
    # plt.xlim(x[0],x[-1])
    # plt.ylim(0,4000)
    # plt.xlabel('Time [hhmmss]',fontsize=12)
    # plt.ylabel('Height [m]',fontsize=12)
    # #plt.xticks(x[idx],np.array(ttt)[idx])
    # plt.savefig(files[:-4]+'.png',bbox_inches='tight')


                