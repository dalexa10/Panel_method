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
from aux_func.Aux_Func import *
from objects.panel import *
from objects.freestream import *


# General variables (modify if neccesary)
main_path = 'C:/Users/dario/OneDrive - University of Illinois - Urbana/First Semester\
/Applied Aerodynamics/Project Aerodynamics/Panel_method'

# Reading the file
af_name = 'naca0012'
verifier = check_af(af_name, main_path)

if verifier == True:
    x, y = read_txt(af_name, main_path)
    print("Reading the file, please wait")
else:
    print('Error')

#af_plot(x,y) # Deactivate this part to check the airfoil shape

# Calculation zone
N = 52  # Number of panels
panels = define_panels(x, y, N)
panel_plot(x, y, panels)

# Defining the freestream conditions
alpha = 0.0
freestream = Freestream(u_inf=1.0, alpha=alpha)

# Defining Source and Vortex contribution
A_source, intt = source_contribution_normal(panels)
B_vortex = vortex_contribution_normal(panels)

# Defining Matrices for the linear system A*x = b
A = build_singularity_matrix(A_source, B_vortex)
b = build_freestream_rhs(panels, freestream)

# Solving for singularity strenghts
strengths = np.linalg.solve(A, b)

# Store source strength on each panel
for i, panel in enumerate(panels):
    panel.sigma = strengths[i]

# Store circulation density
gamma = strengths[-1]

# Tangential velocity at each panel center
compute_tangential_velocity(panels, freestream, gamma, A_source, B_vortex)

# Compute pressure coefficient
compute_pressure_coefficient(panels, freestream)

# Plot surface pressure coefficient
xf_data = read_xfoil('naca2412_xfoil_8', main_path)
#exp_data = read_exp('naca0012_exp_15', main_path)
# cp_plot(panels, xf_data, exp_data, alpha)
cp_plot(panels, xf_data, alpha)

# Calculating the accuracy
accuracy = sum([panel.sigma * panel.len for panel in panels])
print('sum of singularity strengths: {:0.6f}'.format(accuracy))

# Calculating the lift coefficient
# Chord
c = abs(max(panel.xa for panel in panels) -
        min(panel.xa for panel in panels))
cl = (gamma * sum(panel.len for panel in panels) /
      (0.5 * freestream.u_inf * c))
print('lift coefficient: CL = {:0.3f}'.format(cl))

# Mesh grid to define the streamlines
# define a mesh grid
nx, ny = 40, 40  # number of points in the x and y directions
x_start, x_end = -1.0, 2.0
y_start, y_end = -0.3, 0.3
X, Y = numpy.meshgrid(np.linspace(x_start, x_end, nx),
                      np.linspace(y_start, y_end, ny))

# compute the velocity field on the mesh grid
u, v = get_velocity_field(panels, freestream, gamma, X, Y)

# plot the velocity field
width = 10
plt.figure(figsize=(width, width))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.streamplot(X, Y, u, v,
                  density=1, linewidth=1, arrowsize=1, arrowstyle='->')
plt.fill([panel.xc for panel in panels],
            [panel.yc for panel in panels],
            color='k', linestyle='solid', linewidth=2, zorder=2)
plt.axis('scaled')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.title('Streamlines around a {} airfoil (AoA = ${}^o$)'.format(af_name, alpha),
             fontsize=16);

# compute the pressure field
cp = 1.0 - (u**2 + v**2) / freestream.u_inf**2

# plot the pressure field
width = 10
plt.figure(figsize=(width, width))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
contf = plt.contourf(X, Y, cp,
                        levels=np.linspace(-2.0, 1.0, 500), extend='both', cmap = 'jet')
cbar = plt.colorbar(contf,
                       orientation='horizontal',
                       shrink=0.5, pad = 0.1,
                       ticks=[-2.0, -1.0, 0.0, 1.0])
cbar.set_label('$C_p$', fontsize=16)
plt.fill([panel.xc for panel in panels],
            [panel.yc for panel in panels],
            color='k', linestyle='solid', linewidth=2, zorder=2)
plt.axis('scaled')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.title('Contour of pressure field', fontsize=16);

