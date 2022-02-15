import numpy as np
import math
from scipy import integrate
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
    x_circle = x_center + R * np.cos(np.linspace(0.0, 2 * np.pi, N + 1))

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


def integral(x, y, panel, dxdz, dydz):
    """
    Calculates the normal velocity geometric integral (numerically)

    :param x: x coordinate of the target point
    :param y: y coordinate of the target point
    :param panel: panel object (source panel which contribution is evaluated)
    :param dxdz: float Value of the x derivative in a certain direction TODO: replace with cosine or sine Betta
    :param dydz: float Value of the y derivative in a certain direction
    :return:
    Integral over the panel of the influence at a given target point
    """
    def integrand(s):
        """
        This is just a function of s, that is going to be integrated
        """
        return (((x - (panel.xa - np.sin(panel.beta) * s)) * dxdz +
                 (y - (panel.ya + np.cos(panel.beta) * s)) * dydz) /
                ((x - (panel.xa - np.sin(panel.beta) * s))**2 +
                 (y - (panel.ya + np.cos(panel.beta) * s))**2))

    return integrate.quad(integrand, 0.0, panel.len)[0]


def source_contribution_normal(panels):
    """
    Builds the source contribution matrix for the normal velocity

    :param panels: 1D array of panel objects
    :return:
    A: 2D Numpy array of floats - Source contribution matrix
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # Source contribution on a panel from itself
    np.fill_diagonal(A, 0.5)

    # Source contribution on a panel from others
    intt = []
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = 0.5 / np.pi * integral(panel_i.xc, panel_i.yc,
                                                  panel_j,
                                                  np.cos(panel_i.beta),
                                                  np.sin(panel_i.beta))
                intt.append(integral(panel_i.xc, panel_i.yc, panel_j, np.cos(panel_i.beta), np.sin(panel_i.beta)))

    return A, intt

def vortex_contribution_normal(panels):
    """
    Builds the vortex contribution matrix for the normal velocity

    :param panels: 1D array of Panel objects
    :return:
    A: 2D Numpy array of floats
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # Vortex contribution on a panel from itself
    np.fill_diagonal(A, 0.0)
    # Vortex contribution on a panel from others
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = -0.5 / np.pi * integral(panel_i.xc, panel_i.yc,
                                                   panel_j,
                                                   np.sin(panel_i.beta),
                                                   -np.cos(panel_i.beta))
    return A


def kutta_condition(A_source, B_vortex):
    """
    Builds the Kutta condition array for the source-vortex method.

    :param A_source: 2D numpy array of floats
                    Source contribution matrix to calculate the normal velocity
    :param B_vortex: 2D numpy array of floats
                    Vortex contribution matrix to calculate the normal velocity
    :return:
    b: 1D Numpy array of floats
       Left hand side of the Kutta condition to form the N+1 equations
    """
    b = np.empty(A_source.shape[0] + 1, dtype=float)
    # Matrix of source contribution on tangential velocity
    # is the same than matrix of vortex contribution on normal velocity
    b[:-1] = B_vortex[0, :] + B_vortex[-1, :]
    # Matrix of vortex contribution on tangential velocity
    # is the opposite of matrix of source contribution on normal velocity
    b[-1] = - np.sum(A_source[0, :] + A_source[-1, :])

    return b


def build_singularity_matrix(A_source, B_vortex):
    """
    Builds the left-hand side matrix of the system
    arising from souce and vortex contributions

    :param A_source: 2D numpy array of floats
                    Source contribution matrix for the normal velocity
    :param B_vortex: 2D numpy array of floats
                    Vortex contribution matrix for the normal velocity
    :return:
    A: 2D numpy array of floats
    Matrix of the linear system
    """
    A = np.empty((A_source.shape[0] + 1, A_source.shape[1] + 1), dtype=float)
    # Source contribution matrix
    A[:-1, :-1] = A_source
    # Vortex contribution array
    A[:-1, -1] = np.sum(B_vortex, axis=1)
    # Kutta condition array
    A[-1, :] = kutta_condition(A_source, B_vortex)

    return A

