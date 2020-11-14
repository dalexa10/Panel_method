import math
import numpy as np
import matplotlib.pyplot as plt
from plotFunctions.plot_functions import *


# Let's create a source to visualize the streamlines in steady condition

N = 50  # Number of points in each direction
x_start, x_end = -2.0, 2.0  # Boundaries in the x-direction
y_start, y_end = -1.0, 1.0  # Boundaries in the y-direction
x = np.linspace(x_start, x_end, N)  # Creates a 1D array with x-coordinates
y = np.linspace(y_start, y_end, N)  # Creates a 1D array with y-coordiantes

X, Y = np.meshgrid(x, y)   # Creates a mesh grid with the aforesaid x, y coordinates

scatter_graph = plot_scatter(X, Y,  x_start, x_end, y_start, y_end)

