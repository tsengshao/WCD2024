dset test.nc
dtype netcdf
title cl31
options template
undef -9999.9
xdef 1 linear -179.95 0.1
ydef 1 linear -89.95 0.1
zdef 1500 linear 2.5 5 
tdef 4320  linear 00:00Z01JAN2001 1mn
vars 3
  backcoff=>z 1500 t,z z
  hcloud=>cbased 3 t,z height of cloud base (3 layers)
  status=>sta    0 t   detection status
endvars
