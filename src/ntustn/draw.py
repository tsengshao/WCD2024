import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

datestr = '20240401'
datype  = 'MN'
fname  = f'../../data/NTUstn/{datype}_{datestr}.txt'
data = pd.read_csv(fname)
data['DTIME'] = pd.to_datetime(data.DTIME, format='%Y%m%d%H%M')

