import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import copy

def what_do_you_want_to_see(velo,spec):
    return np.amax(spec)

def read_fits(dirc,file_name):
  print 'reading ' + file_name + ' at ' + dirc
  data = fits.open(dirc+file_name)
  return data

def read_ascii(dirc,file_name,skip_num=0):
  print 'reading ' + file_name + ' at ' + dirc
  val1=[]; val2=[]
  with  open(dirc+file_name,'r') as ascii_data :
    if skip_num >= 1:
      for i in range(skip_num):
        next(ascii_data)
    for line in ascii_data:
      line = line.strip()
      data = line.split()
      val1=np.append(val1,np.float(data[0]))
      val2=np.append(val2,np.float(data[1]))
  return val1, val2

def define_vspace(hdr):
  min_vel = (hdr['CRVAL3']-(hdr['CRPIX3']-1)*hdr['CDELT3'])*1.0e-3
  max_vel = (hdr['CRVAL3']+(hdr['NAXIS3']-hdr['CRPIX3'])*hdr['CDELT3'])*1.0e-3
  vspace = np.linspace(min_vel,max_vel,hdr['NAXIS3'])
  return vspace

def produce_map_fig(hdu):
  vspace = define_vspace(hdu[0].header)
  cube = hdu[0].data
  new_hdr = copy.deepcopy(hdu[0].header)
  new_hdr['NAXIS'] = 2
  del new_hdr['NAXIS3']
  del new_hdr['NAXIS4']
  del new_hdr['CTYPE3']
  del new_hdr['CRVAL3']
  del new_hdr['CDELT3']
  del new_hdr['CRPIX3']
  del new_hdr['CROTA3']
  del new_hdr['CTYPE4']
  del new_hdr['CRVAL4']
  del new_hdr['CDELT4']
  del new_hdr['CRPIX4']
  del new_hdr['CROTA4']
  wcs = WCS(new_hdr)
  sz = np.shape(cube)
  map_mat = np.zeros([sz[2],sz[3]])
  for i in range(sz[3]):
    for j in range(sz[2]):
      value = what_do_you_want_to_see(vspace,cube[0,:,j,i])
      map_mat[j,i] = value
  
  fig = plt.figure(501)
  fig_layout = gridspec.GridSpec(1,1)
  sub_fig = fig.add_subplot(fig_layout[0,0],projection=wcs)
  map_img = plt.imshow(map_mat)
  plt.colorbar(map_img)
  plt.xlabel('R.A. (J2000)')
  plt.ylabel('Dec. (J2000)')
  plt.show()
  plt.close(501)
  
    
