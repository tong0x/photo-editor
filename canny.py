import numpy as np
import pdb
from scipy import signal, ndimage
import matplotlib.pyplot as plt
import utils
from interp import interp2
import math
from helpers import discretize
import os
from PIL import Image
from Test_script import Test_script

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 18:07:57 2017

@author: TPow
"""
np.seterr(divide='ignore', invalid='ignore')


def findDerivatives(I_gray):

  # 2D Gaussian kernel
  G = utils.GaussianPDF_2D(0, 1, 10, 10)

  # Deviation vectors/filter for horizontal and vertical direction (to compute gradient of Gaussian)
  dx = [[1.0, 0.0, -1.0]]
  dy = [[1.0], [0.0], [-1.0]]

  # Perform convolution of Gaussian and filters, get gradient of Gaussian (10 by 10)
  Gx = signal.convolve2d(G, dx, mode='same', boundary='symm')
  Gy = signal.convolve2d(G, dy, mode='same', boundary='symm')

  # Perform convolution of original image matrix and gradient matrix
  ix = signal.convolve2d(I_gray, Gx, mode='same', boundary='symm')
  iy = signal.convolve2d(I_gray, Gy, mode='same', boundary='symm')

  # Compute magnitude of the gradient
  im = np.sqrt(np.square(ix) + np.square(iy))

  # Get gradient of the image
  idx = signal.convolve2d(I_gray, dx, mode='same')
  idy = signal.convolve2d(I_gray, dy, mode='same')

  # Get orientation of the edge
  orientation = np.arctan(np.divide(idy, idx))

  return im, ix, iy, orientation


def nonMaxSup(Mag, Ori):

  (yLength, xLength) = Mag.shape

  coordinates = (yLength, xLength)
  coordinates_x = coordinates[1]
  coordinates_y = coordinates[0]

  # Initialize the meshgrid
  mGridY, mGridX = np.meshgrid(np.arange(0, coordinates_x), np.arange(0, coordinates_y))

  # Modify the meshgrid with orientation
  interp_location = np.add(mGridY, np.sin(Ori))
  interp_location_2 = np.add(mGridX, np.cos(Ori))
  interp_location_3 = np.subtract(mGridY, np.sin(Ori))
  interp_location_4 = np.subtract(mGridX, np.cos(Ori))

  # Interpolate and get magnitude of new points
  interp_pos = interp2(mGridX, mGridY, Mag, interp_location, interp_location_2)
  interp_neg = interp2(mGridX, mGridY, Mag, interp_location_3, interp_location_4)

  # New matrix created by logical operation
  Compare = np.logical_and(Mag > interp_pos, Mag > interp_neg)

  # Change into binary matrix
  Compare_int = Compare.astype(np.int)

  return Compare_int


def edgeLink(M, Mag, Ori):

  # Multiply magnitude with
  binary_mag = np.multiply(M, Mag)

  row, column = binary_mag.shape

  edge_map = np.empty([row, column])

  # Declare low and high threshold
  threshold_low = 0.03 * np.amax(binary_mag)
  threshold_high = 2.5 * threshold_low

  # Set thresholds
  for j in range(0, column):
    for i in range(0, row):
      if binary_mag[i, j] > threshold_high:
        edge_map[i, j] = 1
      elif binary_mag[i, j] <= threshold_low:
        edge_map[i, j] = 0
      else:
        edge_map[i, j] = 0.5

  # Hysteresis
  for j in range(0, column):
    for i in range(0, row):
      # Start at strong edge
      if edge_map[i, j] == 0.5:

        pi = math.pi

        # Orientation of gradient
        angle = Ori[i, j]

        # Orientations of edge perpendicular to gradient direction
        angle_neg = discretize(angle - np.cos(angle))
        angle_pos = discretize(angle + np.cos(angle))

        neighbor_1 = 0.0
        neighbor_2 = 0.0
        row_1 = 0
        row_2 = 0
        column_1 = 0
        column_2 = 0

        if angle_neg == 0 or angle_neg == pi or angle_pos == 0 or angle_pos == pi:
          if j + 1 < column:
            neighbor_1 = edge_map[i][j + 1]
            row_1 = i
            column_1 = j + 1
          if j - 1 >= 0:
            neighbor_2 = edge_map[i][j - 1]
            row_2 = i
            column_2 = j - 1
        elif angle_neg == pi / 2 or angle_neg == 3 * pi / 2 or angle_pos == pi / 2 or angle_pos == 3 * pi / 2:
          if i + 1 < row:
            neighbor_1 = edge_map[i + 1][j]
            row_1 = i + 1
            column_1 = j
          if i - 1 >= 0:
            neighbor_2 = edge_map[i - 1][j]
            row_2 = i - 1
            column_2 = j
        elif angle_neg == pi / 4 or angle_neg == 5 * pi / 4 or angle_pos == pi / 4 or angle_pos == 5 * pi / 4:
          if i + 1 < row and j + 1 < column:
            neighbor_1 = edge_map[i + 1][j + 1]
            row_1 = i + 1
            column_1 = j + 1
          if i - 1 >= 0 and j - 1 >= 0:
            neighbor_2 = edge_map[i - 1][j - 1]
            row_2 = i - 1
            column_2 = j - 1
        elif angle_neg == 3 * pi / 4 or angle_neg == 7 * pi / 4 or angle_pos == 3 * pi / 4 or angle_pos == 7 * pi / 4:
          if i - 1 >= 0 and j + 1 < column:
            neighbor_1 = edge_map[i - 1][j + 1]
            row_1 = i - 1
            column_1 = j + 1
          if i + 1 < row and j - 1 >= 0:
            neighbor_2 = edge_map[i + 1][j - 1]
            row_2 = i + 1
            column_2 = j - 1

        ori_difference_1 = abs(Ori[i][j] - Ori[row_1][column_1])
        ori_difference_2 = abs(Ori[i][j] - Ori[row_2][column_2])

        if neighbor_1 < 1 and neighbor_2 < 1:
          edge_map[i][j] = 0
        elif neighbor_1 == 1 and neighbor_2 < 1:
          if ori_difference_1 >= threshold_low and ori_difference_1 <= threshold_high:
            edge_map[i][j] = 1
          else:
            edge_map[i][j] = 0
        elif neighbor_2 == 1 and neighbor_1 < 1:
          if ori_difference_2 >= threshold_low and ori_difference_2 <= threshold_high:
            edge_map[i][j] = 1
          else:
            edge_map[i][j] = 0
        elif neighbor_1 == 1 and neighbor_2 == 1:
          if ori_difference_1 >= threshold_low and ori_difference_1 <= threshold_high or ori_difference_2 >= threshold_low and ori_difference_2 <= threshold_high:
            edge_map[i][j] = 1
          else:
            edge_map[i][j] = 0

  # Final for loop to clear weak values
  for j in range(0, column):
    for i in range(0, row):
      if edge_map[i][j] == 0.5:
        edge_map[i][j] = 0

  return edge_map

# cannyEdge detector


def cannyEdge(Im):
  image = Image.open(Im)
  image.load()
  I = np.asarray(image, dtype='uint8')
  if I.ndim == 3:
    # convert RGB image to gray color space if
    im_gray = utils.rgb2gray(I)
  else:
    im_gray = I

  Mag, Magx, Magy, Ori = findDerivatives(im_gray)
  M = nonMaxSup(Mag, Ori)
  E = edgeLink(M, Mag, Ori)

  # only when test passed that can show all results
  if Test_script(im_gray, E):
    # visualization results
    utils.visDerivatives(im_gray, Mag, Magx, Magy)
    utils.visCannyEdge(I, M, E)

    plt.show()

  return E
