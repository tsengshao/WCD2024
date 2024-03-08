'reinit'
'set background 1'
'c'

'sdfopen mean_preci.nc'
'sdfopen freq_24mmd.nc'
'open ../gs_ctl_tpe/topo.ctl'

'set xlopts 1 5 0.2'
'set ylopts 1 5 0.2'
'set xlint 1'
'set ylint 1'
'set grads off'
'set timelab off'
'set mpdraw off'

*south western
'set lon 119.5 121.5'
'set lat 22.5 24.5'

*chiayi
'set xlint 0.5'
'set ylint 0.5'
'set parea 1 10 1 7.5'
'set lon 119.5 121.3'
'set lat 23 24'


'color -levs 5 10 15 20 30 35 -kind white->antiquewhite->mistyrose->lightpink->mediumvioletred->navy'
'set gxout grfill'
'd maskout(mean,mean>=5)'
'cbar'

'topo=topo.3(e=1,t=1)'
*'topo=const(maskout((topo-1)*100, topo>=1), 0, -u)'
'topo=maskout((topo-1)*100, topo>=1)'

'color -levs 500 1500 2500 -kind (1,1,1,0)->gray->black -gxout grfill -alpha 80'
'd topo'

'draw title 30 cases mean rainfall [mm d`a-1`n]'

ptlat=23.468
ptlon=120.711
'q w2xy 'ptlon' 'ptlat''
ptx = subwrd(result, 3)
pty = subwrd(result, 6)
'set line 3'
'draw mark 3 'ptx' 'pty' 0.1'
'set string 1 bc 10'
'set strsiz 0.1'
'draw string 'ptx' 'pty+0.5' ('ptlat', 'ptlon')'

'q gxinfo'
line=sublin(result,3)
xb1=subwrd(line,4)
xb2=subwrd(line,6)
line=sublin(result,4)
yb1=subwrd(line,4)
yb2=subwrd(line,6)

file="../twisland.txt"
idx=0
while (1)
  res = read(file)
  line1 = sublin(res,1)
  line2 = sublin(res,2)
  rc1 = subwrd(line1,1)
  if (rc1); break; endif
  val = subwrd(line2,1)

  if (val=-999.99)
    idx=0
    continue
  endif

  if (idx=0)
    lon.1 = subwrd(line2,1)
    lat.1 = subwrd(line2,2)
    idx=1
    continue
  endif

  idx = 3-idx
  lon.idx = subwrd(line2,1)
  lat.idx = subwrd(line2,2)

  'q w2xy 'lon.1' 'lat.1''
  x1 = subwrd(result, 3)
  y1 = subwrd(result, 6)

  'q w2xy 'lon.2' 'lat.2''
  x2 = subwrd(result, 3)
  y2 = subwrd(result, 6)

  if ( x1>xb2 | x2>xb2 ); continue; endif
  if ( x1<xb1 | x2<xb1 ); continue; endif
  if ( y1>yb2 | y2>yb2 ); continue; endif
  if ( y1<yb1 | y2<yb1 ); continue; endif

  'set line 1 1 3'
  'draw line 'x1' 'y1' 'x2' 'y2''
endwhile

'printim mean_preci.png x1600 y1200 white'

