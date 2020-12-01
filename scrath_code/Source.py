import math
import numpy as np
from scrath_code.plot_functions import *


# Let's create a meshgrid to test the plotting function visualize the streamlines in steady condition

N = 50  # Number of points in each direction
x_start, x_end = -2.0, 2.0  # Boundaries in the x-direction
y_start, y_end = -1.0, 1.0  # Boundaries in the y-direction
x = np.linspace(x_start, x_end, N)  # Creates a 1D array with x-coordinates
y = np.linspace(y_start, y_end, N)  # Creates a 1D array with y-coordiantes

X, Y = np.meshgrid(x, y)   # Creates a mesh grid with the aforesaid x, y coordinates

# scatter_graph = plot_scatter(X, Y,  x_start, x_end, y_start, y_end)


def source(sigma, x_s, y_s, X, Y, x_start, y_start):
    """
    This function calculates the parameters of a source element in potentical flow
    :param sigma: source strength:
    :param x_s: x-axis position of the source:
    :param y_s: y-axis position of the source:
    :return soruce paramters:
    """

    # compute the velocity field on the mesh grid
    u_s = (sigma / (2 * math.pi) *
                (X - x_s) / ((X - x_s) ** 2 + (Y - y_s) ** 2))
    v_s = (sigma / (2 * math.pi) *
                (Y - y_s) / ((X - x_s) ** 2 + (Y - y_s) ** 2))

    width = 10.0
    height = (y_end - y_start) / (x_end - x_start) * width
    plt.figure(figsize=(width, height))
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.xlim(x_start, x_end)
    plt.ylim(y_start, y_end)
    plt.streamplot(X, Y, u_s, v_s, density=2, linewidth=1, arrowsize=2, arrowstyle='->')
    plt.scatter(x_s, y_s, color='r', s=80, marker='o')

    return


#%%

source(sigma=5, x_s=-1, y_s=0, X=X, Y=Y, x_start=x_start, y_start=y_start)