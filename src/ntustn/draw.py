import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def get_hr(xtime, data):
  xtime_hr = []
  out_hr   = []
  for i in range(xtime.size):
    if xtime[i].strftime('%M')=='00':
      xtime_hr.append(xtime[i])
      out_hr.append(data[i])
  return np.array(xtime_hr), np.array(out_hr)

datestr = '20240401'
datype  = 'MN'
fname  = f'../../data/NTUstn/{datype}_{datestr}.txt'
data = pd.read_csv(fname)
data['DTIME'] = pd.to_datetime(data.DTIME, format='%Y%m%d%H%M')

xtime = data.DTIME

plt.rcParams.update({'font.size':15,
                     'axes.linewidth':2,
                     'lines.linewidth':2})
fig, ax = plt.subplots(3, 1, figsize=(12,8), sharex=True)

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator,show_offset=False)
for axi in ax:
  axi.xaxis.set_major_locator(locator)
  axi.xaxis.set_major_formatter(formatter)


plt.sca(ax[0])
plt.plot(xtime, data.surP)
plt.title('Surface Pressure [hPa]', loc='left', weight='bold')
plt.title(datestr, loc='right', weight='bold')
plt.ylim(1005, 1015)
plt.grid(True)

plt.sca(ax[1])
plt.plot(xtime, data['T'], label='T')
plt.plot(xtime, data.Td, label='Td')
plt.legend()
plt.title('Temperature [K]', loc='left', weight='bold')
plt.ylim(15, 30)
plt.grid(True)

plt.sca(ax[2])
x_hr, rain_hr = get_hr(xtime, data['rain_hr'])
x_hr -= timedelta(minutes=30)
plt.bar(x_hr, rain_hr, width=np.diff(x_hr)[0])
plt.title('rain [mm]', loc='left', weight='bold')
plt.ylim(0, 30)
plt.grid(True)
plt.xlim(xtime.min(), xtime.max())

ax2 = plt.twinx(ax[2])
plt.plot(xtime, data.RH, c='k')
plt.ylim(40, 100)
plt.title('RH [%]', loc='right', weight='bold')

plt.suptitle('NTU observation', fontsize=15)
plt.savefig(f'./fig/ntustn_{datestr}.png', dpi=200)


