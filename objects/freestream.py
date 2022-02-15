import numpy as np


class Freestream:
    """
    Freestream conditions
    TODO
    """
    def __init__(self, u_inf = 1.0, alpha = 0.0):
        """
        Sets the freestream speed and angle (with respect to the x-axis)

        :param u_inf: (float) freestream speed, default = 1.0 (unitary)
        :param alpha: (float) angle of attack, default = 0 (degrees)
        """
        self.u_inf = u_inf
        self.alpha = np.radians(alpha)