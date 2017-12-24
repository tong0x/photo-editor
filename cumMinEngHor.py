'''
  File name: cumMinEngHor.py
'''

import numpy as np
from PIL import Image
from cumMinEngVer import cumMinEngVer


def cumMinEngHor(e):
    my, tby = cumMinEngVer(np.transpose(e))
    My = np.transpose(my)
    Tby = np.transpose(tby)
    return My, Tby
