import matplotlib.pyplot as plt
import numpy as np

#Plotting format

def af_plot(x, y):
    width = 10
    plt.figure(figsize=(width, width))
    plt.grid()
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.axis('scaled')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 0.1)
    return

def panel_plot(x,y, panels):
    # plot the geometry and the panels
    width = 10
    plt.figure(figsize=(width, width))
    plt.grid()
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.plot(np.append([panel.xa for panel in panels], panels[0].xa),
                np.append([panel.ya for panel in panels], panels[0].ya),
                linestyle='-', linewidth=1, marker='o', markersize=6, color='#CD2305')
    Xc = [panel.xc for panel in panels]
    Yc = [panel.yc for panel in panels]
    Betta = [panel.beta for panel in panels]
    plen = [panel.len for panel in panels]
    Xn = np.zeros(2)
    Yn = np.zeros(2)
    for i in range(len(Xc)):
        Xn[0] = Xc[i]
        Yn[0] = Yc[i]
        if Yc[i] >= 0:
            Yn[1] = Yc[i] + plen[i] * np.sin(Betta[i])
            Xn[1] = Xc[i] + plen[i] * np.cos(Betta[i])
        else:
            Yn[1] = Yc[i] + plen[i] * np.sin(Betta[i])
            Xn[1] = Xc[i] + plen[i] * np.cos(Betta[i])
        if i == 0:  # For first panel
            plt.plot(Xn, Yn, 'b-', label='First Panel')  # Plot the first panel normal vector
        elif i == 1:  # For second panel
            plt.plot(Xn, Yn, 'g-', label='Second Panel')  # Plot the second panel normal vector
        else:  # For every other panel
            plt.plot(Xn, Yn, 'k-')

    plt.axis('scaled')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 0.1)
    return


#def cp_plot(panels, xf_data, exp_data, alpha):
def cp_plot(panels, xf_data, alpha):
    """
    Plot the Cp distribution along the airfoil surface
    :param panels: 1D panels object
    :return:
    """
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.xlabel('$x$', fontsize=16)
    plt.ylabel('$C_p$', fontsize=16)
    plt.plot([panel.xc for panel in panels if panel.loc == 'upper'],
                [panel.cp for panel in panels if panel.loc == 'upper'],
                label='upper surface',
                color='r', linestyle='-', linewidth=2, marker='o', markersize=6)
    plt.plot([panel.xc for panel in panels if panel.loc == 'lower'],
                [panel.cp for panel in panels if panel.loc == 'lower'],
                label='lower surface',
                color='b', linestyle='-', linewidth=1, marker='o', markersize=6)
    plt.plot(xf_data[0], xf_data[2], label='Xfoil Results',
             color='k', linestyle = '--', linewidth=1)
    #plt.plot(exp_data[0], exp_data[1], label='Experimental Data',
    #         color='g', linestyle='--', linewidth=1, marker='x', markersize=6)
    plt.legend(loc='best', prop={'size': 16})
    plt.xlim(-0.1, 1.1)
    plt.ylim(max([panel.cp for panel in panels])+ 0.2 , min([panel.cp for panel in panels]) - 0.2)
    plt.title('Number of panels: {:.0f} - AoA: {:.0f} deg'.format(panels.size, alpha), fontsize=16);

