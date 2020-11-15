# Author = Dario Rodriguez
# Start date = 11/14/2020
# Institution: University of Illinois at Urbana Champaign

# We have to import the libraries that we'll use

import math
import numpy
from scipy import integrate
from matplotlib import pyplot as plt
from readFunctions.read_doc import *

# General variables (modify if neccesary)
main_path = 'C:/Users/dario/OneDrive - University of Illinois - Urbana/First Semester/Applied Aerodynamics/Project Aerodynamics/Panel_method'



x,y = read_txt('naca0012',main_path)

