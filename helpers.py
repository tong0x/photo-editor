import numpy as np
import math
'''
  File name: helpers.py
  Author:
  Date created:
'''

'''
  File clarification:
    Helpers file that contributes the project
    You can design any helper function in this file to improve algorithm
'''

def discretize(angle):

    pi = math.pi

    #Condition
    if angle < 0:
        angle += 2 * pi
    if angle >= 2 * pi:
        angle -= 2 * pi

    # Edge discretize into 8 angles
    if angle >= 0 and angle < pi / 4:
        angle = 0
    elif angle >= pi / 4 and angle < pi / 2:
        angle = pi / 4
    elif angle >= pi / 2 and angle < 3 * pi / 4:
        angle = pi / 2
    elif angle >= 3 * pi / 4 and angle < pi:
        angle = 3 * pi / 4
    elif angle >= pi and angle < 5 * pi / 4:
        angle = pi
    elif angle >= 5 * pi / 4 and angle < 3 * pi / 2:
        angle = 5 * pi / 4
    elif angle >= 3 * pi / 2 and angle < 7 * pi / 4:
        angle = 3 * pi / 2
    elif angle >= 7 * pi / 4 and angle < 2 * pi:
        angle = 7 * pi / 4
    return angle



