import math

class Panel:
    """
    Each panel is considered an object in this code. Thus,
    this class constains the information for each panel.
    """

    def __init__(self, xa, ya, xb, yb):
        """
        This function initializes the panel "object".
        :param xa: x-coordinate of first point of panel (float)
        :param ya: y-coordinate of first point of panel (float)
        :param xb: x-coordinate of end point of panel (float)
        :param yb: y-coordinate of end point of panel (float)

        The following attributes are added to the "panel" object
        length, angle, define if panels in on lower and upper surface
        Initialize source strength, tangential velocity, and pressure
        coefficient to zero
        """
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb
        self.xc, self.yc = (xa + xb) / 2, (ya + yb) / 2  # Control point (middle of the panel)
        self.len = math.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)  # Length of panel

        # Orientation of panel normal vector with respect to the positive x axis
        if xb - xa <= 0.0:
            self.beta = math.acos((yb - ya) / self.len)
        elif xb - xa > 0.0:
            self.beta = math.acos(-(yb - ya) / self.len)
        
        # Location of the panel (upper or lower surface)
        if self.beta <= math.pi:
            self.loc = 'upper'
        else:
            self.loc = 'lower'

        self.sigma = 0.0  # source strength
        self.vt = 0.0  # tangential velocity
        self.cp = 0.0  # pressure coefficient