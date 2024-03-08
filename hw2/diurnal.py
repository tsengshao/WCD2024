import numpy as np
import sys, os
sys.path.insert(1,'../')
import config
from util.vvmLoader import VVMLoader, VVMGeoLoader
import util.calculator as calc
import util.tools as tools
from util.dataWriter import DataWriter
from mpi4py import MPI
from datetime import datetime, timedelta
#import numba
from netCDF4 import Dataset
import glob

comm = MPI.COMM_WORLD
nproc = comm.Get_size()
cpuid = comm.Get_rank()
outdir=config.dataPath+"/distance/"+exp+'/'

nexp = len(config.expList)
iexp = 0
exp = config.expList[iexp]

# read VVM coordinate
vvmLoader = VVMLoader(f"{config.vvmPath}/{exp}/", subName='exp')
thData = vvmLoader.loadThermoDynamic(0)
nz, ny, nc = thData['qv'][0].shape
xc, yc, zc = thData['xc'][:], thData['yc'][:], thData['zc'][:]
rho = vvmLoader.loadRHO()[:-1]
pibar = vvmLoader.loadPIBAR()[:-1]

nt = (glob.glob((f"{config.vvmPath}/{exp}/archive/*L.Thermodynamic*.nc")))
sssssssssssssf
# mpi for time
idxTS, idxTE = tools.get_mpi_time_span(0, nt, cpuid, nproc)
print(cpuid, idxTS, idxTE, idxTE-idxTS)

