import numpy as np
import math
from objects.panel import Panel

def define_panels(x, y, N=40):
    """
    This function discretizes the airfoil in panel by using
    a cosine distribution. For this aim, both x and y coordinates
    of the airfoil are employed to create an 'auxiliary' circle.
    Then the panels are calculated by interpolation according to
    the desired number of panels N, (by default N=40)
    :param x:
    :param y:
    :param N:
    :return:
    """
    R = (x.max() - x.min()) / 2  # Radius of auxiliary cicle
    x_center = (x.max() + x.min()) / 2  # Location of the center of the auxiliary cirle
    x_circle = x_center + R * np.cos(np.linspace(0.0, 2 * math.pi, N + 1))

    x_ends = np.copy(x_circle)  # X coordinates of the panels (projection)
    y_ends = np.empty_like(x_ends)  # "Non initialization" of the panels' y coordinates

    x, y = np.append(x, x[0]), np.append(y, y[0])  # Append the first value to the end of the np.array of data values
    # Computing the y coordinate projection for the x_ends coordinates (obtained from circle)
    I = 0  # Iterator (goes from 0 to number of len(x) -1
    for i in range(N):
        while I < len(x) - 1:
            if (x[I] <= x_ends[i] <= x[I+1]) or (x[I+1] <= x_ends[i] <= x[I]):
                break
            else:
                I += 1
        # Linear Interpolation section Equation of the segments of the airfoil (y = mx + b)
        m = (y[I+1] - y[I]) / (x[I+1] - x[I])
        b = y[I+1] - m*x[I+1]
        y_ends[i] = m*x_ends[i] + b

    y_ends[N] = y_ends[0]

    panels = np.empty(N, dtype=object)
    for i in range(N):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i+1], y_ends[i+1])

    return panels


