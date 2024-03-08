DSET /data3/mog/taiwanvvm/%e/TOPO.nc 
DTYPE netcdf 
OPTIONS template 
TITLE TOPOGRAPHY 
UNDEF -99999. 
CACHESIZE 10000000 
XDEF 1024 LINEAR 118.63870 0.00465
YDEF 1024 LINEAR 21.21948 0.00465
ZDEF 1 LEVELS 0 
TDEF 1 LINEAR 00:00Z01JAN2000 1mn 
EDEF 30 NAMES
tpe20050712cln  tpe20070830cln  tpe20100629cln  tpe20110615cln  tpe20110816cln  tpe20130807cln
tpe20050723cln  tpe20080715cln  tpe20100630cln  tpe20110616cln  tpe20110821cln  tpe20130825cln
tpe20060508cln  tpe20090707cln  tpe20100802cln  tpe20110702cln  tpe20120715cln  tpe20140525cln
tpe20060718cln  tpe20090817cln  tpe20100803cln  tpe20110723cln  tpe20120819cln  tpe20140703cln
tpe20060721cln  tpe20090827cln  tpe20100912cln  tpe20110802cln  tpe20130723cln  tpe20140825cln
VARS 9 
TOPO=>topo 1 y,x topo 
albedo=>albedo 1 y,x topo 
GRF=>grf 1 y,x topo 
LAI=>lai 1 y,x topo 
LU=>lu 1 y,x topo 
SHDMAX=>shdmax 1 y,x topo 
SHDMIN=>shdmin 1 y,x topo 
SLOPE=>slope 1 y,x topo
SOIL=>soil 1 y,x topo 
ENDVARS
