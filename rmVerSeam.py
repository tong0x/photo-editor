'''
  File name: rmVerSeam.py
'''

import numpy as np
from PIL import Image
from cumMinEngVer import cumMinEngVer


def rmVerSeam(I, Mx, Tbx):
  height, width, color = I.shape
  Ix = np.zeros((height, width - 1, color))

  E = np.amin(Mx[height - 1])
  min_pos = np.argmin(Mx[height - 1])
  direct = 0
  for i in range(height):
    Ix[height - i - 1][0:min_pos] = I[height - i - 1][0:min_pos]
    Ix[height - i - 1][min_pos:width - 1] = I[height - i - 1][min_pos + 1:width]
    direct = int(Tbx[height - i - 1][min_pos])
    min_pos = min_pos + direct

  return Ix, E
