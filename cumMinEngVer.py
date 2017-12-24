'''
  File name: cumMinEngVer.py
'''

import numpy as np
from PIL import Image


def cumMinEngVer(e):
  height, width = e.shape
  Mx = np.zeros((height, width))
  Tbx = np.zeros((height, width))
  Mx[0] = e[0]

  for i in range(1, height):
    for j in range(width):
      if j == 0:
        Mx[i][j] = e[i][j] + min(Mx[i - 1][j], Mx[i - 1][j + 1])
        if Mx[i - 1][j] < Mx[i - 1][j + 1]:
          Tbx[i][j] = 0
        else:
          Tbx[i][j] = 1
      elif j == (width - 1):
        Mx[i][j] = e[i][j] + min(Mx[i - 1][j], Mx[i - 1][j - 1])
        if Mx[i - 1][j] < Mx[i - 1][j - 1]:
          Tbx[i][j] = 0
        else:
          Tbx[i][j] = -1
      else:
        Mx[i][j] = e[i][j] + min(Mx[i - 1][j], Mx[i - 1][j + 1], Mx[i - 1][j - 1])
        if Mx[i - 1][j] < Mx[i - 1][j + 1]:
          if Mx[i - 1][j] < Mx[i - 1][j - 1]:
            Tbx[i][j] = 0
          elif Mx[i - 1][j - 1] < Mx[i - 1][j + 1]:
            Tbx[i][j] = -1
          else:
            Tbx[i][j] = 1
        elif Mx[i - 1][j + 1] < Mx[i - 1][j - 1]:
          Tbx[i][j] = 1
        else:
          Tbx[i][j] = -1

  return Mx, Tbx