def build_freestream_rhs(panels, freestream):
    """
    Builds the right hand side of the system of equations
    arising from the freestream contribution

    :param panels: 1D array of panel objects
    :param freestream: freestream object (free stream conditions)
    :return:
    b: 1D numpy array of floats
       Freestream contribution on each panel and on the Kutta condition
    """
    b = np.empty(panels.size + 1, dtype=float)
    # freestream contribution on each panel
    for i, panel in enumerate(panels):
        b[i] = -freestream.u_inf * np.cos(freestream.alpha - panel.beta)
    # freestream contribution on the Kutta condition
    b[-1] = -freestream.u_inf * (np.sin(freestream.alpha - panels[0].beta) +
                                 np.sin(freestream.alpha - panels[-1].beta))
    return b


def compute_tangential_velocity(panels, freestream, gamma, A_source, B_vortex):
    """
    Computes the tangential surface velocity

    :param panels: 1D array of panel objects
                  List of panels
    :param freestream: Freestream object
                       Freestream conditions
    :param gamma: float
                  Circulation
    :param A_source: 2D Numpy array of floats
                    Source contributions for the normal velocity
    :param B_vortex: 2D Numpy array of floats
                    Vortex contribution matriix for the normal velocity
    :return:
    tangential velocities as panel attribute
    """
    A = np.empty((panels.size, panels.size + 1), dtype=float)
    # Matrix of source contribution on tangential velocity is the same
    # than matrix of vortex contribution on normal velocity
    A[:, :-1] = B_vortex

    # Matrix of vortex contribution on tangential velocity is the opposite
    # than matrix of source contribution on normal velocity
    A[:, -1] = - np.sum(A_source, axis=1)

    # freestream contribution
    b = freestream.u_inf * np.sin([freestream.alpha - panel.beta for panel in panels])

    strengths = np.append([panel.sigma for panel in panels], gamma)

    tangential_velocities = np.dot(A, strengths) + b

    for i, panel in enumerate(panels):
        panel.vt = tangential_velocities[i]


def compute_pressure_coefficient(panels, freestream):
    """
    Computes the surface pressure coefficients

    :param panels: 1D array of Panel objects
    :param freestream: Freestream Object
    :return:
    cp attribute to panel object
    """
    for panel in panels:
        panel.cp = 1.0 - (panel.vt / freestream.u_inf)**2


def get_velocity_field(panels, freestream, gamma, X, Y):
    """
    Computes the velocity field on a given 2D mesh.

    Parameters
    ---------
    panels: 1D array of Panel objects
        The source panels.
    freestream: Freestream object
        The freestream conditions.
    X: 2D Numpy array of floats
        x-coordinates of the mesh points.
    Y: 2D Numpy array of floats
        y-coordinate of the mesh points.

    Returns
    -------
    u: 2D Numpy array of floats
        x-component of the velocity vector field.
    v: 2D Numpy array of floats
        y-component of the velocity vector field.
    """
    # freestream contribution
    u = freestream.u_inf * math.cos(freestream.alpha) * np.ones_like(X, dtype=float)
    v = freestream.u_inf * math.sin(freestream.alpha) * np.ones_like(X, dtype=float)
    # add the contribution from each source (superposition powers!!!)
    vec_intregral = np.vectorize(integral)
    for panel in panels:
        u += panel.sigma / (2.0 * math.pi) * vec_intregral(X, Y, panel, 1.0, 0.0) - \
             gamma / (2.0 * math.pi) * vec_intregral(X, Y, panel, 0.0, -1.0)

        v += panel.sigma / (2.0 * math.pi) * vec_intregral(X, Y, panel, 0.0, 1.0) - \
             gamma / (2.0 * math.pi) * vec_intregral(X, Y, panel, 1.0, 0.0)
    return u, v