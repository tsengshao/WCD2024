'reinit'
'open ../gs_ctl_tpe/surface.ctl'
e=1
'define mean=const(sprec,0)'
'define freq=const(sprec,0)'

while(e<=30)
'set e 'e
say 'e='e
* daily mean precipitaiton [mm/day]
'define rain=ave(sprec*3600,t=1,t=144)*24'
'define mean=mean+rain/30'

*frequency of intensity >= 1mm/hr
'define obj=const(maskout(1,rain>=24),0,-u)'
'define freq=freq+obj'

e=e+1
endwhile

'set sdfwrite -flt -3dt -rt -nc4 -zip mean_preci.nc'
'set sdfattr mean String units mm/day'
'set sdfattr mean String long_name 30 cases mean of daily precipiation'
'sdfwrite mean'
'clear sdfwrite'

'set sdfwrite -flt -3dt -rt -nc4 -zip freq_24mmd.nc'
'set sdfattr freq String units count'
'set sdfattr freq String long_name number of daily precipiation >= 24mmdy'
'sdfwrite freq'
'clear sdfwrite'



