import numpy as np
import shapefile

fname = 'COUNTY_MOI_1090820.shp'
idlist = np.array([ 1,2,3,4,5,\
                    6,7,8,9,10,\
                   11,12,13,15,\
                   16,17,19,20,21])
shape = shapefile.Reader(fname)
#print(shape.records())

gap_value = np.ones((1,2))*-999.99
lonlat = np.copy(gap_value)
city   = np.array(['city'])
#for i in idlist:
#for i in range(22):
for i in idlist:
  c = shape.shapeRecords()[i]
  lonlat_sub = np.array(c.shape.points)
  dis = np.sum(np.diff(lonlat_sub,axis=0)**2, axis=1)**0.5
  idx = np.nonzero(dis>0.05)[0]
  print(c.record[2], idx)
  lonlat_sub = np.insert(lonlat_sub,idx+1,-999.99,axis=0)

  name=np.array(c.record[3].split()[0])
  lonlat = np.vstack((lonlat, lonlat_sub, gap_value))
  city   = np.hstack((city,   name.repeat(lonlat_sub.shape[0]), 'city'))

# maskout the perimeter
npoint = 0
length = np.zeros(lonlat.shape[0])
for i in range(length.size):
  if ( lonlat[i,0]==-999.99 ):
    length[i] = -999.99
    if ( npoint > 0):
      per = np.sum(np.sum(np.diff(lonlat[idx0:i,:],axis=0)**2, axis=1)**0.5)
      length[idx0-1:i] = per
      #print(per)
    idx0=i+1
    npoint=0
    continue
  npoint += 1

condi = (length>0.4)*(city=='Chiayi')
condi = condi+(length>0.5)*(city!='Chiayi')*(city!='Yunlin')
condi = condi+(length>2)*(city=='Yunlin')
idx = np.where(condi)[0]

lonlat = lonlat[idx,:]
city   = city[idx]

dis = np.sum(np.diff(lonlat,axis=0)**2, axis=1)**0.5
idx = np.nonzero(dis>0.05)[0]
print(idx)
lonlat = np.insert(lonlat,idx+1,-999.99,axis=0)



np.savetxt(f'../twisland.txt', lonlat, fmt='%10.5f')

