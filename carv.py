'''
  File name: carv.py
  Author:
  Date created:
'''

'''
'''

import numpy as np
from PIL import Image
from cumMinEngHor import cumMinEngHor
from cumMinEngVer import cumMinEngVer
from rmVerSeam import rmVerSeam
from rmHorSeam import rmHorSeam
from genEngMap import genEngMap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import imageio

def carv(I, nr, nc):
  res_list = []
  height, width, color = I.shape
  T = np.zeros((nr+1, nc+1))
  e = genEngMap(I)
  Ic = I
  Mx, Tbx = cumMinEngVer(e)
  My, Tby = cumMinEngHor(e)
  removed_c = 0
  removed_r = 0
  T[0][1] = np.amin(Mx[height-1])
  My_transpose = np.transpose(My)
  T[1][0] = np.amin(My_transpose[height-1])
  for i in range(nr + nc):
    
    if removed_c == nc:
      print("all columns removed")
      My, Tby = cumMinEngHor(e)
      Ic, E = rmHorSeam(Ic, My, Tby)
      res_list.append(Ic)
      e = genEngMap(Ic)
      removed_r += 1
    elif removed_r == nr:
      print("all rows removed")
      Mx, Tbx = cumMinEngVer(e)
      Ic, E = rmVerSeam(Ic, My, Tby)
      res_list.append(Ic)
      e = genEngMap(Ic)
      removed_c += 1
    elif T[removed_r][removed_c+1] > T[removed_r+1][removed_c]: #here is the problem
      print("removing row")
      My, Tby = cumMinEngHor(e)
      Ic, E = rmHorSeam(Ic, My, Tby)
      res_list.append(Ic)
      e = genEngMap(Ic)
      removed_r += 1
      Mx, Tbx = cumMinEngVer(e)
      My, Tby = cumMinEngHor(e)
      T[removed_r][removed_c+1] = np.amin(Mx[height-1-removed_r])
      My_transpose = np.transpose(My)
      if (removed_r < nr):
        T[removed_r+1][removed_c] = np.amin(My_transpose[width-1-removed_c])
    else:
      print("removing column")
      Mx, Tbx = cumMinEngVer(e)
      Ic, E = rmVerSeam(Ic, Mx, Tbx)
      res_list.append(Ic)
      e = genEngMap(Ic)
      removed_c += 1
      Mx, Tbx = cumMinEngVer(e)
      My, Tby = cumMinEngHor(e)
      if (removed_c < nc):
        T[removed_r][removed_c+1] = np.amin(Mx[height-1-removed_r])
      My_transpose = np.transpose(My)
      T[removed_r+1][removed_c] = np.amin(My_transpose[width-1-removed_c])
  
  return np.uint8(Ic), T
