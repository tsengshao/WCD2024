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

'color -levs 1 3 5 7 10 12 15 -kind white->grainbow'
'set gxout grfill'
'd maskout(freq.2,freq.2>1)'
'cbar'

'topo=topo.3(e=1,t=1)'
'topo=maskout((topo-1)*100, topo>=1)'

'color -levs 500 1500 2500 -kind (1,1,1,0)->gray->black -gxout grfill -alpha 80'
'd topo'

'draw title count of extreme rainfall (24 mm d`a-1`n)'

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

  'set line 1 1 3'
  'draw line 'x1' 'y1' 'x2' 'y2''
endwhile

'printim freq_preci.png x1600 y1200 white'

