# Author = Dario Rodriguez
# Start date = 11/14/2020
# Institution: University of Illinois at Urbana Champaign

# We have to import the libraries that we'll use

import math
import numpy
from scipy import integrate
from matplotlib import pyplot as plt
from read_dataFunc.read_doc import *
from plotFunc.plotting import *
from aux_func.Aux_Func import define_panels
from objects.panel import *
from objects.freestream import *

# General variables (modify if neccesary)
main_path = 'C:/Users/dario/OneDrive - University of Illinois - Urbana/First Semester\
/Applied Aerodynamics/Project Aerodynamics/Panel_method'



# Reading the file
x, y = read_txt('naca0012', main_path)
print("Reading the file, please wait")
#af_plot(x,y) # Deactivate this part to check the airfoil shape

# Calculation zone
N = 40  # Number of panels
panels = define_panels(x,y, N)
panel_plot(x, y, panels)

#
